# Projektstatus – Kodförbättraren

## Aktuell status

**PÅGÅR – migrering till GPT Byggaren 1.5.0, steg 22.**

Version **1.0.0** är fortsatt stabil/release-ready baslinje. Steg 21 är verifierat utan regression i ZIP-, GitHub/PR-, runtime- eller distributionsflödet.

## Verifierat i steg 21

- plattformsneutrala capability-, artifact-, workspace/state- och tool-kontrakt,
- stateful workspace/tool-heavy modellrobust profil,
- operativ kärna och auktoritativ status,
- fyra modellkompatibilitetsscenarier,
- fem registrerade runtimes bedömda,
- Chat och OpenCode: ready/aktiva,
- Custom GPT: reduced/aktiv,
- Claude Projects och OpenAI Plugin: reduced/inaktiva,
- befintlig full CI-kedja: PASS.

## Nästa rekommenderade steg

**22 – Anpassa distributioner och bygg OpenCode.**

Chat, Custom GPT och OpenCode ska härledas från samma 1.5-kontrakt. OpenCode ska använda workspace och värdens lokala verktyg utan att vi låtsas att projektets `scripts/` automatiskt är runtime-tools.
