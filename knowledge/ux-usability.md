# UX- och usability-analys

Detta dokument är canonical kunskapsstöd för Kodförbättrarens analys av användarupplevelse.
UX-förbättringar ska hållas åtskilda från ren, beteendebevarande refaktorering.

## Grundprincip

En UX-observation är inte automatiskt ett problem och ett problem är inte automatiskt värt att ändra.
Bedöm alltid:

1. användarens mål och kontext,
2. konkret evidens i gränssnitt eller flöde,
3. frekvens och konsekvens,
4. tillgänglighets- och felrisk,
5. alternativ och trade-offs,
6. minsta proportionerliga förbättring,
7. hur förändringen ska verifieras.

När användarbeteende, informationsarkitektur, navigation, ordval, feedback eller interaktionsflöde ändras
ska steget klassificeras som `ux_change` eller annan beteendeförändring – inte som ren `refactoring`.

## Analysdimensioner

### 1. Navigation och orientering
Bedöm om användaren förstår var den befinner sig, kan förutse vart en handling leder, hittar vanliga mål utan onödiga omvägar och kan återvända utan att förlora arbete eller kontext.

### 2. Informationsarkitektur
Bedöm om information är grupperad efter användarens uppgift snarare än implementation, om hierarki och rubriker gör prioritet tydlig och om relaterad information är samlad. Rekommendera inte omstrukturering bara för symmetri.

### 3. Loading-, empty- och error states
Bedöm betydelsefulla asynkrona vyer för loading state, tomt men giltigt state, felstate, retry/recovery och bibehållen användarkontext.

### 4. Formulär och inmatning
Bedöm etiketter, standardvärden, validering, inline-fel, bevarande av inmatning, tangentbord/fokus, input-typer, autocomplete och destruktiva handlingar.

### 5. Feedback och systemstatus
Systemet bör ge proportionerlig återkoppling för påbörjad handling, väntan, lyckat resultat, partiellt resultat, fel och bakgrundsarbete.

### 6. Tillgänglighet
Granska minst semantiska kontroller/rubriker, tangentbordsåtkomst, synlig fokusmarkering, name/role/value, felidentifiering, alternativ text, zoom/reflow, kontrast och information som inte bara förmedlas med färg. Exakta WCAG-påståenden ska bara göras när evidensen räcker.

### 7. Mobil och responsiv användbarhet
Bedöm touch targets, reflow, innehållsprioritering, modaler/drawers och tangentbord, sticky controls och relevanta orientationer.

### 8. Kognitiv belastning
Leta efter för många samtidiga beslut, otydliga termer, information som måste memoreras mellan steg, onödiga val, upprepade manuella handlingar och inkonsekventa mönster.

### 9. Destruktiva och riskfyllda handlingar
Bedöm om konsekvensen är begriplig före handlingen, om undo kan ersätta onödiga confirmation dialogs och om irreversibla steg har proportionerligt skydd.

### 10. Konsistens och språk
Bedöm samma begrepp för samma sak, konsekventa controls, handlingsorienterad microcopy och om tekniska fel exponeras som enda användarmeddelande.

## Evidensnivåer

`direct` – problemet kan observeras direkt i kod, UI-struktur, test, screenshot eller reproducerbart flöde.

`strong_inference` – flera tekniska signaler pekar åt samma håll, men verklig användning har inte observerats.

`hypothesis` – rimlig UX-risk som måste verifieras med körning, användardata eller manuell granskning.

Hypoteser får inte presenteras som etablerade användarproblem.

## Prioritering

Prioritera högre när problemet blockerar ett centralt användarmål, orsakar dataförlust/riskfyllda misstag, påverkar tillgänglighet i centrala flöden, återkommer ofta, har stor räckvidd eller kan förbättras med låg/måttlig förändringsrisk.

Kosmetisk preferens utan tydlig nytta ska normalt prioriteras lågt eller utelämnas.

## Refaktorering kontra UX-förändring

Ren refaktorering kan vara att dela en UI-komponent utan ändrad rendering/interaktion eller flytta state management med bibehållet observerbart beteende.

UX-förändring är exempelvis att flytta en knapp, ändra navigation eller stegordning, byta microcopy som påverkar förståelsen, lägga till autosave, ändra felmeddelande/validering eller ändra loading/empty state.

Ett genomförandesteg får innehålla båda typerna endast när kopplingen är nödvändig och verifieringen tydligt täcker båda.

## Verifiering av UX-förändringar

Välj proportionerlig verifiering:
- komponent-/integrationstest för stabil interaktionslogik,
- tillgänglighetskontroller,
- responsiv/manuell kontroll,
- screenshots eller visual regression där projektet stödjer det,
- E2E för kritiska flöden,
- användbarhetsgranskning eller faktisk användartestning när slutsatsen kräver det.

Påstå inte att användbarheten förbättrades enbart för att koden blev renare.
