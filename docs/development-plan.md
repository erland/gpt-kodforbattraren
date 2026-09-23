# Kodförbättraren – utvecklingsplan

## Projekt

- **Arbetsnamn:** Kodförbättraren
- **Syfte:** En GPT som analyserar befintlig källkod, prioriterar förbättringar och genomför dem säkert och inkrementellt med stöd för både ZIP-baserat arbete och GitHub/PR-baserat arbete.
- **Projektprofil:** `zip_first_advanced`
- **Distributioner:** Chat ZIP och Custom GPT från samma canonical beteende- och capability-kontrakt.
- **Planversion:** 1

## Målbild

Kodförbättraren ska kunna ta emot ett källkodsprojekt som ZIP eller ett GitHub-repository och först göra en strukturerad analys innan kod ändras. Analysen ska täcka kodkvalitet, arkitektur, testbarhet, utvecklarupplevelse och – när projektet innehåller ett användargränssnitt – usability/UX.

Den ska därefter skapa en prioriterad, nedladdningsbar refaktoreringsplan och hålla reda på faktisk status. När användaren säger exempelvis **”Gör nästa steg”** ska GPT:n kunna avgöra nästa lämpliga åtgärd från projektets status, utföra just den förändringen, verifiera resultatet och leverera ett uppdaterat projekt.

I ZIP-läge ska ett komplett uppdaterat projekt levereras som ZIP efter varje genomfört steg. I GitHub-läge ska arbetet ske på branch/PR: om föregående refaktorerings-PR fortfarande är öppen fortsätter GPT:n på den; om den är mergad skapas en ny branch och PR för nästa lämpliga steg.

## Arkitekturprinciper

1. **Canonical instruktion styr beteendet.** Kritiska regler får inte vara beroende av att en Knowledge-fil hittas.
2. **Knowledge används för domänkunskap och heuristiker.** Exempel är code smells, design patterns, arkitekturprinciper, UX-heuristiker och språk-/ramverksspecifika riktlinjer.
3. **Maskinläsbar status är primär statuskälla.** Markdown-status genereras för människor men ska inte vara enda minnet av vad som är genomfört.
4. **Inkrementella förändringar framför rewrites.** Varje steg ska vara så litet att det kan verifieras och återställas separat.
5. **Beteendebevarande refaktorering skiljs från funktionell förändring.** UX-förbättringar och andra beteendeförändringar ska märkas uttryckligen.
6. **Design patterns är verktyg, inte mål.** Ett pattern används endast när det förenklar ansvar, variation eller beroenden.
7. **Tester skyddar riskfylld refaktorering.** Characterization tests kan behöva införas före strukturella förändringar.
8. **Planen är dynamisk.** Blockerare, ny kod eller misslyckade valideringar kan göra att nästa steg avviker från ursprungsordningen.

## Utvecklingssteg

### Steg 1 – Behovs- och konceptanalys

**Mål:** Definiera GPT:ns användningsfall, gränser och centrala arbetsflöden.

**Leverabler:**
- konceptanalys,
- ZIP- och GitHub-flöde,
- analysdimensioner,
- principer för säker refaktorering,
- avgränsning mellan refaktorering och UX-/beteendeförändring.

**Klart när:**
- användningsfallet är tillräckligt stabilt för att planera implementationen,
- centrala verksamhetsval är dokumenterade.

**Status:** Klar.

---

### Steg 2 – Målarkitektur och utvecklingsplan

**Mål:** Välja projektprofil, målarkitektur och en projektspecifik genomförandeordning.

**Leverabler:**
- projektprofil `zip_first_advanced`,
- arkitekturprinciper,
- denna utvecklingsplan.

**Validering:**
- planen innehåller mål och klart-kriterier per steg,
- beroenden är ordnade så att projektet kan byggas inkrementellt,
- distribution, test, hygiene och release ingår.

**Klart när:**
- nedladdningsbar plan finns,
- nästa steg kan påbörjas utan ytterligare arkitekturval.

**Status:** Klar när denna fil levereras.

