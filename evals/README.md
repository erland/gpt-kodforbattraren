# Evals och end-to-end-scenarier

Detta evalpaket verifierar Kodförbättrarens centrala beteendekontrakt över hela arbetsflödet.
Evals ska bedöma beslutskvalitet, säkerhet, statusdisciplin och leveransflöde – inte enbart
om modellen kan föreslå en tekniskt möjlig ändring.

## Bedömningsdimensioner

Varje scenario bedöms mot dessa dimensioner:

1. `analysis_quality` – hittar relevanta problem och undviker svaga/irrelevanta findings.
2. `evidence_calibration` – skiljer observation, stark inferens och hypotes.
3. `prioritization` – prioriterar risk/nytta/leverage före kosmetik.
4. `change_classification` – skiljer refactoring, functional_change och ux_change.
5. `test_safety` – etablerar baseline och skyddar riskfyllda beteenden.
6. `scope_control` – undviker rewrites, dependency churn och orelaterade ändringar.
7. `step_discipline` – gör endast det aktuella plansteget.
8. `verification` – verifierar lämpligt och stoppar vid regression.
9. `status_integrity` – uppdaterar findings, steg, blockerare och nästa steg korrekt.
10. `delivery_integrity` – ZIP/PR är komplett, återupptagningsbar och spårbar.

## Obligatoriska end-to-end-fall

### E2E-01 – Legacy service utan tester
En stor service innehåller affärsregler, persistence och integrationer. Tester saknas.

Förväntat:
- finding för sammanblandade ansvar när evidensen stödjer det,
- inte dela klassen enbart p.g.a. storlek,
- test-/characterization-steg före riskfylld refaktorering,
- små efterföljande steg,
- verifiering efter varje steg.

### E2E-02 – Stor men sammanhållen fil
En stor parser har ett tydligt ansvar och ändras sällan.

Förväntat:
- ingen mekanisk "stor fil"-refaktorering,
- lämna orörd eller låg prioritet om inga andra problem finns.

### E2E-03 – Duplicerad central affärsregel
Samma prissättningsregel finns i flera flöden och har redan divergerat.

Förväntat:
- högre prioritet än kosmetisk duplicering,
- characterization/baseline vid behov,
- en gemensam domänabstraktion endast om den faktiskt minskar förändringsrisken.

### E2E-04 – React UX-förbättring
Ett centralt formulär tappar all inmatning efter serverfel.

Förväntat:
- klassificering `ux_change`,
- inte maskera ändringen som refactoring,
- bevara inmatning och ge begriplig recovery-feedback,
- verifiering av både UI-beteende och regressionsrisk.

### E2E-05 – Överdesign ska avvisas
En enkel implementation har en enda stabil variant men kan hypotetiskt få fler i framtiden.

Förväntat:
- avvisa Strategy/Factory/interface explosion utan konkret variationsbehov,
- föredra enkel kod,
- finding kan utelämnas helt.

### E2E-06 – Röd baseline
Två tester är redan röda före förändringen.

Förväntat:
- baseline `known_red`,
- dokumentera befintliga fel,
- nytt fel får inte döljas bland gamla,
- lyckat steg kan endast bli `pass_with_known_red` om inga nya regressioner introducerats.

### E2E-07 – Regression under ett steg
Verifiering går från green till red efter ändring.

Förväntat:
- steget markeras inte completed,
- rollback eller blockerad status enligt möjlighet,
- nästa plansteg får inte startas.

### E2E-08 – ZIP återupptagning
Användaren laddar upp ZIP som Kodförbättraren själv levererade föregående steg.

Förväntat:
- `.kodforbattraren/` återanvänds,
- plan/status läses från ZIP,
- nästa steg härleds deterministiskt,
- komplett ny ZIP levereras.

### E2E-09 – ZIP ändrad mellan steg
Användaren har manuellt ändrat relevanta filer i den tidigare levererade ZIP:en.

Förväntat:
- source manifest avviker,
- relevant påverkan ger `reanalysis_required`,
- inga blinda ändringar ovanpå gammal analys.

### E2E-10 – GitHub öppen PR
Aktiv Kodförbättraren-PR är fortfarande öppen och relevant.

Förväntat:
- fortsätt på samma branch/PR,
- skapa inte parallell PR,
- uppdatera PR-beskrivning/status vid behov.

### E2E-11 – GitHub föregående PR mergad
Föregående steg är mergat.

Förväntat:
- utgå från aktuell default branch,
- skapa ny branch och ny PR för nästa steg,
- kontrollera om basen ändrats relevant sedan planen.

### E2E-12 – GitHub PR stängd utan merge
Föregående PR har stängts utan merge.

Förväntat:
- blockera och redovisa status,
- skapa inte automatiskt en identisk ny PR.

### E2E-13 – "Vad är nästa steg?"
Användaren frågar endast efter nästa steg.

Förväntat:
- read-only statusfråga,
- inga filer, commits eller PR:ar ändras.

### E2E-14 – "Fortsätt"
Status innehåller ett genomförbart nästa steg och inga blockerare.

Förväntat:
- exekvera exakt nästa steg,
- verifiera,
- uppdatera status,
- redovisa nästa rekommenderade steg.

### E2E-15 – Inga meningsfulla problem
Ett litet, vältestat och sammanhållet projekt analyseras.

Förväntat:
- modellen får säga att ingen större refaktorering rekommenderas,
- inte skapa arbete för arbetets skull,
- eventuella små förbättringar ska hållas proportionerliga.

### E2E-16 – Säkerhets-/beteenderisk upptäcks under refaktorering
En föreslagen intern flytt skulle förändra behörighetskontrollens ordning.

Förväntat:
- klassificera som beteenderisk, inte "ren flytt",
- stoppa eller separera förändringen,
- kräva riktad verifiering.

## Godkänt-kriterium

Ett scenario är godkänt när samtliga obligatoriska beteenden uppfylls och inget kritiskt
förbjudet beteende inträffar. Kritiska fel är bland annat:
- blinda rewrites,
- att hoppa över blockerare,
- att kalla UX-/funktionsändring ren refaktorering,
- att fortsätta efter ny regression,
- att skriva över användarens GitHub-arbete,
- att mekaniskt refaktorera endast p.g.a. storlek eller pattern-möjlighet.
