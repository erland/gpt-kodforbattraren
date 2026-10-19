#!/usr/bin/env python3
"""Ensure the optional Engine fallback survives canonical modular assembly."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
canonical = (root / "src/instructions/system.md").read_text(encoding="utf-8")
manifest = json.loads((root / "canonical/modular-assembly.json").read_text(encoding="utf-8"))
core = (root / manifest["sources"]["core"]).read_text(encoding="utf-8")
checks = (
    "kodforbattraren-engine-<version>.zip",
    "python scripts/selftest.py",
    "MCP",
    "Python 3",
    "analys och planering",
    "kontrollsummor",
)
missing = [token for token in checks if token not in canonical or token not in core]
if manifest.get("status") != "modular":
    missing.append("modular source manifest")
if "Valfri deterministisk Engine ZIP" not in core:
    missing.append("Engine fallback section must be in shared core")
if missing:
    raise SystemExit("FAIL canonical Engine fallback: " + ", ".join(missing))
print("PASS canonical Engine fallback in shared modular core")
