\
#!/usr/bin/env python3
"""Create/update Kodförbättraren ZIP-mode resume metadata.

Current output ZIP digest is intentionally reported outside the same archive:
embedding an archive's own digest would change that digest. On next import,
`accept-input` records the actual input archive digest as the new base.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import yaml

META = ".kodforbattraren"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def init_status(workspace: Path, plan_id: str, input_zip: Path) -> Path:
    status = {
        "schema_version": 1,
        "plan_id": plan_id,
        "source": {"mode":"zip", "zip":{
            "base_name": input_zip.name,
            "base_sha256": sha256_file(input_zip),
            "last_output_name": None,
            "last_output_sha256": None,
        }},
        "progress": {
            "current_step_id": None,
            "completed_step_ids": [],
            "skipped_step_ids": [],
            "blocked_step_ids": [],
        },
        "findings": {},
        "blockers": [],
        "plan_changes": [],
        "delivery": {
            "last_completed_step_id": None,
            "verification_status": "not_run",
            "verification_summary": "",
        },
        "updated_at": now()
    }
    p = workspace / META / "work-status.yaml"
    dump(p, status)
    return p

def accept_input(status_path: Path, input_zip: Path) -> None:
    """Record the actual archive currently being resumed from."""
    s = load(status_path)
    z = s["source"]["zip"]
    z["base_name"] = input_zip.name
    z["base_sha256"] = sha256_file(input_zip)
    # If it is the previously named output, this is now the first point at
    # which its digest can be safely persisted in workspace metadata.
    if z.get("last_output_name") == input_zip.name:
        z["last_output_sha256"] = z["base_sha256"]
    s["updated_at"] = now()
    dump(status_path, s)

def prepare_delivery(status_path: Path, output_name: str, completed_step: str,
                     verification: str, summary: str, next_step: str | None) -> None:
    """Update metadata *before* packaging the output archive."""
    s = load(status_path)
    completed = s["progress"]["completed_step_ids"]
    if completed_step not in completed:
        completed.append(completed_step)
    s["progress"]["current_step_id"] = next_step
    s["delivery"]["last_completed_step_id"] = completed_step
    s["delivery"]["verification_status"] = verification
    s["delivery"]["verification_summary"] = summary
    s["source"]["zip"]["last_output_name"] = output_name
    s["source"]["zip"]["last_output_sha256"] = None
    s["updated_at"] = now()
    dump(status_path, s)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("workspace", type=Path)
    p.add_argument("plan_id")
    p.add_argument("input_zip", type=Path)
    p = sub.add_parser("accept-input")
    p.add_argument("status", type=Path)
    p.add_argument("input_zip", type=Path)
    p = sub.add_parser("prepare-delivery")
    p.add_argument("status", type=Path)
    p.add_argument("output_name")
    p.add_argument("completed_step")
    p.add_argument("verification", choices=["pass","warning","failed","blocked","not_run"])
    p.add_argument("summary")
    p.add_argument("--next-step")
    a = ap.parse_args()
    if a.cmd == "init":
        print(init_status(a.workspace, a.plan_id, a.input_zip))
    elif a.cmd == "accept-input":
        accept_input(a.status, a.input_zip)
    else:
        prepare_delivery(a.status, a.output_name, a.completed_step,
                         a.verification, a.summary, a.next_step)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
