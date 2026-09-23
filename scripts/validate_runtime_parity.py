#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_RUNTIMES = {
    "chatgpt_chat",
    "chatgpt_custom",
    "claude_project",
    "opencode",
    "openai_plugin",
}
EXPECTED_CATEGORIES = {
    "behavior",
    "capability",
    "artifact",
    "workspace_state",
    "tool",
}

errors: list[str] = []

def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
parity = cfg.get("runtime_parity", {})
registered = set(parity.get("registered_runtimes", []))
categories = set(parity.get("compared_categories", []))

check(registered == EXPECTED_RUNTIMES, f"registered runtimes differ: {sorted(registered)}")
check(categories == EXPECTED_CATEGORIES, f"parity categories differ: {sorted(categories)}")

candidates = {
    item.get("runtime_id"): item
    for item in cfg.get("analysis", {}).get("runtime", {}).get("candidates", [])
    if isinstance(item, dict) and item.get("runtime_id")
}
check(set(candidates) == EXPECTED_RUNTIMES, "all five runtimes must have explicit assessment")

for runtime_id in EXPECTED_RUNTIMES:
    item = candidates.get(runtime_id, {})
    check(item.get("suitability") in {"ready", "reduced", "not_viable"}, f"{runtime_id} invalid suitability")
    check(bool(item.get("reason")), f"{runtime_id} missing reason")

for runtime_id in ("chatgpt_chat", "chatgpt_custom", "opencode"):
    check(candidates.get(runtime_id, {}).get("activate_by_default") is True, f"{runtime_id} must be active")
for runtime_id in ("claude_project", "openai_plugin"):
    item = candidates.get(runtime_id, {})
    check(item.get("activate_by_default") is False, f"{runtime_id} must remain inactive")
    check(item.get("suitability") == "reduced", f"{runtime_id} must be reduced")

active_contracts = [
    (ROOT / "dist" / ".staging" / "chat" / "assistant" / "runtime-contract.json", "chatgpt_chat"),
    (ROOT / "dist" / ".staging" / "custom-gpt" / "runtime-contract.json", "chatgpt_custom"),
    (ROOT / "dist" / ".staging" / "opencode" / ".opencode" / "runtime-contract.json", "opencode"),
]
# Build script cleans staging after completion, so validate directly from ZIPs when staging is absent.
zip_patterns = {
    "chatgpt_chat": "kodforbattraren-chat-*.zip",
    "chatgpt_custom": "kodforbattraren-custom-gpt-*.zip",
    "opencode": "kodforbattraren-opencode-*.zip",
}

import zipfile

for _, runtime_id in active_contracts:
    matches = sorted((ROOT / "dist").glob(zip_patterns[runtime_id]))
    if not matches:
        errors.append(f"missing built ZIP for {runtime_id}")
        continue
    path = matches[-1]
    with zipfile.ZipFile(path) as zf:
        contract_name = {
            "chatgpt_chat": "assistant/runtime-contract.json",
            "chatgpt_custom": "runtime-contract.json",
            "opencode": ".opencode/runtime-contract.json",
        }[runtime_id]
        if contract_name not in zf.namelist():
            errors.append(f"{runtime_id} missing runtime contract")
            continue
        payload = json.loads(zf.read(contract_name).decode("utf-8"))
        check(payload.get("runtime_id") == runtime_id, f"{runtime_id} wrong runtime_id")
        for key in ("capabilities", "artifacts", "workspace_state", "tools"):
            check(payload.get(key) == cfg.get(key), f"{runtime_id} {key} contract drift")

# Core behavior parity across active instructions.
core_markers = list(cfg.get("instructions", {}).get("core_contract", {}).get("required_markers", []))
instructions = {}
for runtime_id, pattern, name in (
    ("chatgpt_chat", "kodforbattraren-chat-*.zip", "assistant/instructions.md"),
    ("chatgpt_custom", "kodforbattraren-custom-gpt-*.zip", "INSTRUCTIONS.md"),
    ("opencode", "kodforbattraren-opencode-*.zip", "AGENTS.md"),
):
    matches = sorted((ROOT / "dist").glob(pattern))
    if matches:
        with zipfile.ZipFile(matches[-1]) as zf:
            if name in zf.namelist():
                instructions[runtime_id] = zf.read(name).decode("utf-8")

for runtime_id in ("chatgpt_chat", "chatgpt_custom", "opencode"):
    text = instructions.get(runtime_id, "")
    for marker in core_markers:
        check(marker.lower() in text.lower(), f"{runtime_id} missing core marker: {marker}")

report = {
    "result": "PASS" if not errors else "FAIL",
    "registered_runtimes": sorted(registered),
    "compared_categories": sorted(categories),
    "active_runtimes": ["chatgpt_chat", "chatgpt_custom", "opencode"],
    "inactive_runtimes": ["claude_project", "openai_plugin"],
    "errors": errors,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
