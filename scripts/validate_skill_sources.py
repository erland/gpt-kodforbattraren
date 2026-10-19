#!/usr/bin/env python3
"""Check migration Skills without activating new runtime adapters."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
canonical = root / "src/instructions/system.md"
assert canonical.is_file()
original = canonical.read_text(encoding="utf-8")
assert "Förstå först, prioritera därefter" in original
names = ("kodanalys", "refaktorering", "leverans-och-status")
for name in names:
    path = root / "skills" / name / "SKILL.md"
    value = path.read_text(encoding="utf-8")
    assert value.startswith("---\n"), path
    assert re.search(r"(?m)^name: " + re.escape(name) + r"$", value), path
    assert "src/instructions/system.md" in value, path
    for ref in re.findall(r"`(knowledge/[^\x60]+\.md)`", value):
        assert (root / ref).is_file(), f"missing {ref} from {path}"
    assert len(value.strip()) > 300
print("PASS skill source references: 3 skills; canonical remains authoritative")
