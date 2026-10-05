# Runtime-paritet – GPT Byggaren 1.5

| Förmåga | Chat ZIP | Custom GPT | OpenCode | OpenAI Plugin | Status |
|---|---|---|---|---|
| Analys före bred ändring | Ja | Ja | Ja | Ja | Paritet |
| Evidensbaserad prioritering | Ja | Ja | Ja | Ja | Paritet |
| Design patterns utan pattern-for-pattern-sake | Ja | Ja | Ja | Ja | Paritet |
| Refactoring vs functional/UX change | Ja | Ja | Ja | Ja | Paritet |
| Baseline/testskydd och stopp vid regression | Ja | Ja | Ja | Hostberoende faktisk exekvering | Runtimeanpassat |
| `Gör nästa steg` styrs av faktisk status | Ja | Ja | Ja | Ja, workspace-state | Paritet |
| `Vad är nästa steg?` är read-only | Ja | Ja | Ja | Ja | Paritet |
| Komplett ZIP efter ZIP-steg | Ja | Ja, med filskapande | Ja, via workspace | Ja när hosten kan skapa arkiv | Runtimeanpassat |
| GitHub PR-livscykel | Ja när connector finns | Ja när Action/connector finns | Ja via värdens Git-verktyg | Ja när auktoriserad GitHub-capability finns | Miljöberoende |
| Lokala build/test/shell-verktyg | Värdberoende | Begränsat/värdberoende | Ja | Krävs från host för full parity | OpenCode-styrka |
| Deterministiska hjälpscript inkluderade | Ja | Nej, beteendet kompilerat | Ja som stödresurser | Ja, avgränsad runtime-closure | Avsiktlig skillnad |
| Kan rekommendera ingen refaktorering | Ja | Ja | Ja | Ja | Paritet |

## Aktiva peer runtimes

- ChatGPT Chat – ready
- ChatGPT Custom – reduced men aktiv
- OpenCode – ready
- OpenAI Plugin – equivalent_runtime_dependent

Claude Projects är registrerad men inaktiv. Plugin använder samma canonical behavior/state-kontrakt men full implementation beror på hostens writable workspace, persistent state, shell/code execution samt vid behov GitHub/archive-capability.

OpenCode-distributionen använder `AGENTS.md`, `.opencode/runtime-contract.json` och `.opencode/skills/kodforbattraren/SKILL.md`. Projektets `scripts/` följer med som stödresurser men deklareras inte automatiskt som runtime-tools.


## GPT Byggaren 1.5 – registrerade runtimes

| Runtime | Suitability | Aktiv |
|---|---|---|
| ChatGPT Chat | ready | Ja |
| ChatGPT Custom | reduced | Ja |
| OpenCode | ready | Ja |
| Claude Projects | reduced | Nej |
| OpenAI Plugin | equivalent_runtime_dependent | Ja |

Paritetsgrinden jämför **behavior, capability, artifact, workspace_state och tool**. De fyra aktiva runtimepaketen måste bära samma plattformsneutrala kontrakt. OpenAI Plugin får uttrycka hostberoende adapterkrav utan att försvaga canonical state-, verifierings- eller leveransregler. Claude Projects förblir inaktiv.

`scripts/validate_runtime_parity.py` och `scripts/validate_release_readiness.py` är blockerande i både CI och release.
