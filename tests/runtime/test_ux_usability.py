from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def test_ux_knowledge_covers_core_dimensions():
    text = (ROOT / "knowledge" / "ux-usability.md").read_text(encoding="utf-8").lower()
    for term in ["navigation", "informationsarkitektur", "loading", "empty", "formulär",
                 "tillgänglighet", "mobil", "kognitiv", "refaktorering kontra ux-förändring",
                 "verifiering av ux-förändringar"]:
        assert term in text

def test_ux_change_is_not_hidden_as_refactoring():
    text = (ROOT / "knowledge" / "ux-usability.md").read_text(encoding="utf-8").lower()
    assert "`ux_change`" in text
    assert "observerbart användarbeteende ska vara oförändrat" in (
        ROOT / "knowledge" / "ux-usability-catalog.yaml"
    ).read_text(encoding="utf-8").lower()

def test_evidence_levels_are_explicit():
    data = yaml.safe_load((ROOT / "knowledge" / "ux-usability-catalog.yaml").read_text(encoding="utf-8"))
    assert data["evidence_levels"] == ["direct", "strong_inference", "hypothesis"]

def test_catalog_has_positive_and_avoidance_rules():
    data = yaml.safe_load((ROOT / "knowledge" / "ux-usability-catalog.yaml").read_text(encoding="utf-8"))
    assert len(data["heuristics"]) >= 10
    assert all(x.get("signals") and x.get("avoid") for x in data["heuristics"])

def test_scenarios_include_negative_case_and_behavior_split():
    text = (ROOT / "tests" / "scenarios" / "ux-usability.md").read_text(encoding="utf-8").lower()
    assert "ingen automatisk finding" in text
    assert "`refactoring`" in text
    assert "`ux_change`" in text