---

### Steg 3 – Skapa canonical projektstruktur

**Mål:** Skapa första kompletta GPT-projektet och dess grundläggande metadata.

**Leverabler:**
- `README.md`,
- `PROJECT.md`,
- `STATUS.md`,
- `gpt-project.yaml`,
- `project-status.yaml`,
- `docs/development-plan.md`,
- canonical instruktionsträd,
- grundstruktur för Knowledge, schemas, scripts och tester.

**Validering:**
- projektstrukturen följer GPT Byggarens konventioner,
- projektstatus pekar ut nästa faktiska steg.

**Hygiene:**
- inga temporära eller duplicerade filer,
- genererade distributioner hålls separerade från canonical source.

**Klart när:**
- projektet går att återuppta enbart från projekt-ZIP:en,
- en komplett projekt-ZIP har byggts.

**Beroende:** Steg 2.

---

### Steg 4 – Definiera canonical beteendekontrakt

**Mål:** Beskriva hur GPT:n alltid ska arbeta, oavsett runtime.

**Leverabler:**
- instruktioner för analys före ändring,
- regler för prioritering,
- regler för ”Gör nästa steg”,
- regler för små, verifierbara förändringar,
- regler för refactoring kontra beteendeförändring,
- regler för när GPT:n ska avstå från refaktorering.

**Tester:**
- scenarios där GPT:n inte börjar ändra kod innan initial analys,
- scenarios där ett för stort steg delas upp,
- scenarios där onödig refaktorering avvisas.

**Klart när:**
- kärnflödet kan förstås från canonical instruktionen utan Knowledge-beroende,
- relevanta beteendetester passerar.

**Beroende:** Steg 3.

---

### Steg 5 – Modell för findings, plan och projektstatus

**Mål:** Göra analysresultat och genomförandestatus maskinläsbara och robusta mellan steg.

**Leverabler:**
- schema för findings,
- schema för refaktoreringsplan,
- schema för arbetsstatus,
- statusfält för planerade/pågående/klara/blockerade steg,
- koppling mellan finding och åtgärdssteg,
- stöd för aktuell ZIP-bas eller GitHub branch/PR.

**Validering:**
- exempelstatus kan valideras mot schema,
- nästa steg kan härledas från status utan samtalshistorik.

**Klart när:**
- ”Gör nästa steg” kan baseras på projektfiler i stället för implicit minne.

**Beroende:** Steg 4.

---

### Steg 6 – Kodkvalitets- och refaktoreringsheuristiker

**Mål:** Ge GPT:n konsekventa principer för vad som bör upptäckas och hur det ska bedömas.

**Leverabler:**
- Knowledge om Separation of Concerns och Single Responsibility,
- cohesion/coupling,
- duplicering,
- stora filer/klasser/funktioner utan mekaniska radgränser,
- code smells,
- abstractionsnivåer,
- namngivning och API-begriplighet,
- testbarhet,
- dead code och onödig komplexitet.

**Tester:**
- exempel där stor fil ska delas,
- exempel där stor fil är sammanhållen och ska lämnas orörd,
- exempel med duplicering och ansvarsläckage.

**Klart när:**
- samma typ av problem bedöms konsekvent i referensfall.

**Status:** Klar.

**Beroende:** Steg 4.

---

### Steg 7 – Arkitektur- och design pattern-kunskap

**Mål:** Göra GPT:n kapabel att förbättra struktur utan pattern-driven overengineering.

**Leverabler:**
- principer för lager/moduler/ports-and-adapters där relevant,
- SOLID som heuristik, inte dogm,
- vägledning för vanliga design patterns,
- anti-patterns och signaler på överdesign,
- regler för att förenkla eller ta bort patterns.

**Tester:**
- pattern är motiverat,
- pattern är onödigt,
- befintligt pattern bör förenklas.

**Klart när:**
- rekommendationer utgår från problem och trade-offs snarare än pattern-namn.

**Beroende:** Steg 6.

---

