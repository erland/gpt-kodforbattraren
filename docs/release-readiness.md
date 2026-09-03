# Release-readiness – Kodförbättraren 1.0.0

## Beslut

**READY** – projektet kan taggas som `v1.0.0` när samma kontroller passerar i GitHub CI.

## Releasekriterier

- Canonical instruktion finns och används som källa för båda runtimeformerna.
- Chat ZIP är självbärande och kan startas utan dold projekthistorik.
- Custom GPT har kompilerad instruktion under 8 000 tecken och högst 20 Knowledge-filer.
- Findings, plan, arbetsstatus och source manifest har schemas.
- ZIP- och GitHub/PR-livscykler har deterministiska beslutsregler.
- Test-/säkerhetsstrategi inkluderar baseline, known-red, characterization tests och regressionstopp.
- UX-förändringar hålls åtskilda från ren refaktorering.
- CI kör modellvalidering, project-status-validering, hygiene, runtime-tester och distributionsbygge.
- GitHub Release bygger artefakter från release-taggen.

## Valideringar

Slutsteget kör:

```text
python scripts/validate_project_status.py
python scripts/validate_runtime_models.py
python scripts/check_project_hygiene.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider tests/runtime
python scripts/build_distributions.py --version 1.0.0
```

Resultatet för releasekandidaten ska vara helt grönt innan leverans.

## Runtime-paritet

Se `docs/runtime-parity.md`.

## Kända begränsningar

Se `docs/known-limitations.md`. Begränsningarna är dokumenterade men inte blockerande för 1.0.0.

## Releaseprocess

1. Lägg projektet i GitHub.
2. Öppna PR och kontrollera att `CI` passerar.
3. Merga till default branch.
4. Skapa GitHub Release med taggen `v1.0.0`.
5. `Build release distributions` checkar ut exakt tagg och bygger:
   - `kodforbattraren-chat-1.0.0.zip`
   - `kodforbattraren-custom-gpt-1.0.0.zip`
   - `release-manifest.json`
6. Kontrollera SHA-256 i manifestet och bifogade release assets.

## Faktiskt slutresultat

- Project status: **PASS / release_ready**
- Runtime-modeller: **PASS**
- Project hygiene: **PASS**
- Runtime-tester: **68/68 PASS**
- Chat ZIP-integritet: **PASS**
- Custom GPT ZIP-integritet: **PASS**
- Chat ZIP SHA-256: `0f2e47c71649b2eaa4fc09023295d91ddda2042251da9709d383926192047c53`
- Custom GPT SHA-256: `cf48841c75620c4d5e2f23546e26899b434e9a6c1f9a58c03a38ed35148375c8`
- Blockerare: **inga**
