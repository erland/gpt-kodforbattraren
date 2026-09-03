#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    (ROOT / "schemas/finding.schema.json", ROOT / "schemas/examples/finding.yaml"),
    (ROOT / "schemas/refactoring-plan.schema.json", ROOT / "schemas/examples/refactoring-plan.yaml"),
    (ROOT / "schemas/work-status.schema.json", ROOT / "schemas/examples/work-status-zip.yaml"),
    (ROOT / "schemas/work-status.schema.json", ROOT / "schemas/examples/work-status-github.yaml"),
]

def load(path: Path):
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return yaml.safe_load(path.read_text(encoding="utf-8"))

errors = []
for schema_path, instance_path in CASES:
    validator = Draft202012Validator(load(schema_path), format_checker=FormatChecker())
    case_errors = sorted(validator.iter_errors(load(instance_path)), key=lambda e: list(e.path))
    if case_errors:
        for err in case_errors:
            location = ".".join(str(x) for x in err.path) or "<root>"
            errors.append(f"{instance_path.name}:{location}: {err.message}")
    else:
        print(f"PASS {instance_path.relative_to(ROOT)}")

if errors:
    print("\n".join(f"FAIL {e}" for e in errors), file=sys.stderr)
    sys.exit(1)
