#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
errors: list[str] = []

shared_markers = [
    "validate_project_status.py",
    "validate_runtime_models.py",
    "check_project_hygiene.py",
    "pytest -q -p no:cacheprovider tests/runtime",
    "build_distributions.py",
    "validate_opencode_runtime.py",
    "validate_runtime_parity.py",
    "validate_release_readiness.py",
]
for marker in shared_markers:
    if marker not in ci:
        errors.append(f"CI missing: {marker}")
    if marker not in release:
        errors.append(f"Release missing: {marker}")

for artifact in (
    "kodforbattraren-chat-",
    "kodforbattraren-custom-gpt-",
    "kodforbattraren-opencode-",
):
    if artifact not in release:
        errors.append(f"Release missing active artifact: {artifact}")

if "github.event.release.tag_name" not in release:
    errors.append("Release must derive version/ref from GitHub Release tag")
if "validate_workflow_parity.py" not in ci:
    errors.append("CI must enforce workflow parity")
if "validate_workflow_parity.py" not in release:
    errors.append("Release must enforce workflow parity")

if errors:
    print("WORKFLOW PARITY: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("WORKFLOW PARITY: PASS")
