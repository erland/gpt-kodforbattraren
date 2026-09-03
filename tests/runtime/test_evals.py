from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

def load():
    return json.loads((ROOT/"evals"/"e2e-cases.json").read_text(encoding="utf-8"))

def test_eval_suite_has_required_cases():
    ids = {c["id"] for c in load()["cases"]}
    assert ids == {f"E2E-{i:02d}" for i in range(1,17)}

def test_eval_suite_covers_zip_and_github():
    modes = {c["mode"] for c in load()["cases"]}
    assert "zip" in modes
    assert "github" in modes

def test_eval_suite_contains_negative_controls():
    data = load()
    all_forbidden = {x for c in data["cases"] for x in c["must_not"]}
    for item in ["size_only","pattern_for_pattern_sake","advance_next","invent_work","duplicate_pr"]:
        assert item in all_forbidden

def test_eval_suite_covers_regression_and_resume():
    by_id = {c["id"]: c for c in load()["cases"]}
    assert "block_or_rollback" in by_id["E2E-07"]["must"]
    assert "resume_state" in by_id["E2E-08"]["must"]
    assert "reanalysis_required" in by_id["E2E-09"]["must"]

def test_eval_suite_covers_pr_lifecycle():
    by_id = {c["id"]: c for c in load()["cases"]}
    assert "continue_open_pr" in by_id["E2E-10"]["must"]
    assert "new_branch_after_merge" in by_id["E2E-11"]["must"]
    assert "blocked_closed_unmerged" in by_id["E2E-12"]["must"]

def test_eval_rubric_has_thresholds_and_critical_failures():
    text=(ROOT/"evals"/"scoring-rubric.md").read_text(encoding="utf-8").lower()
    assert "16/20" in text
    assert "18/20" in text
    assert "kritiskt kontraktsbrott" in text
