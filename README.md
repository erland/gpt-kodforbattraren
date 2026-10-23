# Kodförbättraren

Kodförbättraren analyserar och förbättrar befintlig programvara inkrementellt. Den stöder ZIP-baserat arbete och GitHub/PR-flöden, med analys, prioritering, baseline och regressionstester före avslutade förbättringssteg.

## Kanoniska källor och distribution

`src/instructions/system.md` är den sammanställda, kanoniska legacy-instruktionen. Dess modulära motsvarighet ligger i `src/instructions/core.md` och `src/instructions/skills/`, med byte-för-byte-paritet enligt `canonical/modular-assembly.json`.

Projektet har två distributionsspår som måste skiljas åt:

- **Äldre profil i `gpt-project.yaml` och ordinarie CI:** Chat ZIP, Custom GPT, OpenCode och OpenAI Plugin är aktiva; Claude Projects är inaktiv i denna profil.
- **Migrerat releaseflöde:** `.github/workflows/release.yml` använder versionslåst **GPT Byggaren 1.6.26**, genererar en separat migrationsprojektkopia genom `scripts/prepare_builder_1626.py` och bygger fem runtime-distributioner samt en komplett projekt-ZIP. En separat, valfri Engine ZIP byggs och självtestas. Det migrerade flödet ersätter inte automatiskt den äldre profilens inställningar på `main`.

Byggda arkiv hör hemma i distributionsartefakter, inte som kanonisk källa. GitHub-releaseversionen och eventuell installerad Plugin-version ska verifieras mot faktiska releaseartefakter före påståenden om driftsatt version.

## Verifiering och valfria verktyg

ZIP kräver inte GitHub. Kodförbättraren föredrar tillgänglig lokal build/test i ZIP-läge och befintlig GitHub Actions i GitHub-läge. Vid behov får de valfria pluginerna Agent Workspace (isolering, build, test), PWA Preview (temporär publicering av säker statisk webb) och Browser Screenshot (visuella eller verkligt interaktiva webbläsarkontroller) användas. Frånvaro av plugin blockerar inte analys eller planering; en obligatorisk ej körd kontroll får aldrig rapporteras som PASS.

Se `src/runtime-policy/optional-companion-verification-policy.md`. PR #10 införde instruktioner och statiska kontraktstester. PR #11 tillförde offline-fallbacktester av en ren referensmodell; dessa anropar **inte** live-MCP och bevisar inte i sig faktisk modellorkestrering.

## Projektstatus och underlag

`project-status.yaml` är den auktoritativa arbetsstatusen. Se även `STATUS.md`, `PROJECT.md`, `docs/development-plan.md`, `docs/release-readiness.md` och `docs/known-limitations.md`.

Version `1.0.0` är projektets dokumenterade domänbaslinje och ska inte förväxlas med GPT Byggaren-motorns `1.6.26`.
