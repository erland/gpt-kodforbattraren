# Initial analys och prioriteringsmodell

Detta dokument är canonical kunskapsstöd för den analys som ska föregå en bred refaktoreringsserie.
Målet är att skapa en evidensbaserad nulägesbild och en prioriterad mängd findings **utan att modifiera produktionskoden**.

## Grundprincip

Analysen ska svara på fyra frågor i denna ordning:

1. Vad består systemet av och hur byggs/körs/verifieras det?
2. Vilka konkreta problem eller förbättringsmöjligheter finns, med evidens?
3. Vilka av dem är faktiskt värda att åtgärda och i vilken ordning?
4. Vad bör uttryckligen lämnas orört eller skjutas upp?

Analysfasen är read-only för produktionskoden. Test- eller verktygskörningar får göras när de inte ändrar projektets avsedda källinnehåll. Ändringar som behövs för att möjliggöra analys ska planeras som senare steg, inte smygas in i analysen.

## 1. Inventering av projektstruktur och teknikstack

Inventera bara sådant som påverkar analys och genomförande. Beskriv minst när det går att fastställa:

- applikationstyper: frontend, backend, CLI, bibliotek, mobil, monorepo eller kombination,
- språk och centrala ramverk,
- build-/pakethanterare,
- test-, lint- och typkontrollverktyg,
- persistence, meddelanden och externa integrationer,
- deploy/runtime-konfiguration,
- modul-/paketstruktur och tydliga arkitekturgränser,
- entrypoints och centrala användarflöden,
- dokumentation som påverkar hur systemet förstås och körs.

Redovisa osäkerhet. Gissa inte teknikstack utifrån filnamn när innehållet säger något annat.

## 2. Analysdjup och sampling

Små projekt kan normalt läsas brett. Stora projekt kräver riskbaserad sampling.

Prioritera då:

- entrypoints och centrala flöden,
- kod med hög ändringsfrekvens om historik finns,
- stora eller centralt beroende moduler,
- domänlogik och gränser mot persistence/integration,
- områden där tester saknas eller ofta fallerar,
- UI-flöden som är centrala för användarens mål när UX ingår.

Påstå inte full täckning om analysen bygger på sampling. Dokumentera scope och vad som inte granskats.

## 3. Findings måste ha evidens

En finding ska innehålla:

- identifierare och tydlig titel,
- kategori,
- beskrivning av problemet eller förbättringsmöjligheten,
- konkret evidens med berörda filer/symboler när möjligt,
- confidence,
- bedömd konsekvens,
- rekommenderad åtgärd eller beslut att avstå,
- change classification,
- initial prioritet.

En heuristic eller metrisk signal är inte tillräcklig i sig. Förklara varför signalen spelar roll i just detta system.

## 4. Prioriteringsdimensioner

Bedöm varje relevant finding separat längs följande dimensioner:

### Severity
Hur allvarlig är den nuvarande konsekvensen?

- `critical`: sannolik eller pågående allvarlig skada, dataförlust, säkerhets-/driftsrisk eller central funktion blockeras.
- `high`: återkommande eller betydande konsekvens för förändringsförmåga, stabilitet eller användarmål.
- `medium`: reell men begränsad friktion/risk.
- `low`: liten konsekvens eller lokal förbättring.
- `none`: signal utan visad negativ konsekvens.

### Change risk
Hur stor är risken att själva åtgärden orsakar regression eller oavsiktad beteendeförändring?

### Expected benefit
Hur mycket förbättrar åtgärden underhållbarhet, testbarhet, arkitektur, DX eller användarnytta?

### Effort
Grov relativ arbetskostnad: `small`, `medium`, `large`, `unknown`.

### Leverage
Hur mycket möjliggör åtgärden andra säkra förbättringar?

## 5. Rekommenderad prioritet

Prioritet är ett beslut, inte en matematisk poäng. Använd dimensionerna som stöd.

Typiska regler:

- hög severity + hög nytta + hanterbar förändringsrisk => normalt hög prioritet,
- medelhög severity men hög arkitektonisk/testmässig leverage => kan prioriteras tidigt,
- låg nytta + hög risk/kostnad => `defer` eller `wont_fix`,
- kosmetik eller modernisering utan konkret konsekvens => normalt låg prioritet eller ingen finding,
- blockerande testbarhetsproblem kan prioriteras före den kodsmell de skyddar.

Prioritera inte enbart efter filstorlek, antal smells eller personlig preferens.

## 6. Beroenden mellan åtgärder

Identifiera när en åtgärd:

- måste föregås av characterization tests,
- kräver att en modulgräns etableras först,
- bör göras efter att ett API stabiliserats,
- påverkas av en annan planerad förändring,
- bör kombineras eller uttryckligen separeras från en UX/funktionsändring.

Beskriv beroendet, inte bara ordningen.

## 7. Medvetet inte åtgärda

Analysen ska ha en explicit lista över observationer eller findings som **inte** rekommenderas för åtgärd nu.

Exempel:

- stor men sammanhållen stabil fil,
- etablerat pattern som ser tungt ut men skyddar en verklig variationspunkt,
- legacy-modul som är stabil och nära avveckling,
- lågprioriterad kosmetik som skulle skapa stor diff,
- prestandaoptimering utan evidens för prestandaproblem.

Detta minskar risken att planen blir en städlista utan affärs- eller underhållsnytta.

## 8. Diagnostisk baseline

Skapa en diagnostisk baseline med dimensionerna:

- `maintainability`
- `architecture`
- `testability`
- `developer_experience`
- `usability` när relevant
- `accessibility` när relevant

Varje dimension ska innehålla:

- nivå `strong`, `adequate`, `weak`, `unknown`,
- kort evidensbaserad motivering,
- confidence.

Baseline är **inte ett vetenskapligt betyg** och ska inte presenteras som en exakt mätning. Syftet är en konsekvent nulägesbild som kan jämföras kvalitativt efter genomförd serie.

Om underlaget är för svagt: använd `unknown` i stället för att gissa.

## 9. Projektstorlek och typ

### Små projekt
Undvik överanalys. Ett fåtal tydliga findings och en kort baseline kan vara tillräckligt.

### Stora projekt/monorepon
Avgränsa analysen, dokumentera sampling och undvik att hävda fullständig täckning.

### Backend-only
UX/usability ska normalt markeras `not_applicable` eller utelämnas om inget användargränssnitt/API-usability-uppdrag finns.

### Frontend-only
Analysera både intern kodkvalitet och UX när uppdraget omfattar användarupplevelse, men håll findings separerade.

### Fullstack
Analysera gränser och kontrakt mellan frontend/backend samt end-to-end testbarhet, inte bara varje sida isolerat.

## 10. Analysresultat

Den initiala analysen ska normalt ge:

1. scope och begränsningar,
2. projekt-/stackinventering,
3. diagnostisk baseline,
4. prioriterade findings,
5. beroenden,
6. sådant som bör lämnas orört/skjutas upp,
7. rekommenderad riktning inför plansteget.

Den ska **inte** i detta steg börja genomföra refaktoreringar.
