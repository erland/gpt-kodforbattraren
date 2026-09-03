\
from pathlib import Path
import importlib.util
import json
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "zip_workspace.py"
spec = importlib.util.spec_from_file_location("zip_workspace", SCRIPT)
zw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zw)

def make_zip(path: Path, entries):
    with zipfile.ZipFile(path, "w") as z:
        for name, data in entries:
            z.writestr(name, data)

def test_rejects_path_traversal(tmp_path):
    z = tmp_path / "bad.zip"
    make_zip(z, [("../../outside.txt", "x")])
    try:
        zw.inspect_zip(z)
        assert False, "expected ZipSafetyError"
    except zw.ZipSafetyError:
        pass

def test_rejects_absolute_path(tmp_path):
    z = tmp_path / "bad.zip"
    make_zip(z, [("/outside.txt", "x")])
    try:
        zw.inspect_zip(z)
        assert False
    except zw.ZipSafetyError:
        pass

def test_rejects_symlink_entry(tmp_path):
    z = tmp_path / "link.zip"
    info = zipfile.ZipInfo("link")
    info.create_system = 3
    info.external_attr = (stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(z, "w") as f:
        f.writestr(info, "target")
    try:
        zw.inspect_zip(z)
        assert False
    except zw.ZipSafetyError:
        pass

def test_preserves_monorepo_and_build_dirs_but_excludes_safe_cache(tmp_path):
    ws = tmp_path / "ws"
    (ws/"apps"/"a").mkdir(parents=True)
    (ws/"packages"/"b").mkdir(parents=True)
    (ws/"dist").mkdir()
    (ws/"target").mkdir()
    (ws/"__pycache__").mkdir()
    (ws/"apps"/"a"/"main.ts").write_text("a")
    (ws/"packages"/"b"/"lib.ts").write_text("b")
    (ws/"dist"/"bundle.js").write_text("dist")
    (ws/"target"/"app.jar").write_bytes(b"jar")
    (ws/"__pycache__"/"x.pyc").write_bytes(b"x")
    out = tmp_path/"out.zip"
    zw.package_workspace(ws, out)
    with zipfile.ZipFile(out) as z:
        names=set(z.namelist())
    assert "apps/a/main.ts" in names
    assert "packages/b/lib.ts" in names
    assert "dist/bundle.js" in names
    assert "target/app.jar" in names
    assert "__pycache__/x.pyc" not in names

def test_roundtrip_keeps_wrapper_structure(tmp_path):
    src=tmp_path/"src.zip"
    make_zip(src,[("wrapper/README.md","r"),("wrapper/src/a.txt","a")])
    ws=tmp_path/"ws"
    zw.safe_extract(src, ws)
    out=tmp_path/"out.zip"
    zw.package_workspace(ws,out)
    with zipfile.ZipFile(out) as z:
        assert set(z.namelist()) == {"wrapper/README.md","wrapper/src/a.txt"}

def test_manifest_excludes_kodforbattraren_metadata(tmp_path):
    ws=tmp_path/"ws"
    (ws/".kodforbattraren").mkdir(parents=True)
    (ws/"src").mkdir()
    (ws/"src"/"a.txt").write_text("a")
    (ws/".kodforbattraren"/"work-status.yaml").write_text("dynamic")
    m1=zw.build_manifest(ws)
    (ws/".kodforbattraren"/"work-status.yaml").write_text("changed")
    m2=zw.build_manifest(ws)
    assert m1["root_digest"] == m2["root_digest"]
    assert [f["path"] for f in m1["files"]] == ["src/a.txt"]

def test_policy_never_auto_excludes_build_named_directories():
    policy=(ROOT/"knowledge"/"zip-workflow-policy.yaml").read_text(encoding="utf-8")
    for name in ["dist","build","target","node_modules","vendor"]:
        assert name in policy


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def test_zip_status_lifecycle_records_input_and_resumes(tmp_path):
    zs = _load_module(ROOT / "scripts" / "zip_work_status.py", "zip_work_status")
    input_zip = tmp_path / "input.zip"
    make_zip(input_zip, [("README.md", "hello")])
    ws = tmp_path / "workspace"
    ws.mkdir()
    status_path = zs.init_status(ws, "plan-1", input_zip)
    status = __import__("yaml").safe_load(status_path.read_text())
    assert status["source"]["zip"]["base_name"] == "input.zip"
    assert len(status["source"]["zip"]["base_sha256"]) == 64

    zs.prepare_delivery(status_path, "project-step-R-001.zip", "R-001",
                        "pass", "verified", "R-002")
    status = __import__("yaml").safe_load(status_path.read_text())
    assert status["delivery"]["last_completed_step_id"] == "R-001"
    assert status["progress"]["current_step_id"] == "R-002"
    assert status["source"]["zip"]["last_output_name"] == "project-step-R-001.zip"
    assert status["source"]["zip"]["last_output_sha256"] is None

    # Simulate the delivered archive becoming the next input.
    delivered = tmp_path / "project-step-R-001.zip"
    make_zip(delivered, [("README.md", "changed")])
    zs.accept_input(status_path, delivered)
    status = __import__("yaml").safe_load(status_path.read_text())
    assert status["source"]["zip"]["base_name"] == delivered.name
    assert status["source"]["zip"]["last_output_sha256"] == status["source"]["zip"]["base_sha256"]
