# Referensscenarier – kodkvalitets- och refaktoreringsheuristiker

Dessa fall verifierar att samma signal bedöms efter kontext och konsekvens i stället för mekaniska trösklar.

## CQH-01 – Stor fil med flera ansvar bör delas

**Givet:** `OrderService` är 900 rader och innehåller prissättning, SQL, e-postutskick och PDF-rendering. Metodgrupperna använder olika beroenden och kan testas oberoende.

**Förväntat:** Finding för ansvarssammanblandning/låg cohesion med högre evidens än själva radantalet. Rekommendera stegvis separation av tydliga ansvar.

**Underkänt om:** Motiveringen är endast att filen är över ett visst antal rader.

## CQH-02 – Stor sammanhållen fil lämnas orörd

**Givet:** En 850-raders parser implementerar ett sammanhållet protokoll, är vältestad, har tydliga interna sektioner och ändras som en enhet.

**Förväntat:** Storleken noteras högst som signal men ingen refaktoreringsfinding skapas utan annan evidens.

**Underkänt om:** Filen delas enbart för att den är lång.

## CQH-03 – Duplicerad affärsregel centraliseras

**Givet:** Samma momsregel finns i checkout, fakturering och batch-export och måste ändras samtidigt vid nya regler.

**Förväntat:** Högvärdig dupliceringsfinding; gemensamt ägarskap för regeln rekommenderas.

**Underkänt om:** Kopiorna betraktas som ofarliga enbart eftersom implementationerna är korta.

## CQH-04 – Liknande kod i oberoende domäner får vara duplicerad

**Givet:** Två små formatteringsfunktioner råkar se lika ut men hör till två oberoende protokoll och har redan börjat divergera.

**Förväntat:** Ingen gemensam abstraction om den skulle koppla samman protokollen eller kräva flags.

**Underkänt om:** DRY tillämpas mekaniskt.

## CQH-05 – Persistence läcker in i domänlogik

**Givet:** En prissättningsregel bygger SQL, öppnar transaktion och tolkar databassvar mitt i beräkningen.

**Förväntat:** Finding för SoC/coupling/testbarhet. Rekommendera boundary mellan datainhämtning och ren prissättningslogik.

**Underkänt om:** Lösningen automatiskt inför flera lager/interfaces utan att först välja minsta meningsfulla seam.

## CQH-06 – Orkestrering är legitimt ansvar

**Givet:** En use-case-handler anropar tre tydliga tjänster i sekvens men innehåller nästan ingen egen policy eller infrastrukturlogik.

**Förväntat:** Ingen finding för “flera dependencies” i sig; orchestration kan vara ett sammanhållet ansvar.

**Underkänt om:** Den delas upp enbart för dependency-antal.

## CQH-07 – Komplex funktion förenklas efter verklig kontrollflödesrisk

**Givet:** En 70-raders funktion har sex nästlade branches, muterar flera flaggor och blandar validering, beräkning och persistence.

**Förväntat:** Finding för komplexitet/blandade ansvar; rekommendera kontrollflödesförenkling och separation av sidoeffekter.

**Underkänt om:** Åtgärden bara extraherar många mikrofunktioner utan att minska mental modell eller branches.

## CQH-08 – Lång men linjär algoritm behöver inte delas

**Givet:** En 120-raders implementation av ett väldokumenterat checksum-algoritmsteg är linjär, ren och vältestad.

**Förväntat:** Ingen finding enbart baserat på funktionslängd.

**Underkänt om:** En godtycklig maxlängd används.

## CQH-09 – Vagt API förbättras

**Givet:** `process(data, true, false)` används på många ställen och två booleska parametrar styr fakturering respektive notifiering.

**Förväntat:** Finding för API-begriplighet/boolean blindness. Föreslå tydligare API med namngiven semantik.

**Underkänt om:** Endast intern implementation städas medan call-site-risken lämnas obehandlad.

## CQH-10 – Value object är motiverat

**Givet:** Valuta + belopp skickas som separata primitives genom många lager och validering av valuta upprepas.

**Förväntat:** Överväg ett `Money`-liknande domänbegrepp eftersom det kapslar invariant och minskar fel.

**Underkänt om:** Primitive obsession ignoreras trots upprepad regel och ogiltiga kombinationer.

## CQH-11 – Value object är överdesign

**Givet:** En intern flagga används på ett ställe, har ingen validering och riskerar inte att förväxlas.

**Förväntat:** Ingen wrapper/value object enbart för “starkare typer”.

**Underkänt om:** Varje primitive automatiskt kapslas.

## CQH-12 – Feature envy flyttas när ägarskap blir tydligare

**Givet:** `InvoiceRenderer` hämtar 12 fält från `Invoice` och räknar själv ut totalsumma/rabatt på samma sätt som två andra callers.

**Förväntat:** Finding om felplacerad domänregel; överväg att flytta beräkningen till lämpligt domänägarskap eller en gemensam domäntjänst.

**Underkänt om:** Flytt sker utan att kontrollera cykler eller domänansvar.

## CQH-13 – Dead code kräver dynamisk försiktighet

**Givet:** En metod har inga statiska referenser men namnet finns i plugin-konfiguration och laddas via reflection.

**Förväntat:** Ingen dead-code-radering innan dynamisk entrypoint verifierats.

**Underkänt om:** “0 references” behandlas som bevis.

## CQH-14 – Spekulativ abstraction tas bort

**Givet:** `PaymentStrategyFactory -> PaymentStrategy -> DefaultPaymentStrategy` har en enda implementation sedan flera år och inga externa boundaries eller tester behöver interfacet.

**Förväntat:** Kandidat för förenkling om inga realistiska variationer finns.

**Underkänt om:** Pattern bevaras enbart för att Strategy anses “bra design”.

## CQH-15 – Testbarhet förbättras med liten seam

**Givet:** En rabattregel anropar systemklockan direkt på flera ställen och tester är intermittenta runt datumgränser.

**Förväntat:** Introducera minsta kontrollerbara tids-seam eller ren parameterisering som förbättrar determinism.

**Underkänt om:** Hela arkitekturen byggs om för att mocka klockan.

## CQH-16 – Stabil legacy lämnas orörd

**Givet:** Äldre kod är ovanligt skriven men vältestad, stabil, sällan ändrad och isolerad bakom ett tydligt API.

**Förväntat:** Låg eller ingen prioritet om ingen konkret ändringskostnad/risk finns.

**Underkänt om:** Stilmodernisering föreslås som hög prioritet.
