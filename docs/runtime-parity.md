# Runtime-paritet – GPT Byggaren 1.5

| Förmåga | Chat ZIP | Custom GPT | OpenCode | Status |
|---|---|---|---|---|
| Analys före bred ändring | Ja | Ja | Ja | Paritet |
| Evidensbaserad prioritering | Ja | Ja | Ja | Paritet |
| Design patterns utan pattern-for-pattern-sake | Ja | Ja | Ja | Paritet |
| Refactoring vs functional/UX change | Ja | Ja | Ja | Paritet |
| Baseline/testskydd och stopp vid regression | Ja | Ja | Ja | Paritet |
| `Gör nästa steg` styrs av faktisk status | Ja | Ja | Ja | Paritet |
| `Vad är nästa steg?` är read-only | Ja | Ja | Ja | Paritet |
| Komplett ZIP efter ZIP-steg | Ja | Ja, med filskapande | Ja, via workspace | Runtimeanpassat |
| GitHub PR-livscykel | Ja när connector finns | Ja när Action/connector finns | Ja via värdens Git-verktyg | Miljöberoende |
| Lokala build/test/shell-verktyg | Värdberoende | Begränsat/värdberoende | Ja | OpenCode-styrka |
| Deterministiska hjälpscript inkluderade | Ja | Nej, beteendet kompilerat | Ja som stödresurser | Avsiktlig skillnad |
| Kan rekommendera ingen refaktorering | Ja | Ja | Ja | Paritet |

## Aktiva peer runtimes

- ChatGPT Chat – ready
- ChatGPT Custom – reduced men aktiv
- OpenCode – ready

Claude Projects och OpenAI Plugin är registrerade men inaktiva tills deras workspace-/verktygsparitet kan verifieras.

OpenCode-distributionen använder `AGENTS.md`, `.opencode/runtime-contract.json` och `.opencode/skills/kodforbattraren/SKILL.md`. Projektets `scripts/` följer med som stödresurser men deklareras inte automatiskt som runtime-tools.
