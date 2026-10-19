---
name: kodanalys
description: Analysera kodprojekt, teknisk skuld och förbättringsmöjligheter före ändring.
---
# Kodanalys

Använd vid initial projektgranskning, teknikprofilering och prioritering. Läs först projektets auktoritativa `src/instructions/system.md` och aktuell `project-status.yaml` om den finns. Följ originalinstruktionens avsnitt 1, 2, 6–8, 19 och 21 utan att ersätta eller försvaga kärnreglerna.

## Arbetsgång
1. Inventera faktisk kodstruktur, beroenden och verifieringskommandon.
2. Förankra varje iakttagelse i kodbevis; skilj symptom från grundorsak.
3. Bedöm nytta, regressionrisk, kostnad och berörd ändringsfrekvens.
4. Redovisa också sådant som bör lämnas orört.
5. Föreslå prioriterade, avgränsade följdsteg. Ändra inte produktionskod i analyssteget.

## Fördjupning vid behov
- `knowledge/code-quality-refactoring.md`
- `knowledge/initial-analysis-prioritization.md`
- `knowledge/architecture-patterns.md`
- `knowledge/technology-profiles.md`

Om filer inte är åtkomliga, redovisa begränsningen. Påstå inte att analysen är kodförankrad utan tillgång till koden.
