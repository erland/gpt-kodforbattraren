"""Side-effect-free reference routing for Kodförbättraren offline regression tests.

Not an MCP adapter and not a substitute for testing the model in a live host.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    status: str
    backend: str | None
    actions: tuple[str, ...]
    verification: str
    reason: str


def route(*, mode: str, local=False, github_ci=False, agent=False, agent_error=False,
          compatible=True, preview=False, browser=False, interactive=False,
          static_web=False, safe_public=False, artifact=False, url=False,
          required_browser=False, alternate_browser=False, may_defer=False) -> Decision:
    if mode not in {"zip", "github"}:
        raise ValueError("unsupported source mode")
    if mode == "github" and github_ci:
        backend, actions = "github_ci", ["github_ci_verify"]
    elif local:
        backend, actions = "local", ["local_verify"]
    elif agent and not agent_error and compatible:
        backend, actions = "agent_workspace", ["agent_workspace_verify"]
    else:
        reason = "backend_error" if agent_error else "unsupported_runtime" if agent and not compatible else "no_executor"
        if may_defer and not required_browser:
            return Decision("degraded", None, (), "deferred", reason)
        return Decision("blocked", None, (), "not_run", reason)

    if static_web and preview and artifact and safe_public:
        actions.append("preview_create")
    reachable = url or "preview_create" in actions
    interactive_possible = reachable and ((browser and interactive) or alternate_browser)
    if required_browser and not interactive_possible:
        if may_defer:
            return Decision("degraded", backend, tuple(actions), "deferred", "browser_gate_unavailable")
        return Decision("blocked", backend, tuple(actions), "not_run", "browser_gate_unavailable")
    if reachable:
        if browser and interactive:
            actions.append("browser_smoke")
        elif alternate_browser:
            actions.append("alternate_browser_smoke")
        elif browser:
            actions.append("visual_only")
    return Decision("selected", backend, tuple(actions), "planned_not_run", "route_selected")
