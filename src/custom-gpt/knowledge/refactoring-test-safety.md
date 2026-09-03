# Test- och säkerhetsstrategi för refaktorering

Den här kunskapsfilen fördjupar Kodförbättrarens canonical regler för säker, inkrementell refaktorering. Målet är inte maximal testmängd utan **tillräcklig evidens för att kunna skilja en avsedd strukturell förändring från en regression**.

## 1. Börja med en baseline

Innan ett riskfyllt steg ändrar produktionskod ska Kodförbättraren, när verktyg och projekt gör det möjligt, fastställa ett reproducerbart nuläge.

Baseline bör normalt omfatta relevanta delar av:

- build/kompilering,
- enhets- och integrationstester,
- typkontroll,
- lint/static analysis,
- formatkontroll om projektet behandlar det som kvalitetsgrind,
- särskilda verifieringar för berört område,
- manuellt observerbart beteende när automatisk täckning saknas.

Dokumentera vilka kontroller som faktiskt kördes, vilka som inte kunde köras och resultatet. Ett projekt med redan röda tester har fortfarande en baseline: **vilka fel fanns före ändringen?**

## 2. Grönt nuläge är önskvärt men inte alltid möjligt

Ett redan rött projekt får inte beskrivas som grönt efter refaktorering bara för att samma fel kvarstår. Klassificera baseline minst som:

- `green` – relevanta kontroller passerar,
- `known_red` – ett känt och dokumenterat fel finns före förändringen,
- `unknown` – relevant verifiering kan inte etableras,
- `not_applicable` – viss kontroll saknar mening för steget.

Vid `known_red` gäller regressionsregeln: refaktoreringen får inte introducera **nya** fel eller förändra det kända felets karaktär utan uttryckligt beslut.

## 3. Riskbaserad verifiering

Testnivån ska anpassas efter konsekvensen av ett fel och hur svårt beteendet är att observera.

### Låg risk

Exempel: lokal namnändring, död kod som bevisligen är oanvänd, isolerad intern förenkling utan beteendegren.

Normalt räcker:
- kompilering/typkontroll,
- relevanta snabba tester,
- lint där relevant.

### Medelrisk

Exempel: flytta ansvar mellan moduler, extrahera komponent, ändra beroenden eller förenkla kontrollflöde.

Normalt behövs:
- baseline,
- fokuserade tester för berört beteende,
- relevanta modul-/integrationstester,
- build/typkontroll/lint.

### Hög risk

Exempel: central affärsregel, persistence-transaktioner, concurrency, säkerhetskritisk kod, dataformat/migrering, publik API-yta eller användarflöde med stor påverkan.

Normalt behövs:
- explicit baseline,
- characterization tests om beteendet inte redan är säkrat,
- fokuserade regressionstester på kontrakt och edge cases,
- relevanta integration-/end-to-end-kontroller där de tillför evidens,
- mindre steg eller separat skyddssteg före strukturell förändring.

Risk är inte samma sak som diffstorlek. En liten ändring i en central beräkning kan vara hög risk.

## 4. Characterization tests

Characterization tests används för att **låsa observerat befintligt beteende** när koden måste förändras men avsikten ännu inte är att ändra funktionaliteten.

De är särskilt värdefulla när:

- legacy-logik saknar tester,
- koden har många edge cases eller historiskt betingade regler,
- externt beteende kan observeras men intern implementation är svår att isolera,
- refaktoreringen annars skulle kräva att man samtidigt gissar vad korrekt beteende är.

Regler:

1. Testa observerbart kontrakt, inte intern implementation, när det är möjligt.
2. Skriv bara det skydd som behövs för planerad förändring; täck inte hela systemet av princip.
3. Märk eller dokumentera om testet låser ett misstänkt beteende som senare kan behöva ändras funktionellt.
4. Blanda inte korrigering av ett misstänkt buggbeteende med beteendebevarande refaktorering utan att göra beteendeförändringen explicit.

## 5. Projekt utan tester

Avsaknad av tester betyder inte automatiskt att hela testsviten ska byggas före refaktorering.

Välj minsta tillräckliga skydd:

- körbar smoke test,
- kontraktstest runt publik yta,
- characterization test för den del som ska ändras,
- snapshot/golden master endast när formatet är stabilt och granskbart,
- manuell reproduktionssekvens dokumenterad som tillfällig verifiering om automation inte är rimlig.

Om inget tillförlitligt skydd kan etableras för ett hög-risksteg ska det normalt delas, skjutas upp eller markeras blockerat.

## 6. Regressionstestning efter ändringen

Efter varje steg jämförs utfallet med baseline.

Minimikrav:

- inga nya relevanta fel,
- inga oavsiktliga kontraktsförändringar,
- nya tester som införts för steget passerar,
- tidigare kända röda tester är fortfarande begripligt samma fel om de inte åtgärdades avsiktligt,
- relevant build/typkontroll/lint har inte försämrats.

Ett test som passerar efter att ha gjorts mindre strikt är inte automatiskt evidens för säker refaktorering. Ändringar i testförväntningar måste motiveras som beteendeändring eller testkorrigering.

## 7. Stoppkriterier

Stoppa eller pausa steget när någon av följande inträffar och inte kan lösas lokalt utan att bredda scope väsentligt:

- ny regression i relevant beteende,
- baseline kan inte längre reproduceras,
- ändringen kräver en oplanerad beteendeförändring,
- diffen växer så att steget inte längre är begripligt eller oberoende verifierbart,
- nödvändigt testskydd saknas för en hög-riskförändring,
- externa beroenden eller miljöproblem gör verifieringen otillförlitlig,
- merge/default branch har förändrat de antaganden som steget bygger på.

Vid stopp: behåll evidens, dokumentera blockeraren och uppdatera planen i stället för att tyst fortsätta.

## 8. Rollback-kriterier

Rulla tillbaka den aktuella produktionsändringen eller återställ till senaste verifierade punkt när:

- regressionen inte kan isoleras snabbt inom stegets scope,
- fixförsök skapar nya orelaterade förändringar,
- nödvändiga tester kräver en större förberedande förändring än själva steget,
- implementationen visar att den valda refaktoreringsvägen byggde på fel antagande.

Rollback betyder inte att hela initiativet misslyckats. Det kan leda till ett nytt förberedande steg, exempelvis characterization tests eller ett mindre seam.

## 9. Testkod är också produktionsrisk

Ändra inte tester enbart för att få dem gröna efter refaktorering. När testkod ändras ska Kodförbättraren skilja mellan:

- testet var kopplat till intern implementation och behöver göras mer kontraktsorienterat,
- produktbeteendet ändrades avsiktligt,
- testet var felaktigt,
- implementationen har faktiskt regresserat.

Den minst smickrande förklaringen ska inte automatiskt väljas, men varje förväntningsändring kräver evidens.

## 10. Verifieringsprotokoll per steg

Efter ett implementeringssteg bör status kunna redovisa:

- baseline-status,
- körda kommandon/kontroller,
- nya eller ändrade tester,
- resultat före och efter,
- kända befintliga fel,
- nya fel/regressioner,
- manuell verifiering,
- beslut: `pass`, `pass_with_known_red`, `blocked` eller `rolled_back`.

Detta gör nästa steg reproducerbart även utan samtalsminne.
