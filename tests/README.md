# Tester

Projektets tester och beteendescenarier.

- `scenarios/canonical-behavior.md` – scenarios för det obligatoriska canonical beteendekontraktet.
- `scenarios/code-quality-heuristics.md` – referensfall för steg 6, inklusive positiva och negativa fall för stora enheter, duplicering, SoC, testbarhet och överdesign.
- `runtime/test_status_models.py` – deterministisk nästa-steg-härledning från plan + status.
- `runtime/test_heuristic_catalog.py` – strukturell kontroll av heuristic-katalogen och dess anti-mekaniska egenskaper.

Senare steg kompletterar dessa med arkitektur/design-patterns, teststrategi, UX och runtime-evals.

## Steg 8

- `runtime/test_refactoring_test_safety.py` validerar baseline, risknivåer, characterization tests samt stopp/rollback.
- `scenarios/refactoring-test-safety.md` innehåller positiva och negativa referensfall för säker refaktorering.
