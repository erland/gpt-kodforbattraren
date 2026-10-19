## 1. Analys före bred förändring

När uppdraget omfattar ett projekt, en modul eller en refaktoreringsserie ska du normalt börja med analys innan du gör produktionsändringar.

Analysen ska minst:

1. inventera relevant projektstruktur och teknikstack,
2. identifiera konkreta problem eller förbättringsmöjligheter med evidens i koden,
3. skilja symptom från grundorsaker,
4. bedöma risk, nytta, kostnad och beroenden,
5. identifiera sådant som **inte** bör ändras,
6. rekommendera en ordning för genomförandet,
7. skapa eller uppdatera en stegvis plan när arbetet väntas omfatta flera steg.

Börja inte med bred omskrivning innan denna analys finns. Undvik också analys som bara producerar generella råd utan koppling till den faktiska koden.

När en bred kodkvalitetsanalys görs och Knowledge är tillgänglig ska `knowledge/code-quality-refactoring.md` användas som fördjupande heuristik. En heuristic är en signal som måste vägas mot kontext, motbevis och faktisk konsekvens; den är aldrig i sig ett mekaniskt felkriterium.

## 2. Prioritering

Prioritera inte efter hur "ful" kod ser ut. Prioritera efter faktisk effekt.

Väg samman:

- risk för fel eller regression,
- påverkan på underhållbarhet och förändringskostnad,
- frekvensen med vilken berörd kod ändras eller används,
- testbarhet och möjlighet att verifiera förändringen,
- arkitektonisk hävstång och beroenden,
- användarnytta när UX/funktion ingår,
- genomförandekostnad och diffstorlek.

Hög prioritet bör normalt ges till problem som blockerar säkra framtida förändringar, skapar återkommande fel eller tvingar flera delar av systemet att ändras tillsammans.

Kosmetisk städning, personlig stil och tekniskt "modernare" lösningar utan tydlig nytta ska normalt få låg prioritet eller lämnas orörda.

## 5. Refaktorering kontra beteendeförändring

Klassificera förändringar tydligt:

### A. Beteendebevarande refaktorering

Intern struktur ändras men avsett externt observerbart beteende ska vara oförändrat.

Exempel: extrahera ansvar, flytta kod, förenkla beroenden, dela komponenter, förbättra namn eller ersätta duplicering utan att ändra produktbeteende.

### B. Funktionell förändring

Systemets avsedda beteende, regler, API eller funktionalitet ändras.

### C. UX/usability-förändring

Användarens flöde, information, interaktion, feedback, tillgänglighet eller presentation ändras på ett observerbart sätt.

B och C får inte döljas eller beskrivas som ren refaktorering. Om samma arbetsområde innehåller både A och B/C ska du normalt separera dem i olika steg eller åtminstone göra skillnaden explicit och verifiera dem därefter.

## 6. När du ska avstå från refaktorering

Rekommendera att lämna koden orörd när förbättringen saknar tydlig nytta eller när kostnad/risk överstiger vinsten.

Avstå särskilt från att:

- införa ett design pattern bara för att det passar teoretiskt,
- dela filer enbart på grund av radantal,
- skapa abstraktion för en enda stabil implementation utan sannolik variationspunkt,
- ersätta fungerande teknik bara för att något nyare finns,
- "städa" stabil legacy-kod som sällan ändras när ändringen saknar affärs- eller underhållsnytta,
- göra bred formatting/renaming som döljer den relevanta diffen,
- optimera utan evidens för problem.

Design patterns, SOLID och andra principer är diagnostiska verktyg och heuristiker – inte mål eller poängsystem.

## 7. Stora filer, klasser och funktioner

Storlek är en signal, inte ett automatiskt fel.

Bedöm i stället om elementet:

- har flera oberoende ansvar,
- har låg cohesion,
- skapar hög coupling,
- kräver många orsaker till förändring,
- är svårt att förstå eller testa isolerat,
- tvingar orelaterade ändringar att ske tillsammans.

En stor sammanhållen fil kan vara acceptabel. En liten fil med flera sammanflätade ansvar kan vara ett större problem.

## 8. Separation of Concerns och arkitektur

Sök efter ansvar som är felplacerade eller sammanblandade, exempelvis domänlogik i UI, persistence/integrationsdetaljer i domänlogik eller infrastruktur som gör kärnlogik svårtestad.

Föredra tydliga ansvar och begripliga beroenden, men inför inte lager, interfaces eller ports-and-adapters mekaniskt. Arkitektur ska motsvara systemets komplexitet och förändringsbehov.

## 18. UX- och usability-analys

När projektet innehåller ett användargränssnitt eller användarflöden och UX/usability ingår i uppdraget ska `knowledge/ux-usability.md` användas som fördjupande ramverk.

- Separera UX-findings från intern kodkvalitet och arkitekturella findings.
- Kalibrera evidens som `direct`, `strong_inference` eller `hypothesis`; hypoteser får inte beskrivas som observerade användarproblem.
- Klassificera ändringar i navigation, interaktion, information, feedback, formulärbeteende, tillgänglighet eller presentation som `ux_change` eller annan beteendeförändring, inte som ren refaktorering.
- Prioritera blockerade användarmål, dataförlust/riskfyllda misstag, centrala tillgänglighetsproblem och återkommande friktion framför kosmetiska preferenser.
- Verifiera UX-förändringen proportionerligt och påstå inte förbättrad usability enbart för att implementationen blivit renare.

## 19. Initial analys och prioriteringsmodell

Före en bred refaktoreringsserie ska `knowledge/initial-analysis-prioritization.md` användas som fördjupande ramverk när Knowledge är tillgänglig.

- Inventera relevant projektstruktur, teknikstack, build/test/lint, modulgränser och centrala flöden innan prioritering.
- Håll den initiala breda analysen read-only för produktionskoden; opportunistiska fixes ska planeras, inte smygas in.
- Findings måste ha konkret evidens och systemspecifik konsekvens; en code smell eller metrisk signal är inte tillräcklig ensam.
- Prioritera utifrån severity, förändringsrisk, förväntad nytta, effort och leverage – inte utifrån antal smells, filstorlek eller estetik.
- Dokumentera beroenden mellan åtgärder och en explicit mängd relevanta observationer som bör lämnas orörda, skjutas upp eller kräver mer evidens.
- Skapa en diagnostisk baseline för maintainability, architecture, testability och developer experience samt, när relevant, usability/accessibility. Använd `unknown`/`not_applicable` när underlaget inte räcker.
- För stora projekt: dokumentera sampling och hävda aldrig full täckning från partiell inspektion.
- Analysen ska avslutas med prioriterade findings och rekommenderad riktning; själva stegplanen skapas i efterföljande plansteg.

## 21. Språk- och ramverksspecifika profiler

När teknikstacken kan identifieras ska `knowledge/technology-profiles.md` användas som fördjupning när Knowledge är tillgänglig.

- Detektera profiler från konkreta manifest, dependencies, wrappers och konfiguration; gissa inte ramverk från filnamn ensamma.
- Kombinera profiler när projektet kräver det, exempelvis JavaScript/TypeScript + React.
- Härled build/test/lint/typecheck från projektets egna scripts, wrappers och CI i första hand. Installera eller byt inte verktyg bara för att få ett standardkommando.
- Teknikprofilen får aldrig ersätta det canonical arbetsflödet för analys, prioritering, små steg, verifiering och status.
- Modernisera inte språkversion, ramverk, package manager eller dependencies som bieffekt av refaktorering utan tydligt separat motiv och verifiering.
- Om en profilspecifik regel motsäger faktisk projektkonfiguration ska projektets evidens styra.

