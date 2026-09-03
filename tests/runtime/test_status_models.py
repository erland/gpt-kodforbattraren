from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("derive_next_step", ROOT / "scripts/derive_next_step.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

def load(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))

def test_zip_status_derives_r002_without_conversation_history():
    plan = load("schemas/examples/refactoring-plan.yaml")
    status = load("schemas/examples/work-status-zip.yaml")
    assert MOD.derive(plan, status) == {
        "state": "ready",
        "step_id": "R-002",
        "title": "Separera persistence från OrderService",
    }

def test_github_status_continues_open_current_step():
    plan = load("schemas/examples/refactoring-plan.yaml")
    status = load("schemas/examples/work-status-github.yaml")
    assert MOD.derive(plan, status) == {
        "state": "continue",
        "step_id": "R-002",
        "title": "Separera persistence från OrderService",
    }
