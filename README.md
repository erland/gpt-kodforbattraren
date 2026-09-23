# Kodförbättraren

Kodförbättraren är ett GPT-projekt för säker och inkrementell förbättring av befintlig källkod. Den ska analysera ett projekt innan ändringar görs, prioritera förbättringar, skapa en stegvis plan och därefter kunna genomföra ett avgränsat steg åt gången via ZIP eller GitHub/PR.

## Distributioner

Projektet bygger tre aktiva runtime-distributioner från samma canonical kontrakt:

- Chat ZIP
- Custom GPT
- OpenCode

Canonical source ligger i projektträdet; genererade distributioner hamnar under `dist/` och ska inte vara källmaterial. Claude Projects och OpenAI Plugin är registrerade men inaktiva tills deras workspace-/verktygsparitet verifierats.

## Projektstatus

Den primära statuskällan är `project-status.yaml`. Den mänskligt läsbara sammanfattningen finns i `STATUS.md`.

## Utvecklingsplan

Se `docs/development-plan.md`.

## Aktuellt läge

Steg 1–23 är verifierade. Version `1.0.0` är fortsatt stabil baslinje och migreringen till GPT Byggaren 1.5.0 slutvalideras i steg 24.

Se `docs/release-readiness.md`, `docs/runtime-parity.md` och `docs/known-limitations.md`. Nästa naturliga aktivitet är GitHub CI och en Release med taggen `v1.0.0`.
