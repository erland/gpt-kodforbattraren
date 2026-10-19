#!/usr/bin/env python3
"""Build optional, portable Kodförbättraren Engine ZIP from the canonical source.

No MCP dependency and no assumptions about execution capability in the host.
The host must provide a writable workspace and Python 3 for actual execution.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCRIPTS = (
    "derive_next_step.py",
    "detect_technology_profiles.py",
    "generate_refactoring_plan.py",
    "github_pr_decision.py",
    "interpret_progress_command.py",
    "zip_work_status.py",
    "zip_workspace.py",
)

def build(output: Path, version: str) -> None:
    if not version or any(ch not in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-_" for ch in version):
        raise ValueError("Invalid version")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.resolve().is_relative_to((ROOT / "scripts").resolve()):
        raise ValueError("Output must be outside source scripts")
    payload = {}
    for name in RUNTIME_SCRIPTS:
        src = ROOT / "scripts" / name
        raw = src.read_bytes()
        ast.parse(raw.decode("utf-8"), filename=name)
        payload["scripts/" + name] = raw
    selftest = b'''#!/usr/bin/env python3
import ast
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "engine-manifest.json").read_text(encoding="utf-8"))
assert manifest["schema_version"] == 1
for name, digest in manifest["files"].items():
    path = root / name
    assert path.is_file(), name
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, name
    ast.parse(data.decode("utf-8"), filename=name)
print("PASS engine selftest:", len(manifest["files"]), "scripts")
'''
    manifest = {
        "schema_version": 1,
        "name": "kodforbattraren-engine",
        "version": version,
        "host_requirements": ["Python 3", "writable persistent workspace for implementation"],
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(payload.items())}
    }
    payload["scripts/selftest.py"] = selftest
    payload["engine-manifest.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    payload["README.md"] = (
        "# Kodförbättraren Engine\n\n"
        "Optional runtime helpers only. Python 3 and an actual writable workspace are required.\n"
        "Run `python scripts/selftest.py` after extraction.\n"
        "Never interpret presence of this ZIP as proof that ChatGPT Plugin supports script execution.\n"
    ).encode()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(payload.items()):
            z.writestr(name, data)
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
    print("PASS engine package:", output)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--version", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    build(args.output, args.version)
