from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_catalog():
    return yaml.safe_load((ROOT / "knowledge/architecture-pattern-catalog.yaml").read_text(encoding="utf-8"))


def test_problem_before_pattern_and_solid_not_dogma():
    catalog = load_catalog()
    assert catalog["principles"]["problem_before_pattern"] is True
    assert catalog["principles"]["solid_is_heuristic"] is True
    assert catalog["principles"]["prefer_minimum_sufficient_structure"] is True
    assert catalog["principles"]["remove_patterns_when_cost_exceeds_value"] is True


def test_pattern_catalog_has_tradeoffs_not_just_names():
    patterns = load_catalog()["patterns"]
    assert len(patterns) >= 10
    assert len({p["id"] for p in patterns}) == len(patterns)
    for pattern in patterns:
        assert pattern["useful_when"], pattern["id"]
        assert pattern["avoid_when"], pattern["id"]


def test_catalog_covers_required_step7_topics():
    names = {p["name"] for p in load_catalog()["patterns"]}
    for expected in ["Ports and Adapters", "Strategy", "State", "Repository", "Adapter", "Facade"]:
        assert expected in names


def test_reference_scenarios_cover_required_step7_cases():
    text = (ROOT / "tests/scenarios/architecture-patterns.md").read_text(encoding="utf-8")
    required = [
        "Strategy är motiverat",
        "Strategy är onödigt",
        "Befintligt Repository bör förenklas",
        "Ports and Adapters delvis, inte överallt",
        "Pattern tas bort när variationspunkten försvunnit",
    ]
    for title in required:
        assert title in text
