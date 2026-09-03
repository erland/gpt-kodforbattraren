# Rapporter, status och användarupplevelse i Kodförbättraren

Detta dokument beskriver hur analys, plan, status och genomförda steg ska presenteras så att användaren kan driva ett långt förbättringsarbete utan att förstå den interna statusmodellen.

## Grundprincip

Maskinläsbara modeller är canonical källa för tillstånd. Mänskligt läsbara rapporter är projektioner av samma tillstånd och får inte motsäga dem.

Efter varje betydelsefull operation ska användaren enkelt kunna svara på fyra frågor:

1. Vad har analyserats eller ändrats?
2. Varför är det viktigt?
3. Hur verifierades resultatet och finns blockerare?
4. Vad är nästa rekommenderade steg?

## 1. Initial analysrapport

Analysrapporten ska vara beslutsorienterad och innehålla:

- scope och underlag,
- teknik-/projektöversikt,
- diagnostisk baseline,
- prioriterade findings med evidens och konsekvens,
- sådant som bör lämnas orört eller kräver mer evidens,
- risker och beroenden,
- rekommenderad riktning,
- länk/referens till den separata refaktoreringsplanen när den skapats.

Rapporten ska skilja observation, slutsats och rekommendation. Hypoteser får inte presenteras som verifierade problem.

## 2. `refactoring-plan.md`

Planen är den mänskligt läsbara projektionen av den maskinläsbara refaktoreringsplanen. Den ska visa:

- mål och scope,
- ordnade steg,
- findings som varje steg adresserar,
- beroenden och blockerare,
- risknivå,
- klart-kriterier,
- verifiering,
- aktuellt steg och nästa rekommenderade steg,
- historik över explicit omplanering när relevant.

Planen får inte smyga in nya steg som saknas i canonical planstatus.

## 3. `STATUS.md`

`STATUS.md` ska vara kortare än planen och optimerad för återupptagning. Den ska minst innehålla:

- projekt/arbetsserie,
- leveransläge (`zip` eller `github`) när relevant,
- senast avslutade steg,
- aktuellt tillstånd,
- öppna blockerare/varningar,
- verifieringsstatus,
- aktiv ZIP/branch/PR när relevant,
- **Nästa rekommenderade steg** med id + titel + kort motiv.

Om inget steg kan köras ska statusen säga `BLOCKED` eller `COMPLETE`; den får inte hitta på ett nytt nästa steg.

## 4. Standardiserad stegslutrapport

Efter ett genomfört steg ska svaret vara kort och konsekvent:

### Steg N – Titel: klart / blockerat / rollback

**Genomfört**
- viktigaste förändringarna

**Verifiering**
- vilka relevanta kontroller som kördes
- resultat, inklusive known-red om sådant finns

**Leverans**
- komplett ZIP eller PR när relevant

**Kvarstår**
- varningar/blockerare, eller `Inga`

**Nästa rekommenderade steg:** Steg X – Titel

Sista raden ska vara explicit när ett nästa steg finns. Användaren ska inte behöva tolka en lång rapport för att veta vad som kommer härnäst.

## 5. Korta fortsättningskommandon

### `Gör nästa steg` / `Fortsätt` / `Nästa`

Detta är ett exekveringskommando i en pågående arbetsserie. Läs faktisk status och plan, kontrollera blockerare och source drift, och genomför exakt nästa körbara steg. Fråga inte användaren vilket steg som avses när statusen entydigt anger det.

### `Vad är nästa steg?`

Detta är en statusfråga, inte ett exekveringskommando. Läs faktisk status och svara kort med nästa rekommenderade steg och varför. Gör inga kodändringar.

### `Visa status`

Sammanfatta `STATUS.md`/maskinstatus utan att förändra projektet.

### `Fortsätt med PR:n`

I GitHub-läge: läs faktisk PR-status först. Fortsätt endast i relevant öppen PR; annars följ GitHub-beslutsreglerna.

## 6. Blockerare och misslyckad verifiering

Vid blockerare eller misslyckad obligatorisk verifiering:

- markera inte steget som completed,
- presentera blockeraren först efter en kort statusrad,
- ange vilken evidens eller åtgärd som krävs,
- ange inte ett senare plansteg som nästa körbara steg,
- leverera rollback-tillstånd när rollback har gjorts.

## 7. Progressiv detaljnivå

Standardpresentationen ska vara kompakt. Detaljer finns i nedladdningsbara artefakter och kan visas på begäran. Undvik att repetera hela analysen efter varje steg.

För analyser ska tillräcklig evidens finnas för beslut. För stegslut ska fokus ligga på förändring, verifiering, leverans och nästa steg.

## 8. Ingen dold status

Samtalsminne får aldrig vara enda källan till framdrift. Om statusfil och chatt skiljer sig ska fil-/repo-status vinna eller konflikten repareras explicit.
