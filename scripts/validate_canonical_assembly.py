#!/usr/bin/env python3
"""Validate that the pre-activation assembly preserves the canonical source."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "canonical/assembly.json").read_text(encoding="utf-8"))
assert manifest["status"] == "review_required"
assert manifest["legacy_instruction"] == "src/instructions/system.md"
assert manifest["sections"] == [{"owner": "core", "path": "src/instructions/system.md"}]
assert manifest["sources"] == {"core": manifest["legacy_instruction"]}
source = (root / manifest["legacy_instruction"]).read_bytes()
assembled = b"".join((root / section["path"]).read_bytes() for section in manifest["sections"])
assert source and source == assembled
assert (root / manifest["knowledge_root"]).is_dir()
assert (root / "src/conversation-starters/README.md").is_file()
print("PASS canonical assembly: byte-identical legacy instruction; skills not activated")
