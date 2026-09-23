from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]

def module():
    spec = importlib.util.spec_from_file_location("build_distributions", ROOT/"scripts"/"build_distributions.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod

def test_builder_defines_opencode_distribution():
    mod = module()
    assert hasattr(mod, "build_opencode")

def test_project_registers_opencode_as_active_ready_runtime():
    import yaml
    cfg = yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    candidates = {x["runtime_id"]: x for x in cfg["analysis"]["runtime"]["candidates"]}
    assert candidates["opencode"]["suitability"] == "ready"
    assert candidates["opencode"]["activate_by_default"] is True
    assert cfg["build"]["build_opencode_zip"] is True

def test_opencode_builder_is_workspace_first_and_does_not_promote_scripts_to_tools():
    text = (ROOT/"scripts"/"build_distributions.py").read_text(encoding="utf-8")
    assert '"mode": "opencode_workspace"' in text
    assert '"workspace_first": True' in text
    assert '"local_scripts_are_runtime_tools": False' in text
