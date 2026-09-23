#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_runtime_parity.py")], cwd=ROOT)
if proc.returncode != 0:
    errors.append("runtime parity gate failed")

status = yaml.safe_load((ROOT / "project-status.yaml").read_text(encoding="utf-8"))
progress = status.get("progress", {})
current_step = progress.get("current_step")
last_completed = int(progress.get("last_completed_step", 0))
overall = status.get("state", {}).get("overall")
in_progress_migration = current_step in {23, 24} and last_completed >= 22
completed_migration = current_step is None and last_completed == 24 and overall == "release_ready"
if not (in_progress_migration or completed_migration):
    errors.append("migration status must be step 23/24 or a consistent completed step-24 release_ready state")
if status.get("state", {}).get("blocking_issues"):
    errors.append("blocking issues must be empty")

manifest_path = ROOT / "dist" / "release-manifest.json"
if not manifest_path.is_file():
    errors.append("release-manifest.json missing")
else:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = manifest.get("artifacts", {})
    if len(artifacts) != 3:
        errors.append(f"expected 3 runtime artifacts, got {len(artifacts)}")
    required_prefixes = (
        "kodforbattraren-chat-",
        "kodforbattraren-custom-gpt-",
        "kodforbattraren-opencode-",
    )
    for prefix in required_prefixes:
        matches = [name for name in artifacts if name.startswith(prefix)]
        if len(matches) != 1:
            errors.append(f"expected one artifact with prefix {prefix}")
            continue
        name = matches[0]
        path = ROOT / "dist" / name
        if not path.is_file():
            errors.append(f"artifact missing: {name}")
            continue
        expected = artifacts[name].get("sha256")
        if expected != sha256(path):
            errors.append(f"checksum mismatch: {name}")
        try:
            with zipfile.ZipFile(path) as zf:
                bad = zf.testzip()
                if bad:
                    errors.append(f"ZIP CRC error in {name}: {bad}")
        except zipfile.BadZipFile:
            errors.append(f"invalid ZIP: {name}")

report = {
    "result": "PASS" if not errors else "FAIL",
    "runtime_parity_exit_code": proc.returncode,
    "current_step": progress.get("current_step"),
    "last_completed_step": progress.get("last_completed_step"),
    "errors": errors,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
