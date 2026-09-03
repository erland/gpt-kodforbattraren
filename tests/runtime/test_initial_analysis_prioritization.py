from pathlib import Path
import json
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def test_analysis_knowledge_covers_required_deliverables():
    text = (ROOT / "knowledge" / "initial-analysis-prioritization.md").read_text(encoding="utf-8").lower()
    for term in [
        "inventering av projektstruktur", "findings måste ha evidens", "severity",
        "change risk", "expected benefit", "effort", "beroenden mellan åtgärder",
        "medvetet inte åtgärda", "diagnostisk baseline", "developer_experience"
    ]:
        assert term in text


def test_catalog_has_contextual_prioritization_and_non_actions():
    data = yaml.safe_load((ROOT / "knowledge" / "initial-analysis-prioritization-catalog.yaml").read_text(encoding="utf-8"))
    assert "severity" in data["prioritization_dimensions"]
    assert "change_risk" in data["prioritization_dimensions"]
    assert "expected_benefit" in data["prioritization_dimensions"]
    rules = {r["id"]: r for r in data["rules"]}
    assert "ANA-003" in rules
    assert "ANA-006" in rules
    assert data["analysis_mode"] == "read_only_product_source"


def test_analysis_report_schema_is_valid_and_has_baseline():
    schema = json.loads((ROOT / "schemas" / "analysis-report.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    required = set(schema["properties"]["baseline"]["required"])
    assert {"maintainability", "architecture", "testability", "developer_experience", "usability", "accessibility"} <= required


def test_scenarios_cover_small_large_backend_frontend_fullstack_and_no_overrefactoring():
    text = (ROOT / "tests" / "scenarios" / "initial-analysis-prioritization.md").read_text(encoding="utf-8").lower()
    for term in ["litet backend", "stort monorepo", "frontend", "fullstack", "non-action"]:
        assert term in text
    assert "ändra inte produktionskoden" in text
