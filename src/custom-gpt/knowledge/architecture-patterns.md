# Arkitektur- och design pattern-heuristiker

Detta dokument hjälper Kodförbättraren att förbättra struktur utan pattern-driven overengineering. Utgångspunkten är alltid ett observerat problem, dess konsekvens och den minsta förändring som ger tillräcklig förbättring.

## 1. Grundregel: problem före pattern

Nämn inte ett design pattern som rekommendation förrän följande är tydligt:

1. vilket konkret problem som finns,
2. vilken evidens som visar problemet,
3. vilken egenskap i lösningen som behövs,
4. vilka enklare alternativ som finns,
5. varför ett pattern ger bättre trade-off än dessa alternativ.

Ett pattern är ett verktyg och ett gemensamt språk – inte ett kvalitetsmål.

## 2. Modul- och lagergränser

Bedöm gränser utifrån ansvar, stabilitet och beroenderiktning. En bra gräns gör det möjligt att förstå, testa och förändra ett område utan oproportionerlig kunskap om andra områden.

### Starka signaler på dåliga gränser

- domänlogik importerar konkreta databas-, HTTP- eller UI-detaljer,
- interna representationer läcker över flera moduler,
- cirkulära beroenden,
- en liten förändring kräver koordinering över många lager,
- samma regel implementeras i flera lager,
- UI-komponenter känner till persistence- eller transportdetaljer,
- modulers publika API:n exponerar fler implementationdetaljer än användare behöver.

### Motbevis

- enkel kodbas där ett extra lager främst skapar indirektion,
- stabil teknisk integration där abstraktion saknar verklig variationspunkt,
- lokalt sammanhållen feature-modul som legitimt kombinerar flera tekniska detaljer bakom ett tydligt publikt API.

Föreslå inte fler lager bara för att uppnå en schematisk arkitekturbild.

## 3. Ports and Adapters / Hexagonal Architecture

Använd principerna när kärnlogik behöver isoleras från instabila eller utbytbara integrationsdetaljer, särskilt när testbarhet eller flera adapters är ett faktiskt behov.

### Motiverat när

- domän/use-case-logik är central och bör kunna testas utan extern I/O,
- flera adapters finns eller en realistisk variationspunkt är nära förestående,
- infrastrukturdetaljer dominerar domänkoden,
- beroenderiktningen behöver vändas för att skydda en stabil kärna.

### Ofta onödigt när

- systemet är litet och huvudsakligen CRUD,
- ett interface bara speglar exakt en implementation utan test- eller variationsnytta,
- varje operation får egna port/interface/adapter-filer utan att komplexitet faktiskt minskar,
- arkitekturen skapar fler hopp än den eliminerar beroenden.

Välj gärna en partiell tillämpning: isolera den del som har verkligt behov i stället för att konvertera hela systemet.

## 4. SOLID som heuristik, inte dogm

### Single Responsibility Principle

Använd när flera förändringsorsaker eller låg cohesion skapar faktisk underhållskostnad. En stor klass kan fortfarande ha ett ansvar.

### Open/Closed Principle

Sök stabila variationspunkter. Inför inte extension mechanisms för hypotetiska framtida behov.

### Liskov Substitution Principle

Var vaksam när subtyper kräver specialfall, kastar `UnsupportedOperationException`, stärker preconditions eller bryter förväntad semantik. Komposition kan vara bättre än arv.

### Interface Segregation Principle

Dela interface när konsumenter tvingas bero på operationer de inte använder. Dela inte bara för att göra interface små.

### Dependency Inversion Principle

Vänd beroenden när en stabil policy annars binds till instabil mekanik. Skapa inte interface runt varje klass; abstraktion ska ligga vid en meningsfull boundary.

## 5. Strategy

### Problem som kan motivera Strategy

- växande villkorslogik väljer mellan flera beteenden,
- beteendena varierar oberoende och testas separat,
- nya varianter läggs till återkommande.

### Enklare alternativ

- liten `switch` med få stabila fall,
- lookup-tabell eller funktion-map,
- ren funktion som parameter.

Inför inte en klasshierarki för två triviala branches.

## 6. State

Motiverat när ett objekts tillåtna beteende varierar tydligt med tillstånd och tillståndsövergångar annars sprids som villkor genom många metoder.

Undvik när en enum + tydlig transition-funktion ger samma begriplighet med mindre indirektion.

## 7. Factory / Abstract Factory

Factory är motiverat när skapande har komplexa regler, behöver kapsla implementationval eller bör separeras från användning. Undvik factories som endast anropar en konstruktor och saknar policy.

Abstract Factory kräver normalt flera relaterade produktfamiljer eller verklig variation; använd inte för framtidssäkring utan evidens.

## 8. Adapter

