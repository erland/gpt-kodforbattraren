# Kodkvalitet och refaktoreringsheuristiker

Detta dokument fördjupar Kodförbättrarens canonical beteendekontrakt. Heuristikerna används för att skapa evidensbaserade findings – inte för mekanisk poängsättning eller som absoluta regler.

## 1. Bedömningsmodell

För varje misstänkt problem ska bedömningen normalt gå i fem led:

1. **Observation** – vad syns konkret i koden?
2. **Evidens** – vilka filer, symboler, beroenden eller ändringsmönster stödjer observationen?
3. **Konsekvens** – varför spelar det roll för begriplighet, ändringskostnad, testbarhet, felrisk eller användarnytta?
4. **Alternativ** – kan problemet lämnas orört, förenklas lokalt eller kräver det strukturell refaktorering?
5. **Proportionalitet** – är nyttan större än risk, diffstorlek och introducerad komplexitet?

En finding bör inte skapas enbart för att en stilregel eller ett mått passerar en godtycklig gräns.

## 2. Separation of Concerns och Single Responsibility

### Signal

En modul, klass, komponent eller funktion hanterar flera typer av ansvar som har olika orsaker att förändras.

### Starkare evidens

- domänregler blandas med persistence, nätverk, UI eller serialisering,
- samma enhet ändras återkommande av oberoende skäl,
- tester måste mocka flera infrastrukturlager för att verifiera en enkel regel,
- en lokal förändring kräver kunskap om flera tekniska domäner,
- koddelar i samma enhet använder nästan helt olika data och beroenden.

### Svag evidens

- filen är lång,
- klassen har många metoder men alla tjänar samma sammanhållna ansvar,
- en liten mängd orkestrering binder legitimt ihop flera steg i ett use case.

### Typiska åtgärder

Extrahera ansvar, flytta beteende närmare ägd data, separera ren domänlogik från I/O eller skapa tydligare modulgräns. Introducera interface/lager endast om det minskar verklig coupling eller förbättrar testbarhet/variation.

## 3. Cohesion

### Signal

En enhet har låg intern sammanhållning: dess delar hör inte tydligt ihop kring ett gemensamt ansvar eller gemensam data.

### Evidens

- metodgrupper använder disjunkta fält/beroenden,
- ändringar berör ofta bara separata undergrupper av enheten,
- namnet behöver bli vagt, exempelvis `Manager`, `Utils`, `Common`, `Processor`, för att täcka innehållet,
- delar av enheten kan förstås och testas oberoende utan meningsfull koordinering.

### Motbevis

Storlek i sig är inte låg cohesion. En parser, compiler pass eller protokollimplementation kan vara stor men mycket sammanhållen.

## 4. Coupling

### Signal

En förändring eller test av en enhet kräver oproportionerlig kunskap om eller koordinering med andra enheter.

### Evidens

- konkreta infrastrukturdetaljer läcker in i domänlogik,
- många moduler importerar varandras internals,
- cykliska beroenden,
- ändring av ett internt format orsakar shotgun surgery,
- konstruktion kräver ett stort nät av beroenden,
- ett test behöver omfattande setup för ett lokalt beteende.

### Bedömning

Coupling är inte alltid dåligt. Samarbete mellan komponenter är nödvändigt. Fokusera på **onödig**, **instabil** eller **riktad åt fel håll** coupling.

## 5. Duplicering

### Signal

Liknande eller identisk kod finns på flera ställen.

### Frågor innan åtgärd

- Representerar kopiorna faktiskt **samma kunskap/regel**, eller råkar de bara se lika ut idag?
- Ändras de av samma skäl och behöver de hållas synkroniserade?
- Är variationen stabil nog för en gemensam abstraktion?
- Blir den gemensamma lösningen enklare än dupliceringen?

### Högvärdig duplicering att åtgärda

Samma affärsregel, validering, protokolltolkning eller transformationslogik som måste hållas konsekvent på flera ställen.

### Duplicering som kan accepteras

Små likheter i två oberoende domäner där en gemensam abstraction skulle skapa coupling eller många parametrar/flags.

## 6. Stora filer, klasser och funktioner

