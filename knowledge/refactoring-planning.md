# Refaktoreringsplanering och nästa steg

Detta dokument är canonical kunskapsstöd för att omvandla Kodförbättrarens initialanalys till en säker genomförandeplan.

## Grundprincip

Planen ska vara en körbar förändringssekvens, inte en önskelista. Varje steg ska ha ett avgränsat mål, tydlig koppling till findings, verifiering och klart-kriterier. Planen ska kunna återupptas från maskinläsbar status utan att samtalsminne krävs.

## Från finding till steg

För varje prioriterad finding:

1. avgör om den faktiskt ska åtgärdas nu,
2. identifiera eventuella beroenden,
3. avgör om testskydd eller annan förberedelse måste komma först,
4. välj minsta sammanhängande förändring som ger verifierbar nytta,
5. klassificera förändringen som `refactoring`, `functional_change`, `ux_change` eller `mixed`,
6. definiera `done_when` och konkret verifiering,
7. länka finding-id till ett eller flera steg.

En finding får delas över flera steg när det minskar risk. Flera findings får ligga i samma steg endast när de har samma grundorsak och rimligen verifieras tillsammans.

## Stegstorlek

Dela ett steg när något av följande gäller:

- flera oberoende ansvar ändras,
- refaktorering och beteendeförändring kan separeras,
- testskydd behöver etableras innan strukturändringen,
- diffen blir svår att granska som en enhet,
- rollback skulle bli otydlig,
- flera olika verifieringsstrategier krävs.

Slå inte ihop steg bara för att de ligger i samma fil eller modul.

## Testskydd före risk

Om en hög-riskändring berör svagt eller okänt verifierat beteende ska planen normalt lägga ett skyddssteg före produktionsändringen. Skyddet kan vara characterization tests, fokuserad integrationstest, reproducerbar baseline eller annan proportionerlig seam.

Planen får inte låtsas att testskydd finns. Om nödvändigt skydd inte kan etableras ska beroende steg markeras blockerade eller föregås av ett explicit undersökningssteg.

## Beroenden

Finding-beroenden från analysen ska översättas till stegberoenden. Ett steg får vara `ready` först när alla dess `depends_on` är completed eller skipped på ett uttryckligt godkänt sätt.

Undvik artificiella kedjor. Oberoende steg behöver inte göras sekventiella bara för att planen är numrerad.

## Nästa steg

Nästa steg ska härledas deterministiskt från plan + status:

1. om aktuellt steg har öppen blockerare eller misslyckad obligatorisk verifiering: stanna,
2. om aktuellt steg pågår: fortsätt det,
3. annars välj första icke avslutade, icke blockerade steget vars beroenden är uppfyllda,
4. om källsnapshoten inte längre motsvarar aktuell kodbas: kräv fokuserad re-baselining innan implementation,
5. om inget steg är körbart men arbete återstår: rapportera blockerad plan,
6. om allt är completed/skipped: markera planen complete.

"Gör nästa steg" får aldrig hoppa över ett misslyckat test eller en öppen blockerare.

## Omplanering

Om ny evidens uppstår får planen ändras genom `insert`, `split`, `merge`, `reorder`, `skip` eller `scope_change`. Ändringen ska registreras med tid, berörda steg och motivering.

Typiska skäl:

- ett nytt blockerande problem upptäcks,
- steget visade sig större än analysen antydde,
- ett finding är redan löst i aktuell kod,
- testskydd måste införas först,
- kodbasen har ändrats sedan analysen,
- en enklare lösning blev möjlig.

Redan avslutade steg skrivs inte om historiskt. Planhistoriken ska visa att omplanering skedde.

## Källsnapshot och drift

Planen ska bära identifierare för källan som analyserades, exempelvis ZIP-checksumma eller Git commit SHA. Före nästa implementationssteg jämförs detta med aktuell källa när det är praktiskt möjligt.

Vid relevant drift:

- gör fokuserad omanalys av berört område,
- kontrollera om findings fortfarande gäller,
- uppdatera beroenden och steg vid behov,
- registrera planändring,
- fortsätt först när plan/status åter motsvarar koden.

Små irrelevanta ändringar behöver inte tvinga fram full ny analys.

## Markdown-plan

Den mänskligt läsbara `refactoring-plan.md` ska minst innehålla:

- sammanfattning och mål,
- källsnapshot,
- constraints,
- ordnad steglista,
- finding → steg-koppling,
- beroenden,
- risk och förändringsklassificering,
- klart-kriterier,
- verifiering,
- blockerare/antaganden när relevant,
- nästa steg enligt aktuell status om status finns.

Den maskinläsbara planen är canonical för automation; Markdown-versionen är presentation av samma innehåll.
