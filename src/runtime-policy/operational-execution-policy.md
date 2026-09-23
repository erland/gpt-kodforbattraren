# Operativ exekveringspolicy

Kodförbättraren är ett stateful, workspace- och tool-tungt arbetsflöde.

1. Läs projektkontrakt och strukturerad status före progression.
2. Välj exakt ett avgränsat förbättringsmål eller korrigeringsmål.
3. Läs endast direkt relevanta policies och heuristiker.
4. Gör inga breda kodändringar före evidensbaserad analys.
5. Kör relevant baseline före riskfylld förändring när möjligt.
6. Kör deterministiska verifieringar efter ändring.
7. Vid failing verifiering: korrigera felet före nästa ordinarie steg.
8. Uppdatera strukturerad status först när stegets klart-kriterier är uppfyllda.
9. Härled nästa steg från faktisk status, inte från chattminne.

## Auktoritativ status

Projektets maskinläsbara status går före konversationshistorik. Ett steg är inte klart enbart för att kod har ändrats; relevant verifiering måste också ha passerat.

## ZIP och GitHub

I ZIP-läge ska den uppdaterade ZIP:en motsvara verifierat workspace-tillstånd. I GitHub-läge ska faktisk branch/PR-status läsas före fortsatt arbete. En öppen relevant PR fortsätter att användas; efter merge utgår nästa steg från aktuell default branch.
