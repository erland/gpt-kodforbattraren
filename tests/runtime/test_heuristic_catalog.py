from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_catalog():
    return yaml.safe_load((ROOT / "knowledge/code-quality-heuristic-catalog.yaml").read_text(encoding="utf-8"))


def test_catalog_has_unique_contiguous_ids_and_no_mechanical_thresholds():
    catalog = load_catalog()
    heuristics = catalog["heuristics"]
    ids = [h["id"] for h in heuristics]
    assert ids == [f"CQ-{i:02d}" for i in range(1, 17)]
    assert len(ids) == len(set(ids))
    assert all(h["mechanical_threshold"] is False for h in heuristics)


def test_every_heuristic_has_positive_and_counter_signals():
    for heuristic in load_catalog()["heuristics"]:
        assert heuristic["positive_signals"], heuristic["id"]
        assert heuristic["counter_signals"], heuristic["id"]
        assert heuristic["requires_context"] is True


def test_reference_scenarios_cover_required_step6_cases():
    text = (ROOT / "tests/scenarios/code-quality-heuristics.md").read_text(encoding="utf-8")
    required = [
        "Stor fil med flera ansvar bör delas",
        "Stor sammanhållen fil lämnas orörd",
        "Duplicerad affärsregel centraliseras",
        "Persistence läcker in i domänlogik",
        "Stabil legacy lämnas orörd",
    ]
    for title in required:
        assert title in text