### Steg 8 – Test- och säkerhetsstrategi för refaktorering

**Mål:** Skydda befintligt beteende vid riskfyllda förändringar.

**Leverabler:**
- regler för baseline-build/test/lint,
- characterization tests,
- regressionstestning,
- riskbaserad testnivå,
- hantering när projektets tester redan är röda,
- rollback-/stoppkriterier.

**Tester:**
- projekt utan tester,
- projekt med befintliga fel,
- refaktorering av central affärslogik,
- rent kosmetisk förändring.

**Klart när:**
- GPT:n kan avgöra när testförstärkning måste föregå refaktorering.

**Beroende:** Steg 5 och 6.

---

### Steg 9 – UX- och usability-analys

**Mål:** Låta GPT:n identifiera förbättringar i användarupplevelsen utan att blanda ihop dem med ren refaktorering.

**Leverabler:**
- usability-heuristiker,
- informationsarkitektur och navigering,
- feedback/loading/empty/error states,
- formulär och validering,
- tillgänglighet,
- mobil användbarhet,
- konsekvens och kognitiv belastning,
- märkning av förslag som ändrar observerbart beteende.

**Tester:**
- ren kodförbättring,
- ren UX-förbättring,
- kombinerad förändring som bör delas upp.

**Klart när:**
- UX-förslag kan prioriteras separat och aldrig maskeras som beteendebevarande refactoring.

**Beroende:** Steg 4.

---

### Steg 10 – Initial analys och prioriteringsmodell

**Mål:** Definiera den analys som alltid föregår en refaktoreringsserie.

**Leverabler:**
- inventering av projektstruktur och teknikstack,
- findings med evidens och berörda filer,
- severity/risk/nytta/kostnad,
- rekommenderad prioritering,
- beroenden mellan åtgärder,
- sådant som medvetet inte bör åtgärdas,
- diagnostisk baseline för maintainability, architecture, testability, DX och vid behov UX/accessibility.

**Tester:**
- små och stora projekt,
- backend-only,
- frontend-only,
- fullstack,
- projekt där få förbättringar är motiverade.

**Klart när:**
- GPT:n kan producera en konsekvent analys utan att börja modifiera projektet.

**Beroende:** Steg 6–9.

---

### Steg 11 – Generering av refaktoreringsplan och nästa steg

**Mål:** Omvandla findings till en säker, genomförbar plan.

**Leverabler:**
- nedladdningsbar `refactoring-plan.md`,
- maskinläsbar plan,
- länkning finding → steg,
- små steg med verifiering och klart-kriterier,
- dynamisk next-step-rekommendation,
- regler för blockerare och omplanering.

**Tester:**
- ”Gör nästa steg”,
- misslyckad test efter ett steg,
- nytt blockerande problem,
- redan löst steg,
- ändrad kodbas sedan ursprungsanalysen.

**Klart när:**
- nästa steg kan väljas från faktisk status och inte enbart sekventiellt stegnummer.

**Beroende:** Steg 5 och 10.

---

### Steg 12 – ZIP-arbetsflöde

**Mål:** Göra ZIP till ett fullvärdigt arbetsläge.

**Leverabler:**
- regler för import och säker uppackning,
- bevarande av projektstruktur,
- exkludering av irrelevanta build/cache-filer när lämpligt,
- uppdatering av status efter varje steg,
- komplett uppdaterad projekt-ZIP efter varje genomfört steg,
- återupptagning från tidigare levererad ZIP.

**Tester:**
- första ZIP,
- uppdaterad ZIP från föregående steg,
- monorepo,
- ZIP med binära artefakter/buildkataloger,
- återupptagning i ny konversation.

**Klart när:**
- användaren kan genomföra en hel refaktoreringsserie genom att bara återanvända senaste ZIP.

**Beroende:** Steg 5 och 11.

---

### Steg 13 – GitHub repository- och PR-arbetsflöde

**Mål:** Göra GitHub till ett fullvärdigt alternativ till ZIP.

