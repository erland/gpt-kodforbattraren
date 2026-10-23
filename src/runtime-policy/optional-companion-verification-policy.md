# Optional companion verification policy

## Discovery and routing
Determine capabilities from the *current* host/tool results, not historic availability. Companion services Agent Workspace, PWA Preview and Browser Screenshot are all optional. Distinguish **available**, **unavailable**, **unknown** and **backend_error**; do not substitute an imagined tool call.

For GitHub source mode, prefer repository CI when it provides sufficient required checks, preserving branch/PR source authority. For ZIP mode, prefer working host-local execution; if inadequate, use compatible Agent Workspace before asking the user to run tests locally. Never make GitHub a condition for ZIP work. When no safe executor exists, continue read-only analysis/planning or explicitly defer only non-blocking checks; do not mark a required blocking gate complete.

## Refactoring baseline and evidence
Before risky behavior-preserving refactoring, record relevant test command, baseline result, known pre-existing failures and source identity. Afterwards run equivalent focused regression checks against modified source and distinguish regressions from known red tests. Report PASS only for tests actually executed. Timeout/connection/tool failures are environment limitations, not code-test failures.

## Agent Workspace
Probe live profile/capabilities. Respect reported npm/Maven and runtime support; other stacks require separate compatible execution. Review untrusted ZIP safely; do not upload secrets or confidential source without authorization. Prefer verify for tests, build for necessary artifact outputs. Read logs through file_read; prefer short-lived signed artifact download links rather than file materialization. Destroy short-lived workspace even following failures.

## PWA Preview and Browser Screenshot
PWA Preview is appropriate only for safe-to-expose, prebuilt static web artifacts. Preview READY does not establish functional correctness. Browser Screenshot may provide visual-only capture, or interactive session/navigate/snapshot/fill/click if those features are confirmed live. An actual observed click/fill/assertion supports only that focused browser smoke path, not full Playwright/E2E parity, PWA offline behavior or accessibility. Do not create unnecessary previews or screenshots.

## Fallback and safety
Never require any companion plugin, nor auto-retry expensive or potentially unsafe operations indefinitely. No live service calls in offline capability-routing regression tests. Persist provenance (source revision/hash, test command, backend, outcome), classify unavailable/deferred explicitly and keep production/release safety gates intact.
