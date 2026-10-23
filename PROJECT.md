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

Version 1.0.0 är dokumenterad domänbaslinje. Det separata migrationsreleaseflödet för **GPT Byggaren 1.6.26** är implementerat i `.github/workflows/release.yml`, med versionslåst byggmotor, kontrollsumma, fem runtime-distributioner, projekt-ZIP och valfri Engine ZIP. `project-status.yaml` anger steg 1–25 som slutförda.

## Teknikprofiler

Steg 14 tillför stackdetektion och fördjupande profiler för Java/Quarkus, JavaScript/TypeScript, React och generell backend/webb. Profilerna ändrar inte canonical arbetsflöde utan förbättrar precisionen i heuristiker och verifieringskommandon.

## Rapporter och status-UX

Canonical presentation och kortkommandon definieras i `knowledge/reporting-status-ux.md` och `templates/`.


## Runtime-arkitektur och migrationsspår

Projektet är stateful med maskinläsbar auktoritativ status. Den äldre projektprofilen deklarerar Chat ZIP, Custom GPT, OpenCode och OpenAI Plugin som aktiva, medan Claude Projects är inaktiv. Ordinarie CI validerar detta äldre spår.

Det migrerade GPT Byggaren **1.6.26**-releaseflödet förbereder en separat projektkopia med modulära Skills. Det bygger fem runtime-distributioner och projekt-ZIP från samma canonical beteende. Källans modulära sammanställning kontrolleras byte-för-byte mot `src/instructions/system.md` med hjälp av `canonical/modular-assembly.json`. Den äldre profilen skrivs inte över av migrationen.

## Valfria verifieringsintegrationer

Kodförbättraren använder befintlig CI eller lokal exekvering före externa alternativ när dessa räcker. Agent Workspace kan användas för kompatibel isolerad ZIP-build/test; PWA Preview kan exponera säker statisk output; Browser Screenshot kan verifiera bild eller faktiska interaktioner när hosten stödjer dem. Allt är optional. Se `src/runtime-policy/optional-companion-verification-policy.md`.

PR #10 tillförde instruktioner och statiska kontrakttester. PR #11 tillförde offline-testade fallbackbeslut i en referensmodell utan MCP-anrop. Detta är inte bevis för end-to-end-beteende i den installerade Kodförbättraren.

## OpenAI Plugin

OpenAI Plugin är en aktiv skills-first `equivalent_runtime_dependent` peer runtime. Canonical `tools` förblir tom; utvalda Pythonfiler paketeras som stödresurser och hostens workspace/shell/code/GitHub/archive-capabilities realiserar arbetet.
