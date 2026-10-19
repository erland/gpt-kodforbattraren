#!/usr/bin/env python3
"""Prevent divergence between canonical Engine fallback and distributed runtime instructions."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
canonical = (root / "src/instructions/system.md").read_text(encoding="utf-8")
skill_source = (root / "src/instructions/skills/leverans-och-status/behavior.md").read_text(encoding="utf-8")
checks = (
    "kodforbattraren-engine-<version>.zip",
    "python scripts/selftest.py",
    "MCP",
    "Python 3",
    "analys och planering",
    "kontrollsummor",
)
missing = [token for token in checks if token not in canonical]
if "src/instructions/system.md" not in skill_source:
    missing.append("skill source must reference canonical instruction")
if missing:
    raise SystemExit("FAIL canonical Engine fallback: " + ", ".join(missing))
print("PASS canonical Engine fallback and skill source link")
