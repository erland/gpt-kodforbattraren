# Migreringsanalys – GPT Byggaren 1.6.26

Datum: 2026-10-19

## Inventering (verifierade källfiler)

- `gpt-project.yaml`: canonical instruktion i `src/instructions/system.md`.
- `project-status.yaml`: 25 avslutade utvecklingssteg och status `release_ready` avser den **tidigare** distributionsuppsättningen.
- `README.md`: aktiva distributioner Chat ZIP, Custom GPT, OpenCode och Plugin.
- `scripts/build_distributions.py`: egen befintlig distributionsbyggare.
- `.github/workflows/ci.yml`: befintliga tester och kontroll av fyra distributionsartefakter.
- `.github/workflows/release.yml`: taggbaserad release och uppladdning av fyra ZIP-artefakter.
- `src/instructions/system.md`: domänspecifikt beteende för inkrementell kodförbättring, riskbedömning, testskydd och statusstyrd återupptagning.

## Målbild

Migrera med GPT Byggaren Chat ZIP **1.6.26** som kanonisk byggmotor.
Behåll Kodförbättrarens beteende, knowledge, schemas, scripts, tester och Git-historik.
Bygg fem distributioner från samma källa:

1. Chat ZIP
2. ChatGPT Plugin (utan obligatoriskt MCP)
3. Claude Project
4. Claude Skills
5. OpenCode

Custom GPT pensioneras först efter att de fem nya distributionerna har byggts, validerats och deras funktionsskillnader dokumenterats. Den tidigare release-statusen räknas inte som verifiering av den nya distributionsuppsättningen.

## Migrationssekvens

1. **Baseline:** kör befintlig CI och spara testresultat; kontrollera nuvarande versions-/releasebeteende.
2. **Säker kopieringsmigrering:** kör GPT Byggarens kanoniska migreringsskript från det versionsmatchade Chat ZIP-paketet i separat arbetskopia. Läs `engine_migration`-rapporten och skydda samtliga projektspecifika filer.
3. **Projektprofil och runtimekontrakt:** uppdatera `gpt-project.yaml`, härled målens adapters och säkerställ att varningar som kräver manuell granskning inte aktiveras tyst.
4. **Domänparitet:** verifiera att kärnregler om analys före ändring, säker stegvis refaktorering, characterization tests, rollback och `project-status.yaml` består i alla fem distributioner.
5. **Plugin:** kontrollera installerbara Skills, nyttjande av befintliga scripts och om projektspecifik Engine ZIP verkligen behövs. Lägg inte till Engine ZIP utan verifierat exekveringsbehov.
6. **CI/release:** byt först efter lyckad migration från fyra till fem artefakter; kör bygg, lint, runtimevalidering, runtimeparitet och arkivintegritet. Versionsnummer skall härledas ur GitHub Release-taggen.
7. **Dokumentation och status:** uppdatera README, STATUS, kända begränsningar och release readiness först när faktisk verifiering finns.

## Säkerhetsgräns

Detta dokument är ett inventerings- och migrationsunderlag, **inte en färdig migration**. Ingen runtime är aktiverad eller avaktiverad genom dokumentet. `project-status.yaml` behåller sin historiska status, men den är inte bevis för kompatibilitet med GPT Byggaren 1.6.26. Alla ändringar som kräver semantisk bedömning skall granskas innan aktivering.

## Klart-kriterier för full migration

- [ ] Befintlig baseline validerad.
- [ ] Migreringsrapport genererad och granskad.
- [ ] Kanonisk motor installerad utan förlust av domänlogik.
- [ ] Alla fem nya distributioner byggda.
- [ ] Samtliga fem runtimevalideringar passerade.
- [ ] Kontroller av semantisk paritet och testfall passerade.
- [ ] CI och GitHub Release uppdaterade och gröna.
- [ ] README och projektstatus beskriver verifierat levererat läge.
