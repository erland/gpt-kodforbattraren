# Referensscenarier – arkitektur och design patterns

## AP-S01 – Strategy är motiverat

**Situation:** En prissättningsmotor har sju kundspecifika algoritmer. En växande `switch` innehåller olika regler och varje ny kundvariant ändrar samma funktion.

**Förväntat:** Identifiera varierande beteende och ändringshotspot. Strategy eller funktionbaserad variantmodell är rimlig. Rekommendationen ska förklara varför och jämföra mot enklare lookup/funktionsalternativ.

## AP-S02 – Strategy är onödigt

**Situation:** En formatteringsfunktion har två stabila utdataformat med sex rader kod vardera och inga tecken på fler varianter.

**Förväntat:** Behåll enkel branch/switch. Skapa inte interface + två implementationer bara för att Strategy finns.

## AP-S03 – Befintligt Repository bör förenklas

**Situation:** `UserRepository` vidarebefordrar exakt `findById/save/delete` till frameworkets repository. Ingen domänlogik, ingen alternativ persistence och alla call sites kan använda frameworktypen direkt utan att läcka den in i domänkärnan.

**Förväntat:** Föreslå att pass-through-lagret kan tas bort eller slås ihop, förutsatt att publika beroenden och tester tillåter det. Pattern-namnet är inte ett självändamål.

## AP-S04 – Repository är motiverat

**Situation:** Orderdomänen innehåller SQL-/ORM-querydetaljer och transaction hints inne i use-case-logik. Tester kräver databas för enkla regler.

**Förväntat:** Isolera persistence vid en meningsfull boundary. Repository/port kan vara lämpligt eftersom det förbättrar beroenderiktning och testbarhet.

## AP-S05 – Ports and Adapters delvis, inte överallt

**Situation:** Ett system har komplex betalningsdomän med två betalproviders men en enkel intern admin-CRUD.

**Förväntat:** Använd ports/adapters runt betalningsgränsen där variation och extern I/O finns. Konvertera inte admin-CRUD till full hexagonal struktur utan behov.

## AP-S06 – Interface explosion ska undvikas

**Situation:** 40 serviceklasser har varsitt interface och exakt en implementation. Interfaces finns bara för mocking, trots att tester kan använda fakes vid verkliga boundaries.

**Förväntat:** Identifiera överdesign. Föreslå färre, meningsfulla abstraktioner vid boundaries i stället för mekaniskt interface-per-class.

## AP-S07 – State kan vara motiverat

**Situation:** Ett workflow har åtta tillstånd, olika tillåtna operationer och transition-regler som idag dupliceras i flera `if status == ...`-block.

**Förväntat:** State eller explicit state-machine-modell kan minska spridd policy. Bedöm också om central enum + transition-tabell är enklare.

## AP-S08 – Arv bör ersättas med komposition

**Situation:** Fyra exporter-subklasser override:ar allt fler metoder och två kastar `UnsupportedOperationException` för basklassens operationer.

**Förväntat:** Markera substituerbarhetsproblem och överväg komposition/strategies. Undvik att bara lägga fler abstrakta hooks i hierarkin.

## AP-S09 – Facade är motiverad

**Situation:** Tre konsumenter måste känna till sex interna subsystem och anropa dem i samma ordning för att skapa ett konto.

**Förväntat:** En use-case/facade kan minska publik yta och koordinationsduplicering, men ska vara fokuserad på kontoskapandet och inte bli generell `SystemManager`.

## AP-S10 – Event/PubSub är överdesign

**Situation:** När en lokal preferens sparas ska exakt en cache uppdateras synkront i samma process. Teamet föreslår event bus med retries och event schemas.

**Förväntat:** Rekommendera direkt anrop om inga oberoende subscribers eller asynkrona behov finns. Förklara att eventing skulle öka dold kontrollflow och driftkostnad.

## AP-S11 – Event/PubSub är motiverat

**Situation:** Slutförd order triggar oberoende fakturering, analytics och notifiering, med separata fel-/retry-behov och olika teamägare.

**Förväntat:** Eventdriven koppling kan vara rimlig. Kräv resonemang om idempotens, ordering, retries och observability – inte bara pattern-namnet.

## AP-S12 – Pattern tas bort när variationspunkten försvunnit

**Situation:** En plugin-arkitektur byggdes för fem adapters. Produkten stödjer sedan flera år endast en adapter och extension API:t används inte externt. Flödet går genom factory, registry, plugin loader och adapter interface.

**Förväntat:** Föreslå kontrollerad förenkling och borttagning av obehövlig generell struktur efter verifiering av externa användare och regressionstest.
