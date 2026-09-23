#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

REQUIRED = {
    "AGENTS.md",
    "README.md",
    "VERSION",
    "opencode.json",
    ".opencode/runtime-contract.json",
    ".opencode/skills/kodforbattraren/SKILL.md",
}

CORE_MARKERS = [
    "Förstå först, prioritera därefter",
    "Gör nästa steg",
    "Operativ kärna",
    "Auktoritativ status",
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
        missing = sorted(REQUIRED - names)
        if missing:
            errors.append(f"missing files: {missing}")
        bad = zf.testzip()
        if bad:
            errors.append(f"CRC error: {bad}")

        if "AGENTS.md" in names:
            agents = zf.read("AGENTS.md").decode("utf-8")
            for marker in CORE_MARKERS:
                if marker not in agents:
                    errors.append(f"AGENTS.md missing core marker: {marker}")

        if ".opencode/runtime-contract.json" in names:
            contract = json.loads(zf.read(".opencode/runtime-contract.json").decode("utf-8"))
            if contract.get("runtime_id") != "opencode":
                errors.append("runtime-contract has wrong runtime_id")
            adapter = contract.get("adapter", {})
            if adapter.get("mode") != "opencode_workspace":
                errors.append("runtime-contract has wrong adapter mode")
            if adapter.get("workspace_first") is not True:
                errors.append("OpenCode must be workspace_first")
            if adapter.get("local_scripts_are_runtime_tools") is not False:
                errors.append("scripts/ must not be declared as automatic runtime tools")

    if errors:
        print("OPENCODE RUNTIME VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OPENCODE RUNTIME VALIDATION: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
