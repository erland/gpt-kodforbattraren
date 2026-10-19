# Femdistributionsbygge – isolerat tekniskt genombrott

Datum: 2026-10-19. Källbas: commit `24a294e6c6f343600e78309d806d4ed365687706`, kanonisk motor GPT Byggaren 1.6.26.

## Verifierad lokal provbyggning

I kopian av den äldre källan, med GPT Byggarens installerade `scripts/build_distributions.py`, har en experimentell konfiguration tagits fram:

- Modern `build_system.runtime_targets` med `project` och fem runtimes.
- Modern `structure` och de runtimeavsnitt som byggskriptet kräver.
- Tre projektspecifika Skill-definitioner (kodanalys, refaktorering och leverans/status), med explicit deklarerade referenser och utan obligatoriska externa skript.
- Tom lista med tidigare GPT Byggaren-specifika OpenCode Skills så att dokument från ett annat projekt inte används.
- Projektspecifik `project.description` för Plugin-manifestet.
- Byggmotorns saknade `templates/*.tpl` har tillförts **arbetskopian** från samma versionsmatchade motor.
- Custom GPT avaktiverad i provkonfigurationen.

Efter dessa ändringar avslutades `python scripts/build_distributions.py --version migration-test` med **Build complete**.

## Byggresultat

| Arkiv | Antal filer | ZIP-test |
|---|---:|---|
| `kodforbattraren-chat-migration-test.zip` | 104 | PASS |
| `kodforbattraren-claude-project-migration-test.zip` | 25 | PASS |
| `kodforbattraren-claude-skills-migration-test.zip` | 10 | PASS |
| `kodforbattraren-opencode-migration-test.zip` | 32 | PASS |
| `kodforbattraren-plugin-migration-test.zip` | 11 | PASS |
| `kodforbattraren-project-migration-test.zip` | 165 | PASS |

`DELIVERY-MANIFEST.json` och `SHA256SUMS.txt` skapades. ZIP-testet använder `zipfile.testzip()`, som gav `None` för samtliga sex arkiv.

## Viktiga begränsningar

- Provbygget kördes på uppladdat basarkiv, **inte** på en komplett nedladdad checkout av PR-grenen. Därför bevisar det inte att varje senare GitHub-ändring kan byggas oförändrat.
- För byggexperimentet användes minsta Skill-källtext i arbetskopian. De tre utförligare Skill-filerna från PR:n är inte ännu fullständigt integrerade och paritetstestade.
- Provbygget verifierar ZIP-integritet, inte att Plugin kan importeras i ChatGPT, att bestående workspace fungerar eller att faktisk kodförbättring fungerar i respektive runtime.
- Genererad konfiguration, motorfiler och ZIP har inte checkats in i PR:n; den befintliga distributionskedjan är orörd.
- Ingen fullständig runtimeparitet, modern CI eller releaseautomation är ännu verifierad.

## Nästa steg

1. Använd de tre fullständiga Skill-filerna på migrationsgrenen som kanonisk källa, skapa deras riktiga `src/instructions/skills/<id>/behavior.md` och kontrollera att källa–projektion är spårbar.
2. Lägg in projektspecifik kanonisk byggprofil och nödvändiga motorresurser i PR efter säker filjämförelse.
3. Kör modern distribution/lint/paritetsvalidering på samma checkout, komplettera funktionella scenarier.
4. Byt CI och release från fyra till fem artefakter först när tester passerar.
