#!/usr/bin/env python3
"""Check legacy CI baseline and migrated five-runtime release contract."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ci = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
release = (root / ".github/workflows/release.yml").read_text(encoding="utf-8")
errors = []
baseline = [
    "validate_project_status.py", "validate_runtime_models.py",
    "check_project_hygiene.py", "pytest -q -p no:cacheprovider tests/runtime",
    "validate_opencode_runtime.py", "validate_openai_plugin.py",
    "validate_runtime_parity.py", "validate_release_readiness.py",
    "validate_workflow_parity.py",
]
for token in baseline:
    if token not in ci:
        errors.append("CI missing baseline validation: " + token)

release_required = [
    "github.event.release.tag_name",
    "gpt-byggaren-chat-1.6.26.zip",
    "EXPECTED_SHA256",
    "prepare_builder_1626.py",
    "install_distribution_engine.py",
    "build_distributions.py",
    "validate_distributions.py",
    "build_optional_engine.py",
    "scripts/selftest.py",
    "validate_workflow_parity.py",
    "zipfile.ZipFile",
    "migration-artifacts/",
    "gh release upload",
]
for token in release_required:
    if token not in release:
        errors.append("Release missing canonical build step: " + token)
if "on:\n  release:" not in release or "types: [published]" not in release:
    errors.append("Release must publish on GitHub Release")
if "github.event_name == 'release'" not in release:
    errors.append("Release must scope upload to published releases")
if "kodforbattraren-custom-gpt-" in release:
    errors.append("Release must not publish retired Custom GPT")
if errors:
    print("WORKFLOW PARITY: FAIL")
    for error in errors:
        print("- " + error)
    raise SystemExit(1)
print("WORKFLOW PARITY: PASS (legacy CI baseline + canonical release)")
