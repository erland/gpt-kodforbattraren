# Custom GPT-konfiguration – Kodförbättraren

## Grunddata
- **Namn:** Kodförbättraren
- **Beskrivning:** Expert på säker, stegvis refaktorering och förbättring av källkod, arkitektur, testbarhet och UX. Analyserar först, skapar plan och kan därefter genomföra ett steg i taget via ZIP eller GitHub när skrivverktyg finns.
- **Instruktioner:** kopiera hela `INSTRUCTIONS.md` till GPT:ns Instructions-fält.

## Capabilities
- **Code Interpreter / Data Analysis:** PÅ – krävs för ZIP-analys, filändringar, testkörning och återpaketering.
- **Web Search:** PÅ – används vid behov för aktuell officiell dokumentation; projektets egen kod/config är alltid primär källa.
- **Image generation:** AV – behövs inte för kärnflödet.
- **Canvas:** inte relevant.
- **GitHub write capability:** konfigurera en godkänd GitHub Action/connector om GPT:n ska skapa branches, commits och PR:ar. Utan sådan capability ska GitHub-läget vara read-only och ZIP-flödet användas för kodändringar.

## Knowledge
Ladda upp samtliga filer i katalogen `knowledge/`. Paketet innehåller 19 filer och ligger därmed under gränsen 20 Knowledge-filer.

## Rekommenderade conversation starters
1. `Analysera den här ZIP-filen och skapa en prioriterad refaktoreringsplan.`
2. `Analysera detta GitHub-repository och föreslå vad som bör förbättras först.`
3. `Gör nästa steg.`
4. `Vad är nästa steg?`
5. `Förbättra användarupplevelsen utan att blanda ihop UX-förändringar med ren refaktorering.`

## Första verifiering efter konfigurering
- Ladda upp ett mindre testprojekt som ZIP.
- Kontrollera att GPT:n analyserar innan bred ändring.
- Kontrollera att planen skapas innan en flerstepsserie.
- Säg `Vad är nästa steg?` och verifiera att inget ändras.
- Säg `Gör nästa steg` och verifiera att exakt ett steg genomförs och en komplett ZIP lämnas tillbaka.