Motiverat vid faktisk gräns mellan två inkompatibla API:n eller när ett externt API bör kapslas bakom ett internt språk. Det kan också skydda mot leverantörsspecifika typer.

Skapa inte adapters mellan interna moduler som redan delar ett begripligt kontrakt.

## 9. Facade

Motiverat när konsumenter annars behöver koordinera ett komplext subsystem eller känna många interna detaljer. Facaden ska minska konceptuell yta, inte bli en ny `Manager` som samlar alla operationer i systemet.

## 10. Repository

Motiverat när domän/use-case-logik behöver ett stabilt persistence-kontrakt eller när query/persistence-detaljer annars läcker in i kärnlogiken.

Undvik extra repository-lager ovanpå ett ramverk om lagret bara vidarebefordrar identiska CRUD-anrop och inte förbättrar språk, testbarhet eller beroenderiktning.

## 11. Command

Motiverat när operationer behöver behandlas som data: köas, loggas, återspelas, ges undo eller hanteras med gemensam pipeline. Onödigt för vanliga metodanrop utan dessa behov.

## 12. Observer / Publish-Subscribe

Motiverat för lös koppling mellan flera oberoende reaktioner på en händelse. Kontrollera kostnaderna: dold kontrollflöde, ordning, retries, idempotens och felsökning.

För enkel synkron koordinering kan ett direkt anrop vara tydligare.

## 13. Decorator / Middleware / Pipeline

Motiverat för ortogonala, komponerbara beteenden som logging, auth, metrics eller transformationer när de annars dupliceras.

Undvik djupa dekoratörskedjor där ordning är svår att förstå och felsöka.

## 14. Template Method och arv

Template Method kan fungera när en stabil algoritm har ett fåtal tydliga variationspunkter. Föredra ofta komposition när variationerna förändras oberoende eller arvshierarkin börjar få specialfall.

## 15. Dependency Injection

DI är nyttigt när det gör beroenden explicita och möjliggör substitution vid meningsfulla boundaries. Ett DI-container-ramverk är inte ett krav för DI.

Varningssignaler:

- service locator används dolt inne i domänlogik,
- nästan varje klass får ett interface enbart för mocking,
- constructors får många beroenden som egentligen signalerar för stort ansvar.

## 16. Anti-patterns och överdesign

### Pattern cargo cult

Pattern införs för att det är känt eller "best practice", inte för ett verifierat problem.

### Interface explosion

Många enimplementations-interface utan boundary-, test- eller variationsnytta.

### Layer cake

Controller → Service → Manager → Facade → Repository där flera lager bara vidarebefordrar data.

### Generic framework inside the application

Teamet bygger ett generiskt regelsystem, pluginramverk eller mini-framework trots ett litet och stabilt konkret behov.

### Configuration over code

Enkel logik blir metadata/configuration som kräver en interpreter och gör beteendet svårare att följa.

### Inheritance taxonomy

Arv används för kodåteranvändning trots att subtyperna inte är substituerbara eller behöver många overrides/specialfall.

### Premature distributed architecture

Process-, tjänste- eller eventgränser införs utan organisatoriskt, skalningsmässigt eller autonomt behov och skapar nätverks-/driftkomplexitet.

## 17. När ett befintligt pattern bör förenklas eller tas bort

Sök aktivt efter möjligheten att ta bort arkitekturell komplexitet när:

- variationspunkten inte längre finns,
- flera implementationer har blivit en,
- ett lager bara vidarebefordrar,
- abstractionens API är svårare att förstå än implementationen,
- pattern skapar fler filer/hopp men ingen isolation,
- testning kräver omfattande mocks på grund av själva abstraktionen,
- feature-flödet är svårt att följa genom flera generiska extension points.

Förenkla stegvis. Säkerställ först att beteendet är skyddat av tester och att inga externa extension points används.

## 18. Beslutsformat för arkitekturrekommendationer

En arkitektur- eller pattern-finding bör beskriva:

- **Problem:** konkret strukturellt problem.
- **Evidens:** berörda moduler, beroenden och ändringsmönster.
- **Konsekvens:** faktisk kostnad/risk.
- **Minsta rimliga åtgärd:** ofta utan pattern-namn.
- **Pattern/arkitektur (om relevant):** vilket verktyg och vilken egenskap som hjälper.
- **Alternativ:** minst ett enklare alternativ när sådant finns.
- **Trade-offs:** ny indirektion, diffstorlek, migration/testbehov.
- **Avgränsning:** vad som uttryckligen inte ska byggas.

## 19. Arkitekturmål

Målet är inte maximal abstraktion eller "renaste" möjliga arkitektur. Målet är minsta tillräckliga struktur som ger bättre begriplighet, ändringsbarhet, testbarhet och robusthet för det faktiska systemet och dess förväntade förändringstakt.
