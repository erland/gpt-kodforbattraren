---
name: leverans-och-status
description: Återuppta arbete från auktoritativ status och leverera verifierade ZIP- eller GitHub-ändringar.
---
# Leverans och status

Använd när användaren säger ”Gör nästa steg”, arbetar med ZIP eller vill ha branch/PR. Läs alltid först `src/instructions/system.md`, särskilt avsnitt 9–13, 22 och Operativ kärna. Status i arbetskopians `project-status.yaml` är auktoritativ, inte konversationsminnet.

## Arbetsgång
1. Läs `project-status.yaml` och relevant utvecklingsplan; reparera eller rapportera motsägelser.
2. Gör bara nästa verifierbara steg med tillhörande tester och uppdaterad status.
3. Vid ZIP-läge: bevara komplett projektstruktur, inkludera status och verifiera arkivets integritet.
4. Vid GitHub-läge: arbeta i avgränsad branch/PR, bevara originalgren och rapportera exakta ändringar.
5. Redovisa verifierade kontroller, kända fel, återstående arbete och konkret nästa steg.

## Fördjupning vid behov
- `knowledge/zip-workflow.md`
- `knowledge/github-pr-workflow.md`
- `knowledge/reporting-status-ux.md`

Frånvaro av GitHub write, bestående filer eller körmiljö innebär reducerad leverans, inte tyst lyckande.

## Valfri Engine ZIP och säker fallback

När Kodförbättrarens deterministiska Python-skript behöver köras, försök först använda verkligt tillgänglig körmiljö och skript i arbetsprojektet. Om skripten saknas kan användaren bifoga den versionsmatchade `kodforbattraren-engine-<version>.zip` från GitHub Release. Kontrollera arkivintegriteten och kör `python scripts/selftest.py` innan användning. Engine ZIP ger inte i sig åtkomst till Python, bestående filer eller GitHub och kräver ingen MCP-server. Om dessa värdförmågor saknas, erbjud endast analys/planering och redovisa vilka implementationstester som inte kunde köras. Påstå aldrig att ett arbetssteg eller en ZIP har verifierats utan faktisk kontroll.
