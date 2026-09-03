from copy import deepcopy
from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[2]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

planner = load_module("planner", ROOT / "scripts" / "generate_refactoring_plan.py")
nextstep = load_module("nextstep", ROOT / "scripts" / "derive_next_step.py")

class Args:
    plan_id="test-plan"; project_name="Demo"; mode="zip"; base_identifier="abc123"; repository=None; captured_at="2026-09-03T12:00:00+00:00"

def fixture_plan():
    analysis = yaml.safe_load((ROOT/"tests/fixtures/planning/analysis.yaml").read_text())
    findings = planner.load_findings(ROOT/"tests/fixtures/planning/findings")
    return planner.build_plan(analysis, findings, Args)[0], analysis

def status_for(plan, current=None):
    return {
      "progress": {"current_step_id": current, "completed_step_ids": [], "skipped_step_ids": [], "blocked_step_ids": []},
      "blockers": [],
      "delivery": {"verification_status": "not_run"}
    }

def test_plan_adds_guard_before_high_risk_change_and_maps_dependencies():
    plan, _ = fixture_plan()
    assert plan["steps"][0]["title"].startswith("Etablera testskydd")
    ids = {s["finding_ids"][0]: s["id"] for s in plan["steps"] if len(s["finding_ids"]) == 1 and s["title"] != "Etablera testskydd för riskfyllda förändringar"}
    f2 = next(s for s in plan["steps"] if s["finding_ids"] == ["F-002"])
    assert ids["F-001"] in f2["depends_on"]

def test_gor_nasta_steg_returns_first_ready_step():
    plan, _ = fixture_plan(); result = nextstep.derive(plan, status_for(plan))
    assert result["state"] == "ready" and result["step_id"] == "R-001"

def test_failed_verification_does_not_advance():
    plan, _ = fixture_plan(); st = status_for(plan, "R-001"); st["delivery"]["verification_status"] = "failed"
    result = nextstep.derive(plan, st)
    assert result["state"] == "blocked" and result["reason"] == "verification_failed"

def test_new_blocker_prevents_current_step():
    plan, _ = fixture_plan(); st = status_for(plan, "R-001"); st["blockers"]=[{"id":"B-1","status":"open","step_id":"R-001","description":"Ny blockerare"}]
    result = nextstep.derive(plan, st)
    assert result["state"] == "blocked" and result["step_id"] == "R-001"

def test_completed_step_advances_to_next_runnable():
    plan, _ = fixture_plan(); st = status_for(plan); st["progress"]["completed_step_ids"]=["R-001"]
    result = nextstep.derive(plan, st)
    assert result["state"] == "ready" and result["step_id"] == "R-002"

def test_source_drift_requires_reanalysis():
    plan, _ = fixture_plan(); result = nextstep.derive(plan, status_for(plan), "different")
    assert result["state"] == "reanalysis_required" and result["reason"] == "source_drift"

def test_markdown_contains_steps_mapping_and_non_actions():
    plan, analysis = fixture_plan()
    _, mapping = planner.build_plan(analysis, planner.load_findings(ROOT/"tests/fixtures/planning/findings"), Args)
    md = planner.render_markdown(plan, mapping, analysis)
    assert "## Finding → steg" in md and "## Medvetna non-actions" in md and "R-001" in md
