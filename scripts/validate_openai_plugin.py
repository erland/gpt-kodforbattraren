#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

EXPECTED_SCRIPTS = {
    "derive_next_step.py",
    "detect_technology_profiles.py",
    "generate_refactoring_plan.py",
    "github_pr_decision.py",
    "interpret_progress_command.py",
    "zip_work_status.py",
    "zip_workspace.py",
}

FORBIDDEN_SCRIPTS = {
    "build_distributions.py",
    "validate_runtime_parity.py",
    "validate_release_readiness.py",
    "validate_workflow_parity.py",
    "validate_project_status.py",
    "validate_runtime_models.py",
    "check_project_hygiene.py",
    "validate_opencode_runtime.py",
}

CORE_MARKERS = [
    "Förstå först, prioritera därefter",
    "Gör nästa steg",
    "Operativ kärna",
    "Auktoritativ status",
    "komplett uppdaterad projekt-ZIP",
    "GitHub-läge",
]

PLUGIN_MARKERS = [
    "Samtalsminne ersätter aldrig workspace-state",
    "Ändra inte kod utan writable workspace",
    "Markera aldrig ett implementeringssteg verifierat",
    "kräver branch/commit/PR en faktisk auktoriserad GitHub-capability",
    "kräver ingen MCP-wrapper",
]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True)
    args = parser.parse_args()

    path = Path(args.zip)
    errors: list[str] = []
    if not path.is_file():
        print(f"ERROR missing ZIP: {path}")
        return 1

    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        required = {
            "plugin.json",
            "runtime-contract.json",
            "README.md",
            "VERSION",
            "skills/kodforbattraren/SKILL.md",
            "skills/kodforbattraren/references/runtime-policy/operational-execution-policy.md",
            "skills/kodforbattraren/references/knowledge/zip-workflow-policy.yaml",
            "skills/kodforbattraren/references/knowledge/github-pr-workflow-policy.yaml",
            "skills/kodforbattraren/references/schemas/work-status.schema.json",
            "skills/kodforbattraren/references/schemas/refactoring-plan.schema.json",
        }
        missing = sorted(required - names)
        if missing:
            errors.append(f"missing files: {missing}")
        bad = zf.testzip()
        if bad:
            errors.append(f"CRC error: {bad}")

        if "plugin.json" in names:
            plugin = json.loads(zf.read("plugin.json").decode("utf-8"))
            if plugin.get("name") != "kodforbattraren":
                errors.append("plugin name mismatch")

        if "runtime-contract.json" in names:
            contract = json.loads(zf.read("runtime-contract.json").decode("utf-8"))
            if contract.get("runtime_id") != "openai_plugin":
                errors.append("runtime-contract has wrong runtime_id")
            adapter = contract.get("adapter", {})
            if adapter.get("mode") != "openai_plugin":
                errors.append("runtime-contract has wrong adapter mode")
            if adapter.get("skills_first") is not True:
                errors.append("Plugin must be skills-first")
            if adapter.get("workspace_first") is not True:
                errors.append("Plugin must be workspace-first")
            if adapter.get("state_authority") != "workspace_file":
                errors.append("workspace file must remain state authority")
            if adapter.get("state_path") != "project-status.yaml":
                errors.append("wrong state path")
            if adapter.get("local_scripts_are_runtime_tools") is not False:
                errors.append("support scripts must not become canonical runtime tools")
            resources = adapter.get("script_resources", {})
            if set(resources.get("packaged", [])) != EXPECTED_SCRIPTS:
                errors.append("runtime support script list differs")
            if resources.get("mcp_required_for_resource_use") is not False:
                errors.append("script resources must not require MCP")
            fallback = adapter.get("fallback_policy", {})
            if fallback.get("without_shell_or_code_execution") != "do_not_mark_implementation_verified":
                errors.append("verification fallback weakened")
            if fallback.get("without_github_write") != "github_read_only_or_zip_mode":
                errors.append("GitHub fallback weakened")
            if fallback.get("without_archive_output") != "do_not_claim_updated_zip_delivered":
                errors.append("ZIP delivery fallback weakened")
            if contract.get("tools", {}).get("tools") != []:
                errors.append("canonical tools contract must remain empty")

        if "skills/kodforbattraren/SKILL.md" in names:
            skill = zf.read("skills/kodforbattraren/SKILL.md").decode("utf-8")
            for marker in CORE_MARKERS + PLUGIN_MARKERS:
                if marker not in skill:
                    errors.append(f"SKILL.md missing marker: {marker}")

        actual_scripts = {
            Path(name).name
            for name in names
            if name.startswith("skills/kodforbattraren/scripts/") and name.endswith(".py")
        }
        if actual_scripts != EXPECTED_SCRIPTS:
            errors.append(f"Plugin support scripts differ: {sorted(actual_scripts)}")
        if actual_scripts & FORBIDDEN_SCRIPTS:
            errors.append(f"development scripts leaked into Plugin: {sorted(actual_scripts & FORBIDDEN_SCRIPTS)}")

    if errors:
        print("OPENAI PLUGIN VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OPENAI PLUGIN VALIDATION: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
