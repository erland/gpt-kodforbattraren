#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

TERMINAL = {"completed", "skipped"}

def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def derive(plan: dict, status: dict, current_source_identifier: str | None = None) -> dict:
    if current_source_identifier is not None:
        planned = plan.get("source_snapshot", {}).get("base_identifier")
        if planned and planned != current_source_identifier:
            return {"state": "reanalysis_required", "step_id": None, "title": "Källan har ändrats sedan analysen", "reason": "source_drift"}

    steps = sorted(plan["steps"], key=lambda s: s["order"])
    by_id = {s["id"]: s for s in steps}
    completed = set(status["progress"]["completed_step_ids"])
    skipped = set(status["progress"]["skipped_step_ids"])
    blocked = set(status["progress"]["blocked_step_ids"])
    current = status["progress"].get("current_step_id")
    open_blockers = [b for b in status.get("blockers", []) if b["status"] == "open"]

    if current:
        if status.get("delivery", {}).get("verification_status") == "failed":
            return {"state": "blocked", "step_id": current, "title": by_id.get(current, {}).get("title", current), "reason": "verification_failed"}
        if current not in by_id:
            raise ValueError(f"current_step_id {current} finns inte i planen")
        if current in blocked or any(b.get("step_id") == current for b in open_blockers):
            return {"state": "blocked", "step_id": current, "title": by_id[current]["title"]}
        if current not in completed and current not in skipped:
            return {"state": "continue", "step_id": current, "title": by_id[current]["title"]}

    for step in steps:
        sid = step["id"]
        if sid in completed or sid in skipped:
            continue
        if sid in blocked or any(b.get("step_id") == sid for b in open_blockers):
            continue
        dependencies = set(step.get("depends_on", []))
        if dependencies.issubset(completed | skipped):
            return {"state": "ready", "step_id": sid, "title": step["title"]}

    unresolved = [s for s in steps if s["id"] not in completed | skipped]
    if unresolved:
        return {"state": "blocked", "step_id": None, "title": "Inget körbart steg; kontrollera blockerare eller beroenden"}
    return {"state": "complete", "step_id": None, "title": "Planen är slutförd"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--status", required=True, type=Path)
    parser.add_argument("--current-source-identifier")
    args = parser.parse_args()
    result = derive(load(args.plan), load(args.status), args.current_source_identifier)
    print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True).strip())

if __name__ == "__main__":
    main()