Storlek är en **screening-signal**, aldrig ett självständigt skäl till en finding.

Sök efter ytterligare evidens:

- flera förändringsorsaker,
- låg cohesion,
- många oberoende beroenden,
- svår isolerad testning,
- djup eller oöverskådlig kontrollflödeslogik,
- flera begreppsnivåer blandas,
- orelaterade delar måste förstås samtidigt.

Lämna en stor enhet orörd när den är sammanhållen, vältestad, begripligt organiserad och en uppdelning främst skulle öka navigering eller indirektion.

## 7. Långa och komplexa funktioner

### Signal

Det är svårt att beskriva funktionen på en abstraktionsnivå eller att förutsäga dess vägar och sidoeffekter.

### Evidens

- djup nesting,
- många oberoende branches,
- flera tidiga/mutabla tillstånd som påverkar senare logik,
- blandning av policy och mekanik,
- flera sidoeffekter,
- samma funktion validerar, transformerar, persisterar och rapporterar.

### Åtgärd

Förenkla kontrollflöde, extrahera namngivna koncept, skilj ren beräkning från sidoeffekter. Extrahera inte mikrofunktioner som bara flyttar svårigheten och gör läsningen hoppig.

## 8. Namngivning och API-begriplighet

### Signal

Koden kräver att läsaren känner till implementationen för att förstå vad ett API eller en symbol betyder.

### Evidens

- generiska namn (`data`, `handle`, `process`, `manager`) döljer domänbegrepp,
- booleska parametrar vars betydelse inte framgår vid call site,
- samma begrepp har flera namn eller samma namn betyder flera saker,
- metodnamn lovar mindre eller mer än metoden faktiskt gör,
- ordningen på parametrar är lätt att förväxla.

### Åtgärd

Prioritera domänspråk, tydliga typer/value objects eller små API-justeringar. Undvik massrenaming med stor diff om nyttan är låg.

## 9. Primitive obsession och svaga domänmodeller

### Signal

Viktiga domänbegrepp representeras som generiska strängar/tal/maps så att regler upprepas vid många call sites.

### Evidens

- samma validering av id, pengar, datumintervall eller status görs på flera ställen,
- ogiltiga kombinationer kan uttryckas fritt,
- många parametrar av samma primitiva typ är lätta att blanda ihop.

### Avvägning

Introducera starkare typer när de kapslar verkliga regler eller eliminerar fel. Skapa inte value objects för varje trivialt fält utan tydlig nytta.

## 10. Long parameter list / data clumps

### Signal

Samma grupp parametrar färdas tillsammans eller en funktion kräver så många oberoende uppgifter att dess ansvar blir oklart.

### Evidens

- samma 3–5 värden skickas tillsammans genom flera lager,
- parametrarna formar ett tydligt domänbegrepp,
- call sites är svåra att läsa eller lätta att anropa fel.

### Motbevis

Ett parameterobjekt som bara gömmer en enda call site och introducerar ny indirektion kan vara sämre.

## 11. Feature envy / felplacerat ansvar

### Signal

En metod använder mer data/beteende från en annan modul än från sin egen och implementerar i praktiken den andras ansvar.

### Evidens

- många getters från ett annat objekt följs av domänberäkningar,
- samma externa datastruktur tolkas på flera platser,
- ändringar av den andra typen kräver ofta ändring här.

Flytta ansvar endast när det förbättrar ägarskap och beroenderiktning; undvik att skapa cirklar.

## 12. Shotgun surgery och divergent change

### Shotgun surgery

En liten konceptuell ändring kräver små ändringar i många filer. Leta efter saknad central regel, läckande representation eller för svaga modulgränser.

### Divergent change

En modul ändras ofta av många helt olika skäl. Leta efter sammanblandade ansvar.

Historisk ändringsdata är stark evidens när den finns, men strukturell evidens i koden kan användas när historik saknas.

## 13. Dead code och spekulativ generalitet

### Dead code

Ta bort kod när det finns rimlig evidens att den inte används och återställning är säker via versionshistorik. Var försiktig med reflection, plugin-registrering, konfiguration, serialization och externa entrypoints.

### Spekulativ generalitet