**Leverabler:**
- repository-inspektion,
- default branch-synk,
- branch-namngivning,
- commit- och PR-konventioner,
- fortsätt på öppen refaktorerings-PR,
- skapa ny PR efter merge,
- hantering av stängd men ej mergad PR,
- konflikthantering och begränsad omanalys vid drift i kodbasen.

**Tester:**
- ingen tidigare PR,
- föregående PR öppen,
- föregående PR mergad,
- föregående PR stängd utan merge,
- default branch ändrad sedan planen skapades.

**Klart när:**
- GPT:n konsekvent väljer rätt branch/PR-beteende och dokumenterar statusen.

**Beroende:** Steg 5 och 11.

---

### Steg 14 – Språk- och ramverksspecifika profiler

**Mål:** Förbättra precisionen utan att göra kärninstruktionen beroende av en viss teknikstack.

**Första profiler:**
- Java/Quarkus,
- JavaScript/TypeScript,
- React,
- generell backend/webb.

**Leverabler:**
- teknikdetektion,
- ramverksspecifika heuristiker,
- build/test/lint-kommandon som kan härledas från projektet,
- regler för att inte modernisera dependencies utan tydligt motiv.

**Tester:**
- minst ett referensprojekt per första profil.

**Klart när:**
- samma canonical arbetsflöde fungerar över flera teknikstackar.

**Beroende:** Steg 8 och 10.

---

### Steg 15 – Rapporter, status och användarupplevelse i GPT:n

**Mål:** Göra arbetsflödet lätt att förstå och fortsätta med korta instruktioner.

**Leverabler:**
- analysrapport,
- `refactoring-plan.md`,
- `STATUS.md`,
- standardiserad sammanfattning efter genomfört steg,
- tydlig rad med nästa rekommenderade steg,
- stöd för uttryck som ”Gör nästa steg”, ”fortsätt”, ”vad är nästa steg?”.

**Klart när:**
- användaren kan driva projektet framåt utan att förstå intern statusmodell.

**Beroende:** Steg 11–13.

---

### Steg 16 – Evals och end-to-end-scenarier

**Mål:** Säkerställa konsekvent beteende i realistiska projektflöden.

**Leverabler:**
- eval cases för analyskvalitet,
- eval cases för prioritering,
- eval cases för överrefaktorering,
- eval cases för testförstärkning före riskfylld ändring,
- E2E ZIP-serie över flera steg,
- E2E GitHub/PR-serie över flera steg,
- återupptagningsscenario.

**Validering:**
- blockerande beteenden testas explicit,
- regressionsfall sparas som referensfall.

**Klart när:**
- kärnflödena kan köras reproducerbart och ger förväntat resultat.

**Beroende:** Steg 12–15.

---

### Steg 17 – Chat ZIP-runtime

**Mål:** Bygga och validera Chat ZIP-distributionen.

**Leverabler:**
- Chat ZIP-startinstruktion,
- nödvändiga canonical/Knowledge-filer,
- minimerade runtime-beroenden,
- runtime-paritetskontroll mot canonical kontrakt.

**Validering:**
- Chat ZIP kan startas från ren konversation,
- kärnflödet kräver få filhopp,
- kritiska beteenden fungerar utan dold projekthistorik.

**Klart när:**
- Chat ZIP-distributionen validerar och klarar relevanta E2E-fall.

**Beroende:** Steg 16.

---

### Steg 18 – Custom GPT-kompilering

**Mål:** Skapa Custom GPT-versionen från samma canonical kontrakt.

**Leverabler:**
- kompilerad systeminstruktion inom plattformsgränser,
- utvalda Knowledge-filer,
- capability-dokumentation,
- kända skillnader mot Chat ZIP.

**Validering:**
- instruktionens storlek och Knowledge-struktur är plattformskompatibla,
- inga kritiska beteenden försvinner i kompileringen,
- runtime parity dokumenteras.

**Klart när:**
- Custom GPT-paketet kan konfigureras utan manuella designbeslut.

**Beroende:** Steg 16.

---

### Steg 19 – GitHub Actions CI och release-byggning

