# Projektstatus – Kodförbättraren

## Aktuell status

**PÅGÅR – migrering till GPT Byggaren 1.5.0, steg 23.**

Version **1.0.0** är fortsatt stabil/release-ready baslinje. Steg 21–22 är verifierade utan regression i ZIP-, GitHub/PR-, runtime- eller distributionsflödet.

## Verifierat i steg 22

- Chat ZIP har explicit 1.5-runtime-kontrakt,
- Custom GPT har explicit 1.5-runtime-kontrakt,
- Custom GPT innehåller Operativ kärna och Auktoritativ status inom 8 000 tecken,
- OpenCode byggs som aktiv peer-runtime,
- OpenCode innehåller `AGENTS.md`, `.opencode/runtime-contract.json`, skill och workspace-first-konfiguration,
- `scripts/` följer med som stödresurser men blir inte automatiskt runtime-tools,
- CI bygger tre runtimeartefakter,
- OpenCode-runtimevalidator: PASS,
- full CI-kedja: PASS.

## Nästa rekommenderade steg

**23 – Generaliserad runtime parity och release readiness.**

Behavior, capability, artifact, workspace_state och tool ska verifieras över alla fem registrerade runtimes. Chat, Custom GPT och OpenCode är aktiva; Claude Projects och OpenAI Plugin förblir reducerade/inaktiva tills deras workspace-/verktygsparitet kan verifieras.
