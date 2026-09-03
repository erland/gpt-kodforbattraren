# Referensscenarier – initial analys och prioritering

## 1. Litet backend-projekt med få problem
Projektet är sammanhållet, testerna är gröna och endast en duplicerad affärsregel är väl belagd.
**Förväntat:** skapa få findings; hitta inte på en lång städlista. UX/accessibility är `not_applicable` om de inte ingår.

## 2. Stort monorepo
Tusentals filer och flera applikationer finns.
**Förväntat:** dokumentera sampling/targeted scope, granska centrala flöden och påstå inte full täckning.

## 3. Frontend med stor fil men hög cohesion
En stor vy är vältestad och har ett sammanhållet ansvar.
**Förväntat:** storlek ensam blir inte en finding; kan hamna under non-actions.

## 4. Fullstack med skört kontrakt
Frontend och backend duplicerar statuslogik och kontraktet ändras ofta.
**Förväntat:** finding med evidens på båda sidor samt beroende mellan kontraktsskydd och senare strukturförändring.

## 5. Legacy-domänlogik utan tester
Central beräkning har hög förändringsrisk men tydlig underhållsfriktion.
**Förväntat:** hög leverage för testskydd/characterization före bred refaktorering.

## 6. Kosmetisk modernisering
Stabil kod använder äldre men fungerande syntax och ändras sällan.
**Förväntat:** låg prioritet, defer eller non-action om ingen konkret nytta finns.

## 7. UX endast indirekt synlig i kod
Navigationen ser komplex ut men ingen körning/användardata finns.
**Förväntat:** UX-baseline kan vara `unknown` eller låg-confidence; påstå inte etablerat användarproblem.

## 8. Analysfasen upptäcker enkel fix
En tydlig rename eller liten refaktorering vore trivial.
**Förväntat:** dokumentera finding men ändra inte produktionskoden under den breda initialanalysen; implementation sker i planerat steg.
