# Schemas

Kodförbättrarens runtime använder tre canonical modeller för längre förbättringsserier:

- `finding.schema.json` – ett konkret problem eller förbättringsmöjlighet, med evidens, prioritet, status och koppling till åtgärdssteg.
- `refactoring-plan.schema.json` – den ordnade genomförandeplanen med beroenden, klart-kriterier, verifiering och klassificering av beteendeförändring.
- `work-status.schema.json` – faktisk arbetsstatus mellan körningar, inklusive genomförda/blockerade steg, finding-status, planändringar och aktuellt ZIP- eller GitHub/PR-läge.

`schemas/examples/` innehåller validerbara exempel för båda källägena.

## Viktiga invariants

1. Finding-id använder `F-NNN`; plansteg använder `R-NNN`.
2. Ett finding kan kopplas till noll eller flera plansteg, och ett plansteg kan hantera flera findings.
3. Stegstatus skiljer `planned`, `ready`, `in_progress`, `completed`, `blocked` och `skipped`.
4. Work status är sanningen om faktisk progress; samtalshistorik får inte användas som enda källa.
5. `source.mode` är antingen `zip` eller `github`. ZIP lagrar basfil/checksumma. GitHub lagrar repository, default branch, base SHA, working branch och PR-status.
6. Planändringar loggas explicit och historiskt i `plan_changes`.
7. Ett nästa steg är körbart först när dess beroenden är avslutade eller explicit hoppade över och det inte är blockerat.

## Validering

Kör:

```bash
python3 scripts/validate_runtime_models.py
pytest -q tests/runtime/test_status_models.py
python3 scripts/derive_next_step.py \
  --plan schemas/examples/refactoring-plan.yaml \
  --status schemas/examples/work-status-zip.yaml
```

Sista kommandot ska härleda `R-002` helt från plan och status, utan konversationshistorik.
