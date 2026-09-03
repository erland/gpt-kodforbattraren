from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]

def module():
    spec = importlib.util.spec_from_file_location("build_distributions", ROOT/"scripts"/"build_distributions.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod

def test_normalize_release_tag():
    mod = module()
    assert mod.normalize_version("v1.2.3") == "1.2.3"
    assert mod.normalize_version("refs/tags/v1.2.3") == "1.2.3"

def test_rejects_unsafe_version():
    mod = module()
    try:
        mod.normalize_version("../bad")
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe version accepted")

def test_custom_compilation_is_within_platform_limits():
    custom = ROOT/"src"/"custom-gpt"
    instruction = (custom/"INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert len(instruction) <= 8000
    assert len([p for p in (custom/"knowledge").iterdir() if p.is_file()]) <= 20


def test_custom_source_is_not_inside_ignored_dist():
    custom = ROOT / "src" / "custom-gpt"
    assert custom.exists()
    assert "dist" not in custom.relative_to(ROOT).parts

def test_build_script_uses_canonical_custom_source():
    text = (ROOT/"scripts"/"build_distributions.py").read_text(encoding="utf-8")
    assert 'ROOT / "src/custom-gpt"' in text
    assert 'ROOT / "dist/custom-gpt"' not in text


def test_runtime_ignore_filters_cache_and_bytecode():
    mod = module()
    ignored = mod.runtime_ignore("x", ["__pycache__", ".pytest_cache", "a.pyc", "keep.py"])
    assert "__pycache__" in ignored
    assert ".pytest_cache" in ignored
    assert "a.pyc" in ignored
    assert "keep.py" not in ignored
