# UX/usability – referensscenarier

1. Tom projektlista visar blank yta → finding: empty state saknas; `ux_change`.
2. API-fel visas som stack trace → finding: begriplig recovery saknas; `ux_change`.
3. Stor React-komponent delas utan ändrad rendering/interaktion → `refactoring`.
4. Primär handling flyttas så vanliga flödet får färre steg → `ux_change`.
5. Tvådimensionell datatabell kräver mobil horisontell scroll → ingen automatisk finding.
6. Långt formulär raderar inmatning efter serverfel → högprioriterad recovery/data-bevarande-finding.
7. Reversibel handling har confirmation varje gång → utvärdera undo; ta inte bort skydd mekaniskt.
8. Färg är enda statusindikering → tillgänglighetsfinding när statusen är betydelsefull.
9. Samma domänobjekt har tre användartermer → finding om det rimligen skapar begreppsförvirring.
10. Komplicerad navigation kan bara härledas ur kod → `hypothesis`/`strong_inference`, inte etablerat användarproblem.
