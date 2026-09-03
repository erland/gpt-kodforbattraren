#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
status_path = ROOT / "project-status.yaml"
schema_path = ROOT / "schemas/project-status.schema.json"


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    try:
        status = yaml.safe_load(status_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"kan inte läsa project-status/schema: {exc}")
    errors = sorted(Draft202012Validator(schema).iter_errors(status), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            path = ".".join(str(x) for x in error.path) or "<root>"
            print(f"ERROR {path}: {error.message}", file=sys.stderr)
        return 1
    progress = status["progress"]
    completed = progress["completed_steps"]
    last = progress["last_completed_step"]
    if completed != sorted(completed):
        return fail("completed_steps måste vara sorterad")
    if completed and max(completed) != last:
        return fail("last_completed_step måste motsvara högsta completed_steps")
    if len(completed) != len(set(completed)):
        return fail("completed_steps innehåller dubbletter")
    if status["state"]["overall"] == "release_ready":
        if completed != list(range(1, 21)):
            return fail("release_ready kräver steg 1-20 completed")
        if progress["current_step"] is not None:
            return fail("release_ready kräver current_step: null")
        if status["next_step"] is not None:
            return fail("release_ready kräver next_step: null")
        if status["state"]["blocking_issues"]:
            return fail("release_ready får inte ha blockerare")
    print("PASS project-status.yaml")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
