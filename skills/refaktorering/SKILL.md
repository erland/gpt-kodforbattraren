---
name: refaktorering
description: Planera och genomför säker, inkrementell kodförbättring med verifierat testskydd.
---
# Refaktorering

Använd för en konkret kodförändring efter analys. `src/instructions/system.md` är auktoritativ; särskilt avsnitt 3–6, 9–10 och 20 samt Operativ kärna. Ingen Skill ersätter de reglerna.

## Arbetsgång
1. Läs verklig projektstatus och plan, identifiera ett begränsat nästa steg.
2. Klassificera arbetet som beteendebevarande refaktorering, funktionell ändring eller UX-ändring.
3. Fastställ baseline och testskydd; lägg vid behov till characterization tests före en riskfylld ändring.
4. Genomför minsta begripliga diff, kör relevanta tester och jämför med baseline.
5. Avbryt eller rulla tillbaka om en ny regression inte kan isoleras, eller om steget kräver oplanerad beteendeförändring.
6. Uppdatera maskinläsbar status endast när verifierade klart-kriterier passerar.

## Fördjupning vid behov
- `knowledge/refactoring-planning.md`
- `knowledge/refactoring-test-safety.md`
- `knowledge/code-quality-refactoring.md`
- `knowledge/ux-usability.md`

Utan körmöjlighet får ändringen inte rapporteras som testad.