Abstraktioner, extension points och interfaces utan faktisk användning eller realistisk variationspunkt kan öka kostnaden. Föreslå förenkling när abstraktionen gör flödet svårare att förstå än konkret kod.

## 14. Onödig komplexitet och överabstraktion

### Signal

Lösningen har fler koncept, lager eller indirektioner än problemet kräver.

### Evidens

- en enkel operation passerar genom många delegating layers,
- interfaces har en enda stabil implementation och saknar test-/boundary-nytta,
- factories/builders används utan konstruktionskomplexitet,
- generic frameworks ersätter några få tydliga branches,
- återanvändning kräver flags och specialfall som gör abstraktionen svårare än kopiorna.

Förenkling är en fullvärdig refaktorering. Att ta bort ett pattern kan vara bättre än att införa ett.

## 15. Testbarhet

### Signal

Det är svårt att verifiera viktig logik snabbt och isolerat.

### Evidens

- ren affärslogik är hårt bunden till databas, klocka, nätverk eller global state,
- tester kräver full appstart för små regler,
- nondeterminism saknar kontrollerbar seam,
- komponenter har för många beroenden,
- sidoeffekter och beräkning är sammanvävda.

Refaktorera för testbarhet när det samtidigt förbättrar design eller minskar regressionsrisk; skapa inte abstractions enbart för mocking om enklare teststrategi finns.

## 16. Felhantering och kontrollflöde

### Signal

Fel behandlas inkonsekvent eller transporteras på sätt som gör normalflödet svårbegripligt.

### Evidens

- exceptions fångas och ignoreras,
- samma fel översätts olika i olika lager,
- `null`/sentinel-värden används med oklar semantik,
- logging och användarfel blandas med domänbeslut,
- retry/timeout/logik dupliceras.

Bedöm felhantering som kodkvalitet när fokus är struktur. Observerbart felbeteende/API-kontrakt är funktionell/UX-förändring och ska märkas som sådan.

## 17. Abstraktionsnivåer

Kod är svårare att förstå när hög nivå (”skapa order”) blandas med låg nivå (SQL, bytes, HTTP-headerformat) i samma flöde.

Föredra att en funktion eller modul huvudsakligen arbetar på en begriplig nivå. Undvik dock ceremoniella wrappers som bara byter namn på ett enradigt anrop utan att skapa en meningsfull boundary.

## 18. Prioriteringssignal för findings

En finding blir mer prioriterad när flera av följande gäller:

- problemet orsakar eller riskerar konkreta fel,
- koden ändras ofta,
- problemet blockerar andra förbättringar,
- det påverkar flera team/moduler/call sites,
- testbarheten är låg i kritisk logik,
- en liten förändring ger stor strukturell hävstång,
- evidensen är tydlig och åtgärden kan göras inkrementellt.

Den blir mindre prioriterad när:

- problemet främst är estetiskt,
- koden är stabil och sällan rörd,
- evidensen är svag,
- åtgärden kräver stor rewrite,
- föreslagen abstraction ökar indirektion mer än den minskar komplexitet.

## 19. Finding-format: rekommenderad evidens

När heuristikerna används bör en finding minst kunna svara på:

- **Vad:** vilket konkret problem observeras?
- **Var:** vilka filer/symboler berörs?
- **Varför:** vilken faktisk kostnad eller risk skapar det?
- **Evidens:** vilka kodobservationer stödjer slutsatsen?
- **Motargument:** finns skäl att lämna det orört?
- **Förslag:** minsta rimliga förbättring?
- **Klassificering:** refaktorering, funktionell förändring eller UX-förändring?
- **Verifiering:** hur vet vi att ändringen blev rätt?

## 20. Anti-dogmatiska regler

Kodförbättraren ska uttryckligen kunna komma fram till **ingen åtgärd**.

Den ska inte:

- sätta maxgränser för rader som universell regel,
- kräva en klass per ansvar eller interface per dependency,
- eliminera all duplicering oavsett semantik,
- behandla SOLID som poängsystem,
- skapa fler filer som ett självändamål,
- kalla ren stilpreferens för teknisk skuld,
- anta att modernare syntax/ramverk automatiskt är bättre,
- optimera för test mocks framför begriplig produktionskod.
