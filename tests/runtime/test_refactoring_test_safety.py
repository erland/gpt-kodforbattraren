from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_catalog():
    return yaml.safe_load((ROOT / "knowledge/refactoring-test-safety-catalog.yaml").read_text(encoding="utf-8"))


def test_safety_strategy_requires_baseline_and_regression_distinction():
    catalog = load_catalog()
    principles = catalog["principles"]
    assert principles["establish_baseline_before_risky_change"] is True
    assert principles["distinguish_existing_failures_from_regressions"] is True
    assert principles["verification_is_risk_based"] is True
    assert principles["do_not_weaken_tests_to_make_refactoring_pass"] is True


def test_baseline_can_represent_preexisting_failures():
    catalog = load_catalog()
    assert "green" in catalog["baseline_states"]
    assert "known_red" in catalog["baseline_states"]
    assert "unknown" in catalog["baseline_states"]
    assert catalog["preexisting_failures"]["rules"]


def test_high_risk_requires_stronger_safety_net_than_low_risk():
    catalog = load_catalog()
    low = catalog["risk_levels"]["low"]["expected_checks"]
    high = catalog["risk_levels"]["high"]["expected_checks"]
    assert "characterization_if_needed" in high
    assert "smaller_or_preparatory_step" in high
    assert len(high) > len(low)


def test_characterization_has_positive_and_negative_rules():
    characterization = load_catalog()["characterization"]
    assert characterization["use_when"]
    assert characterization["avoid_when"]
    assert characterization["rules"]


def test_stop_rollback_and_outcomes_are_explicit():
    catalog = load_catalog()
    assert len(catalog["stop_criteria"]) >= 5
    assert len(catalog["rollback_criteria"]) >= 3
    for expected in ["pass", "pass_with_known_red", "blocked", "rolled_back"]:
        assert expected in catalog["verification_outcomes"]


def test_reference_scenarios_cover_required_step8_cases():
    text = (ROOT / "tests/scenarios/refactoring-test-safety.md").read_text(encoding="utf-8")
    required = [
        "Projekt utan tester",
        "Projekt med befintliga fel",
        "Central affärslogik",
        "Rent kosmetisk förändring",
        "Test görs svagare för att få grönt",
        "Regression kan inte isoleras",
    ]
    for title in required:
        assert title in text
