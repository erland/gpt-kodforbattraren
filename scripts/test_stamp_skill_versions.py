#!/usr/bin/env python3
"""Regression tests for release Skill frontmatter stamping."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("stamp", Path(__file__).with_name("stamp_skill_versions.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def check(source, version):
    result = module.stamp(source, version)
    assert result.startswith("---\n"), result
    assert result.count("\n---\n") == 1, result
    assert result.count("metadata:") == 1, result
    assert f'  version: "{version}"' in result, result
    assert "\\n" not in result.split("---", 2)[1], result
    assert module.stamp(result, version) == result, "Stamping must be idempotent"
    return result

check('---\nname: test\nmetadata:\n  version: "1.3.1"\n---\n\n# Body\n', "1.3.3")
check('---\nname: test\nmetadata:\n  category: quality\n---\n\n# Body\n', "1.3.3")
check('---\nname: test\n---\n\n# Body\n', "1.3.3")
check('# Body\n', "1.3.3")
print("PASS: Skill frontmatter stamping and idempotency")
