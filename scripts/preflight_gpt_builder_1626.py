#!/usr/bin/env python3
"""Read-only preflight for migration to GPT Byggaren 1.6.26.

Run in the project root: python scripts/preflight_gpt_builder_1626.py
Does not mutate gpt-project.yaml, active runtimes or distribution scripts.
"""
from pathlib import Path
import json
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML required (pip install -r requirements-ci.txt)")

ROOT = Path(__file__).resolve().parents[1]
cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
required_targets = {"chat", "plugin", "claude_project", "claude_skills", "opencode"}
issues = []
build = cfg.get("build_system", {})
targets = build.get("runtime_targets", {})
if not isinstance(targets, dict):
    issues.append("build_system.runtime_targets must be a mapping")
else:
    missing = required_targets - set(targets)
    if missing:
        issues.append("Missing runtime targets: " + ", ".join(sorted(missing)))
if set(build.get("targets", [])) != required_targets | {"project"}:
    issues.append("build_system.targets must contain project and five runtimes")
runtime = cfg.get("runtime", {})
for key in ("chat_zip", "plugin", "claude", "opencode", "custom_gpt"):
    if not isinstance(runtime.get(key), dict):
        issues.append("Missing runtime." + key)
if runtime.get("custom_gpt", {}).get("enabled") is not False:
    issues.append("Custom GPT must be disabled in migrated build configuration")
if runtime.get("openai_plugin", {}).get("enabled"):
    issues.append("Legacy runtime.openai_plugin remains enabled; explicit mapping required")
if runtime.get("plugin", {}).get("enabled"):
    issues.append("Plugin host persistent workspace, execution and Skills import not yet verified")
if not isinstance(cfg.get("structure"), dict):
    issues.append("Canonical builder requires structure.conversation_starters, absent in legacy project")
if not (ROOT / "canonical" / "assembly.json").exists():
    issues.append("Canonical assembly.json absent: skill source ownership must be reviewed")
for entry in runtime.get("opencode", {}).get("skills", {}).get("definitions", []):
    for rel in entry.get("references", []):
        if not (ROOT / rel).is_file():
            issues.append("OpenCode skill missing resource: " + rel)
report = {
    "schema_version": 1,
    "status": "ready_for_build" if not issues else "review_required",
    "issues": issues,
    "read_only": True,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(0 if not issues else 2)
