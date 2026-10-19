#!/usr/bin/env python3
"""Ensure modular Skill sources preserve every legacy canonical section exactly."""
import json
import re
from pathlib import Path

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/"canonical/modular-assembly.json").read_text(encoding="utf-8"))
original=(root/manifest["legacy_instruction"]).read_text(encoding="utf-8")
sources=manifest["sources"]
parts={}
header=""
for owner,rel in sources.items():
    content=(root/rel).read_text(encoding="utf-8")
    matches=list(re.finditer(r"^## (.+)$",content,re.M))
    if owner=="core":
        header=content[:matches[0].start()]
    parts[owner]={match.group(1):content[match.start():matches[i+1].start() if i+1<len(matches) else None] for i,match in enumerate(matches)}
expected=header+"".join(parts[s["owner"]][s["title"]] for s in manifest["sections"])
assert expected==original, "Modular assembly does not match original canonical instruction byte-for-byte"
assert sum(map(len,parts.values()))==len(manifest["sections"])
assert len(sources)==4
print("PASS modular assembly: canonical behavior preserved across three distinct skills")
