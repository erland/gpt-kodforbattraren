# Plugin-mappning och Engine-beslut – GPT Byggaren 1.6.26

Granskat mot den verkliga källkods-ZIP-filen från commit `24a294e6c6f343600e78309d806d4ed365687706` och migreringsrapporten.

## Beslut om Plugin-mappning

Legacy: `runtime.openai_plugin` (aktiverad, `skills_first`, `peer_distribution`). Målet är modern `runtime.plugin` men **initialt `enabled: false`**. Gamla nyckeln får finnas kvar som dokumenterat migrationsunderlag tills alla validerare och byggskript gått över. Den får inte tolkas som bevis för att nya runtimevarianten är aktiverad.

- Manifest: `plugin.json`.
- Skills: `skills/kodforbattraren/SKILL.md`, härledd från `src/instructions/system.md` och nuvarande Plugin-generator, inte en generisk ny instruktion.
- Huvudflöde: läs faktiskt projekt/workspace-state, analysera, planera, genomför avgränsade ändringar, kör relevanta tester, uppdatera status.
- Värdberoende: filesystem read/write och persistent workspace-state krävs för fullt implementationsflöde; shell/code execution krävs för testad implementation. GitHub write är frivilligt och används bara där verktyget finns.
- Säkert reducerat beteende: utan skrivbart bestående workspace erbjud endast analys och planering; utan shell/körning påstå inte godkänd implementation; utan ZIP-utdata påstå inte levererad projekt-ZIP.
- Ingen obligatorisk MCP-koppling.

## Bedömning av befintliga Python-skript

| Skript | Klassificering | Slutsats |
|---|---|---|
| `derive_next_step.py` | Körbart deterministiskt runtime-stöd | Hjälper statusstyrd progression |
| `detect_technology_profiles.py` | Körbart runtime-stöd | Hjälper kodanalys |
| `generate_refactoring_plan.py` | Körbart runtime-stöd | Hjälper reproducerbar planering |
| `github_pr_decision.py` | Körbart runtime-stöd | Hjälper PR-beslut; ger inte GitHub write i sig |
| `interpret_progress_command.py` | Körbart runtime-stöd | Hjälper konsekvent stegtolkning |
| `zip_work_status.py` | Körbart runtime-stöd | Hjälper status i ZIP-läge |
| `zip_workspace.py` | Körbart runtime-stöd | Hjälper ZIP-packning; utdata förutsätter runtime med arkivstöd |
| `build_distributions.py` | Byggverktyg | Endast projektbygge/release |
| `validate_*.py`, `check_project_hygiene.py` | Verifiering/CI | Används i kvalitetssäkring, inte som generella Plugin-verktyg |

De sju runtime-skripten paketeras enligt befintlig `PLUGIN_SCRIPTS`. Nuvarande adapter har redan `local_scripts_are_runtime_tools: false`; paketering betyder alltså **inte** att värdplattformen exekverar dem automatiskt.

## Engine ZIP: beslut

**Inte automatiskt aktiverad.** Migreringsmotorn kräver explicita `tools.tools[]`-deklarationer av Python-script med `requirement: required` samt verklig `scripts/selftest.py` innan projekt-Engine kan konfigureras. Nuvarande profil har `tools.tools: []` och inget sådant självtest verifierat. Att skapa tom/fiktiv Engine eller deklarera falsk obligatorisk körbarhet skulle försvaga kontraktet.

Pröva i stället installerade Skills + host-exekvering med befintliga scriptresurser. Om tester visar att tillförlitlig runtime-körning saknas, skapa ett riktigt Engine med reproducerbart självtest i ett separat, spårbart steg.

## Granskningens slutsats

Den semantiska mappningen och skriptklassificeringen är fastställd. **Host-kapacitet och import av den färdigbyggda Plugin-distributionen är fortfarande ej verifierade.** `enabled: true` vore därför för tidigt. Nästa steg är en explicit, icke-aktiverande kanonisk byggprofil samt validering av de fem distributionerna i separat kopia.

Källa: `reconstructed-canonical/plugin-migration-plan.json` genererad vid ZIP-migreringen och det befintliga `scripts/build_distributions.py`.