**Mål:** Automatisera kvalitetssäkring och distributionsbyggen.

**Leverabler:**
- CI vid push/PR,
- lint/schema/test/build-validering,
- release-workflow,
- versionering från GitHub Release-taggen,
- byggda Chat ZIP- och Custom GPT-artefakter vid release.

**Klart när:**
- en PR verifierar projektet automatiskt,
- en GitHub Release bygger distributionsartefakter med taggens version.

**Beroende:** Steg 17 och 18.

---

### Steg 20 – Release readiness, hygiene och första stabila release

**Mål:** Göra projektet redo för faktisk användning.

**Leverabler:**
- full project hygiene,
- release-readiness-rapport,
- runtime-paritetsrapport,
- slutlig dokumentation,
- distributionsartefakter,
- första stabila releasekandidat.

**Validering:**
- lint, schemas, tester och E2E passerar,
- båda distributionerna validerar,
- inga blockerande hygiene-problem finns,
- kända begränsningar är dokumenterade.

**Klart när:**
- projektet uppfyller GPT Byggarens releasekriterier och kan taggas som första stabila version.

**Beroende:** Steg 19.

## Dynamiska korrigeringssteg

Planen är vägledande. Om ett steg upptäcker ett blockerande fel, bristande runtime-paritet, ett schemafel, testregression eller ett hygiene-problem ska ett korrigeringssteg prioriteras före nästa planerade steg. Ett steg får också delas om diffen eller risken blir för stor.

## Första implementation efter denna plan

Nästa rekommenderade steg är **Steg 3 – Skapa canonical projektstruktur**. Det är då den första kompletta projekt-ZIP:en ska skapas. Därefter ska varje genomfört steg avslutas med verifierad status, hygiene-bedömning och en ny komplett projekt-ZIP.


---

### Steg 21 – GPT Byggaren 1.5-kontrakt och modellrobust kärna

**Mål:** Migrera Kodförbättrarens canonical kontrakt till GPT Byggaren 1.5.0 utan att ändra domänbeteendet.

**Leverabler:**
- capability-, artifact-, workspace/state- och tool-kontrakt,
- stateful modellrobust profil,
- operativ kärna och auktoritativ status,
- modellkompatibilitetsscenarier,
- explicit bedömning av fem registrerade runtimes.

**Klart när:**
- befintlig CI är grön,
- kärnflöden för ZIP/GitHub är oförändrade,
- 1.5-kontrakten är lintbara och spårbara.

### Steg 22 – Anpassa distributioner och bygg OpenCode

**Mål:** Låta Chat, Custom GPT och OpenCode härledas från samma 1.5-kontrakt.

**Leverabler:**
- runtime-kontrakt i aktiva distributioner,
- verifierad Custom GPT-kompilering med 1.5-kärnan,
- OpenCode-distribution med AGENTS.md, runtime-contract och relevant skill/workspace-stöd,
- tydlig dokumentation av värdverktyg kontra paketerade verktyg.

**Klart när:**
- Chat, Custom GPT och OpenCode validerar,
- kritiska kärnregler finns i alla aktiva runtimes.

### Steg 23 – Generaliserad runtime parity och release readiness

**Mål:** Generalisera parity/readiness till GPT Byggaren 1.5-modellen.

**Leverabler:**
- parity för behavior, capability, artifact, workspace_state och tool,
- explicit status för alla fem runtimes,
- release-readiness som blockerar vid drift mellan runtimebeslut, CI och release.

**Klart när:**
- tre aktiva runtimes är verifierade,
- reducerade/inaktiva runtimes har explicit motivering,
- parity/readiness är blockerande CI-gates.

### Steg 24 – Slutvalidera migreringen och releasekedjan

**Mål:** Verifiera full regression, distributionsbyggen, CI/release-paritet och releaseartefakter.

**Klart när:**
- alla aktiva distributioner och gates passerar,
- dokumentationen beskriver 1.5-arkitekturen,
- projektet är redo att mergeas och releasas.
