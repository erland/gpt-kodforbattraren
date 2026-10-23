"""Offline companion routing matrix. No installed MCP endpoints are contacted."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from offline_companion_routing import route


def test_all_companions_zip():
    d = route(mode="zip", agent=True, preview=True, browser=True, interactive=True,
              static_web=True, safe_public=True, artifact=True)
    assert d.actions == ("agent_workspace_verify", "preview_create", "browser_smoke")
    assert d.verification == "planned_not_run"


def test_agent_absent_local():
    d = route(mode="zip", local=True)
    assert d.backend == "local" and d.actions == ("local_verify",)


def test_preview_absent():
    d = route(mode="zip", agent=True, browser=True, interactive=True, static_web=True, artifact=True)
    assert d.actions == ("agent_workspace_verify",)


def test_browser_absent():
    d = route(mode="zip", agent=True, preview=True, static_web=True, artifact=True, safe_public=True)
    assert d.actions == ("agent_workspace_verify", "preview_create")


def test_all_absent_defer():
    d = route(mode="zip", may_defer=True)
    assert (d.status, d.verification) == ("degraded", "deferred")


def test_all_absent_required_blocks():
    d = route(mode="zip")
    assert (d.status, d.verification) == ("blocked", "not_run")


def test_agent_backend_error_is_not_project_failure():
    d = route(mode="zip", agent=True, agent_error=True, may_defer=True)
    assert d.reason == "backend_error"
    assert d.verification == "deferred"


def test_agent_unsupported_runtime():
    d = route(mode="zip", agent=True, compatible=False)
    assert d.status == "blocked" and d.reason == "unsupported_runtime"


def test_github_ci_preferred_to_agent():
    d = route(mode="github", github_ci=True, agent=True)
    assert d.backend == "github_ci"
    assert "agent_workspace_verify" not in d.actions


def test_github_without_ci_can_use_agent():
    d = route(mode="github", agent=True)
    assert d.backend == "agent_workspace"


def test_browser_snapshot_only_is_visual_not_functional():
    d = route(mode="zip", local=True, browser=True, url=True)
    assert d.actions == ("local_verify", "visual_only")
    assert d.verification != "passed"


def test_required_browser_without_interaction_blocks():
    d = route(mode="zip", local=True, browser=True, url=True, required_browser=True)
    assert d.status == "blocked" and d.verification == "not_run"


def test_required_browser_alternative_runner():
    d = route(mode="zip", local=True, alternate_browser=True, url=True, required_browser=True)
    assert d.actions == ("local_verify", "alternate_browser_smoke")


def test_private_source_never_auto_published():
    d = route(mode="zip", agent=True, preview=True, static_web=True, artifact=True, safe_public=False)
    assert "preview_create" not in d.actions


def test_no_browser_without_url():
    d = route(mode="zip", local=True, browser=True, interactive=True)
    assert d.actions == ("local_verify",)


def test_no_live_mcp_dependencies():
    src = (Path(__file__).resolve().parents[2] / "scripts/offline_companion_routing.py").read_text()
    for forbidden in ("mcp__", "requests", "httpx", "urllib", "socket", "subprocess"):
        assert forbidden not in src
