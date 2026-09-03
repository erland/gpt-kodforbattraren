# GitHub repository- och PR-arbetsflöde

Detta dokument är canonical kunskapsstöd för Kodförbättrarens GitHub-läge.

## Grundprincip

GitHub-läget ska vara statusdrivet, inte minnesdrivet. Före varje förändringssteg ska faktisk repository-, branch- och PR-status hämtas och jämföras med arbetsstatusen.

## Beslut före varje steg

1. Läs repository metadata och default branch.
2. Läs aktuell arbetsstatus och eventuell aktiv refaktorerings-PR.
3. Hämta faktisk PR-status från GitHub.
4. Jämför planens source snapshot med aktuell bas/head.
5. Avgör ett av följande lägen:
   - `continue_open_pr`
   - `create_new_pr_after_merge`
   - `create_first_pr`
   - `reanalysis_required`
   - `blocked_closed_unmerged`
   - `blocked_conflict_or_divergence`

## Fortsätt i öppen PR

Fortsätt i samma branch/PR endast när:
- PR:n är öppen,
- branchens ändringar hör till samma refaktoreringsplan,
- föregående steg inte har mergats till basbranchen,
- head/base inte har divergerat så mycket att planen blivit osäker,
- användarens ändringar i samma branch inte gör nästa steg oklart.

Nya commits ska läggas på samma branch och PR-beskrivningen får uppdateras med genomförda steg och verifiering.

## Ny PR efter merge

När föregående PR är mergad:
- hämta aktuell default branch och dess senaste SHA,
- markera föregående PR som historisk i arbetsstatus,
- kontrollera om merge eller andra commits påverkar kvarvarande plan,
- skapa en ny branch från aktuell default branch,
- skapa ny PR för nästa steg.

Återanvänd inte den gamla branchens antagna bas-SHA.

## Stängd PR utan merge

En stängd men ej mergad PR ska inte automatiskt ersättas med en ny identisk PR. Status sätts till `blocked_closed_unmerged` tills orsaken är begriplig. Nästa åtgärd kan vara omplanering, ny implementation eller explicit beslut att återöppna/ersätta PR:n.

## Ändrad kodbas

Kräv `reanalysis_required` när förändringar på basbranchen påverkar:
- filer eller symboler som nästa steg ska ändra,
- antaganden i en finding,
- testbaseline,
- modul-/arkitekturgränser som planen bygger på.

Enbart en ny SHA utanför relevant scope kräver inte automatiskt full omanalys; gör proportionerlig impact check.

## Branch- och PR-namngivning

Rekommenderad branch:
`kodforbattraren/<plan-id>/<step-id>-<kort-slug>`

PR-titel:
`[Kodförbättraren] <step-id> – <stegtitel>`

PR-beskrivningen ska minst innehålla:
- plan-id och steg-id,
- varför ändringen görs,
- berörda findings,
- ändringstyp (`refactoring`, `ux_change`, etc.),
- verifiering och resultat,
- risker/avvikelser,
- nästa planerade steg.

## Säkerhetsregler

- Pusha aldrig direkt till default branch inom refaktoreringsflödet.
- Merg:a inte PR automatiskt om användaren inte uttryckligen ber om det.
- Force-pusha inte som standard.
- Skriv inte över användarens commits.
- Vid merge conflict: stoppa, analysera konflikten och lös endast när semantiken är klar.
- Vid skyddad branch eller otillräcklig behörighet: rapportera blockerare, försök inte kringgå skyddet.
- Behåll små, granskningsbara PR:er i linje med planens steg.

## Arbetsstatus

GitHub-status ska minst kunna lagra:
- repository full name,
- default branch,
- base SHA,
- work branch,
- head SHA,
- active PR number/url/state,
- merged PR history,
- source snapshot,
- last verified workflow/check result,
- eventuell blockerare eller reanalysis flag.

## Verifiering

Efter push/commit:
- verifiera relevanta lokala tester om möjligt,
- kontrollera PR-head SHA,
- kontrollera tillgängliga CI/workflow-runs,
- markera steget completed först när stegkontraktets verifiering är uppfylld eller känt rött baseline-tillstånd är korrekt dokumenterat.
