"""Static offline guards for optional verification integration (no MCP calls)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "src/instructions/system.md"
POLICY = ROOT / "src/runtime-policy/optional-companion-verification-policy.md"


def test_critical_rules_in_canonical_instruction():
    text = CORE.read_text(encoding="utf-8")
    for clause in (
        "Agent Workspace, PWA Preview och Browser Screenshot är valfria",
        "GitHub får inte bli ett krav i ZIP-läge",
        "screenshot ensam är aldrig ett funktionstest",
        "baseline före ändring och regression efter ändring",
        "completion-blocking test får aldrig rapporteras som PASS",
    ):
        assert clause in text


def test_fallback_and_runtime_gates():
    text = POLICY.read_text(encoding="utf-8")
    for clause in (
        "available", "unavailable", "unknown", "backend_error",
        "repository CI", "Agent Workspace", "PWA Preview",
        "Browser Screenshot", "file_read", "signed artifact download",
        "full Playwright/E2E parity", "No live service calls",
    ):
        assert clause in text


def test_workflow_references_policy():
    text = (ROOT / "src/runtime-policy/operational-execution-policy.md").read_text(encoding="utf-8")
    assert "optional-companion-verification-policy.md" in text
