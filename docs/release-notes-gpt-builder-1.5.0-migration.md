# Kodförbättraren – migrering till GPT Byggaren 1.5.0

Migreringen bevarar Kodförbättrarens domänbeteende men moderniserar runtime-, state- och releasekontrakten.

Viktigaste förändringar:
- plattformsneutrala capability-, artifact-, workspace_state- och tool-kontrakt
- stateful modellrobust progression och auktoritativ projektstatus
- OpenCode som aktiv ready peer-runtime
- ChatGPT Chat och Custom GPT fortsatt aktiva
- Claude Projects och OpenAI Plugin explicit reducerade/inaktiva
- runtime-kontrakt i alla aktiva distributioner
- fem-runtime parity som blockerande gate
- release-readiness för tre runtimeartefakter
- CI/release workflow parity
- oförändrade kärnregler för ZIP, GitHub/PR, små verifierbara steg och stopp vid regression
