from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("ghdec", ROOT / "scripts" / "github_pr_decision.py")
MOD = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

def test_first_pr():
    assert MOD.decide({}) == "create_first_pr"

def test_continue_open_pr():
    assert MOD.decide({"active_pr_state":"open","same_plan":True,"relevant_branch":True}) == "continue_open_pr"

def test_new_pr_after_merge():
    assert MOD.decide({"active_pr_state":"merged"}) == "create_new_pr_after_merge"

def test_closed_unmerged_blocks():
    assert MOD.decide({"active_pr_state":"closed"}) == "blocked_closed_unmerged"

def test_relevant_base_change_reanalysis():
    assert MOD.decide({"active_pr_state":"open","relevant_base_change":True}) == "reanalysis_required"

def test_conflict_blocks():
    assert MOD.decide({"active_pr_state":"open","conflict_or_unclear_divergence":True}) == "blocked_conflict_or_divergence"

def test_policy_has_safety_rules():
    t=(ROOT/"knowledge"/"github-pr-workflow.md").read_text(encoding="utf-8").lower()
    assert "pusha aldrig direkt till default branch" in t
    assert "merg:a inte pr automatiskt" in t
    assert "stängd men ej mergad" in t
