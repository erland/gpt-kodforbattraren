# Kodförbättraren

Kodförbättraren är ett GPT-projekt för säker och inkrementell förbättring av befintlig källkod. Den ska analysera ett projekt innan ändringar görs, prioritera förbättringar, skapa en stegvis plan och därefter kunna genomföra ett avgränsat steg åt gången via ZIP eller GitHub/PR.

## Distributioner

Projektet ska bygga två runtime-distributioner från samma canonical kontrakt:

- Chat ZIP
- Custom GPT

Dessutom byggs en komplett projekt-ZIP. Canonical source ligger i projektträdet; genererade distributioner ska senare hamna under `dist/` och ska inte vara källmaterial.

## Projektstatus

Den primära statuskällan är `project-status.yaml`. Den mänskligt läsbara sammanfattningen finns i `STATUS.md`.

## Utvecklingsplan

Se `docs/development-plan.md`.

## Aktuellt läge

Alla 20 planerade utvecklingssteg är avslutade och projektet är **release ready**. Första stabila versionskandidaten är `1.0.0`.

Se `docs/release-readiness.md`, `docs/runtime-parity.md` och `docs/known-limitations.md`. Nästa naturliga aktivitet är GitHub CI och en Release med taggen `v1.0.0`.
