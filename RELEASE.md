# Kodförbättraren 1.0.0

Första stabila versionen av Kodförbättraren.

## Huvudfunktioner

- read-only initial analys av källkod och prioriterade findings,
- nedladdningsbar stegvis refaktoreringsplan,
- `Gör nästa steg`/`Fortsätt` med beständig status,
- säker ZIP-import och komplett ZIP efter varje lyckat steg,
- GitHub branch/PR-livscykel med återanvändning av öppen PR och ny PR efter merge,
- evidensbaserade code-smell-heuristiker och design-pattern-beslut,
- test-/regressionssäker refaktorering,
- separat UX/usability-analys,
- teknikprofiler för Java/Quarkus, JS/TS, React och generell backend/webb,
- Chat ZIP och Custom GPT från samma canonical beteendekontrakt,
- CI och releasebygge från GitHub Release-taggen.

Se `docs/known-limitations.md` före produktionsanvändning.


## GPT Byggaren 1.5-migrering

Efter version 1.0.0 har projektet migrerats till GPT Byggaren 1.5.0 med oförändrat domänbeteende. ChatGPT Chat, ChatGPT Custom och OpenCode är aktiva peer runtimes. Fem-runtime parity, release-readiness och CI/release workflow parity verifieras deterministiskt.
