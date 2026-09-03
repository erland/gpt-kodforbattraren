# Scenarier – canonical beteendekontrakt

Dessa scenarier verifierar kärnbeteendet i steg 4. De är avsedda att senare kunna omvandlas till eller kompletteras med automatiserade evals.

## CB-01 – Bred refaktorering börjar med analys

**Givet:** Användaren lämnar ett helt projekt och säger "Refaktorera det här projektet".

**Förväntat:** GPT:n inventerar och analyserar projektet, prioriterar findings och skapar en plan innan breda produktionsändringar görs.

**Underkänt om:** GPT:n direkt börjar flytta/dela större mängder kod utan projektanalys.

## CB-02 – Lokal trivial förändring kräver inte full projektanalys

**Givet:** Användaren ber att byta ett missvisande lokalt variabelnamn i en tydligt avgränsad funktion.

**Förväntat:** GPT:n förstår relevant kod och gör den lokala ändringen utan att kräva en full projektinventering.

**Underkänt om:** GPT:n tvingar fram en oproportionerlig helhetsanalys.

## CB-03 – För stort steg delas upp

**Givet:** Planerat steg innehåller samtidig databasomläggning, uppdelning av en stor service, nytt API-kontrakt och UI-ändring.

**Förväntat:** GPT:n delar upp steget i mindre verifierbara steg och motiverar ordningen.

**Underkänt om:** Allt genomförs som en enda stor diff trots separata risker och verifieringsbehov.

## CB-04 – Onödig refaktorering avvisas

**Givet:** En 700-raders parser är sammanhållen, stabil, vältestad och ändras sällan. Enda argumentet är att filen är "för lång".

**Förväntat:** GPT:n behandlar storleken som en signal men rekommenderar inte uppdelning utan ytterligare evidens.

**Underkänt om:** GPT:n använder en mekanisk radgräns som skäl för refaktorering.

## CB-05 – Pattern införs inte som mål

**Givet:** En enda stabil implementation finns och ingen realistisk variationspunkt är identifierad.

**Förväntat:** GPT:n avstår från Strategy/Factory/interface-lager om det inte finns tydlig nytta.

**Underkänt om:** Pattern införs enbart för "bättre arkitektur".

## CB-06 – Refaktorering skiljs från beteendeförändring

**Givet:** En komponent ska delas upp och samtidigt ska användarflödet kortas från tre steg till två.

**Förväntat:** GPT:n klassificerar uppdelningen som refaktorering och flödesändringen som UX/beteendeförändring, och separerar dem normalt i olika steg.

**Underkänt om:** Hela förändringen beskrivs som beteendebevarande refaktorering.

## CB-07 – Riskfylld legacy-logik skyddas

**Givet:** En central beräkningsservice saknar tester och ska delas upp.

**Förväntat:** GPT:n bedömer behovet av characterization tests eller motsvarande verifiering före strukturell förändring.

**Underkänt om:** Service delas upp utan plan för att skydda befintligt beteende.

## CB-08 – "Gör nästa steg" använder faktisk status

**Givet:** `project-status.yaml` anger rekommenderat steg 8 medan konversationshistoriken antyder steg 7.

**Förväntat:** GPT:n följer den faktiska statusen, kontrollerar plan/blockerare och återupptar steg 8.

**Underkänt om:** GPT:n väljer steg utifrån implicit minne.

## CB-09 – Blockerat nästa steg hoppas inte över

**Givet:** Nästa steg har blockerare på grund av misslyckade tester.

**Förväntat:** GPT:n hanterar blockeraren eller rapporterar att steget inte kan avslutas; den markerar inte steget klart och hoppar inte tyst vidare.

**Underkänt om:** Status flyttas fram trots blockeraren.

## CB-10 – ZIP-leverans är komplett

**Givet:** Ett implementeringssteg utförs på ett ZIP-projekt.

**Förväntat:** GPT:n levererar ett komplett uppdaterat projektpaket som kan användas som källa för nästa steg.

**Underkänt om:** Endast diff/enskilda ändrade filer levereras när komplett ZIP är möjlig.

## CB-11 – GitHub fortsätter i öppen PR

**Givet:** Det finns en relevant öppen, ej mergad förbättrings-PR.

**Förväntat:** Nästa relaterade steg fortsätter normalt i samma PR.

**Underkänt om:** En ny parallell PR skapas utan skäl.

## CB-12 – Ny PR efter merge

**Givet:** Föregående förbättrings-PR är mergad.

**Förväntat:** GPT:n utgår från aktuell default branch och skapar normalt en ny branch/PR för nästa steg.

**Underkänt om:** GPT:n fortsätter på den gamla mergade branchen som om den vore aktiv.
