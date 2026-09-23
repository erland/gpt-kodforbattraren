# Kodförbättraren

Kodförbättraren är en GPT för säker, inkrementell förbättring av befintlig programvara. Den analyserar kod och arkitektur, prioriterar teknisk skuld och förbättringsmöjligheter, skapar en stegvis plan och genomför därefter ett verifierbart steg i taget.

## Primära arbetslägen

- **ZIP:** användaren lämnar ett projekt som ZIP och får efter implementeringssteg tillbaka en komplett uppdaterad ZIP.
- **GitHub:** GPT:n arbetar via branch/PR och fortsätter i en relevant öppen PR tills den mergas; därefter startar nästa steg från aktuell default branch i en ny PR.

## Förbättringsperspektiv

- kodkvalitet och refaktorering,
- arkitektur och ansvarsfördelning,
- testbarhet och säker förändring,
- developer experience,
- UX/usability när användaren efterfrågar det.

## Canonical kärnkontrakt

`src/instructions/system.md` är canonical instruktion. Den kräver bland annat analys före bred förändring, prioritering efter faktisk effekt, små verifierbara steg, explicit skillnad mellan beteendebevarande refaktorering och funktionell/UX-förändring, avstående från refaktorering utan tydlig nytta samt projektfilbaserad återupptagning vid "Gör nästa steg".

Kritiska runtime-regler ska vara begripliga utan Knowledge-retrieval. Knowledge används för fördjupade heuristiker, patterns, UX och exempel. Steg 6 har aktiverat kodkvalitetsheuristikerna i `knowledge/code-quality-refactoring.md` och den maskinläsbara katalogen `knowledge/code-quality-heuristic-catalog.yaml`. Steg 7 kompletterar dessa med problemorienterad arkitektur- och design pattern-kunskap i `knowledge/architecture-patterns.md` och `knowledge/architecture-pattern-catalog.yaml`. Steg 8 lägger till riskbaserad test- och säkerhetsstrategi i `knowledge/refactoring-test-safety.md` och `knowledge/refactoring-test-safety-catalog.yaml`. Steg 9 lägger till separat UX/usability-analys i `knowledge/ux-usability.md` och `knowledge/ux-usability-catalog.yaml`. Steg 10 formaliserar initial analys/prioritering. Steg 11 lägger till planeringsmotorn i `knowledge/refactoring-planning.md`, `knowledge/refactoring-planning-catalog.yaml`, `scripts/generate_refactoring_plan.py` och den förstärkta `scripts/derive_next_step.py`. Steg 12 lägger till ZIP-arbetsflödet i `knowledge/zip-workflow.md`, policyfilen samt `scripts/zip_workspace.py`/`scripts/zip_work_status.py`.

## Projektstyrning

- `docs/development-plan.md` – canonical utvecklingsplan.
- `project-status.yaml` – maskinläsbar faktisk status.
- `STATUS.md` – mänskligt läsbar status.
- `gpt-project.yaml` – projektkonfiguration.
- `tests/scenarios/canonical-behavior.md` – kärnscenarier för beteendekontraktet.
- `schemas/finding.schema.json` – canonical finding-format.
- `schemas/refactoring-plan.schema.json` – canonical planformat för kodförbättring.
- `schemas/work-status.schema.json` – faktisk runtime-status för ZIP/GitHub-arbete.

## Aktuell fas

Version 1.0.0 är stabil baslinje. GPT Byggaren 1.5-migreringen är i **Steg 24 – slutvalidering av migreringen och releasekedjan**.

## Teknikprofiler

Steg 14 tillför stackdetektion och fördjupande profiler för Java/Quarkus, JavaScript/TypeScript, React och generell backend/webb. Profilerna ändrar inte canonical arbetsflöde utan förbättrar precisionen i heuristiker och verifieringskommandon.

## Rapporter och status-UX

Canonical presentation och kortkommandon definieras i `knowledge/reporting-status-ux.md` och `templates/`.


## GPT Byggaren 1.5-arkitektur

Projektet är stateful och workspace/tool-heavy. Maskinläsbar status är auktoritativ framför chattminne.

Aktiva peer runtimes:
- ChatGPT Chat
- ChatGPT Custom
- OpenCode

Bedömda men inaktiva:
- Claude Projects
- OpenAI Plugin

De aktiva runtimepaketen delar samma plattformsneutrala capability-, artifact-, workspace_state- och tool-kontrakt. OpenCode använder workspace-first, värdens lokala shell/build/test/Git-verktyg och deklarerar inte projektets `scripts/` som automatiska runtime-tools.
