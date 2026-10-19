#!/usr/bin/env python3
"""Smoke tests for non-generic Python identification."""
import importlib.util
import tempfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("detect",root/"scripts/detect_technology_profiles.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)
    (p/"sample.py").write_text("def main(): pass\n",encoding="utf-8")
    profiles,evidence=module.detect(p)
    assert "python" in profiles and "generic-backend-web" not in profiles,(profiles,evidence)
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)
    (p/"pyproject.toml").write_text("[project]\nname = 'test'\n",encoding="utf-8")
    profiles,_=module.detect(p)
    assert "python" in profiles, profiles
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)
    profiles,_=module.detect(p)
    assert profiles==["generic-backend-web"],profiles
print("PASS Python profile classification: script, pyproject, empty")
