# Referensscenarier – test- och säkerhetsstrategi

## 1. Projekt utan tester – skydda bara berörd legacy-logik

**Situation:** En central prisberäkning saknar tester och ska delas upp i mindre ansvar.

**Förväntat beslut:** Skapa fokuserade characterization tests runt observerat resultat och relevanta edge cases innan strukturen ändras. Bygg inte en komplett testsuite för hela systemet som förkrav.

## 2. Projekt med befintliga fel – known red är baseline

**Situation:** Två integrationstester misslyckas redan före refaktorering på grund av en känd extern testmiljö.

**Förväntat beslut:** Dokumentera exakt vilka fel som finns före ändringen. Efter steget får de kända felen kvarstå, men inga nya relevanta fel får introduceras. Beskriv inte resultatet som helt grönt.

## 3. Central affärslogik – hög risk trots liten diff

**Situation:** En femraders regel för avgiftsberäkning ska flyttas och förenklas.

**Förväntat beslut:** Klassificera som hög risk eftersom konsekvensen är stor. Säkerställ kontrakts-/edge-case-tester och baseline innan ändringen trots liten diff.

## 4. Rent kosmetisk förändring – proportionerlig verifiering

**Situation:** Ett internt lokalt variabelnamn förtydligas utan påverkan på publik yta eller kontrollflöde.

**Förväntat beslut:** Kör proportionerliga snabba kontroller; skapa inte nya end-to-end-tester eller characterization tests bara för ändringen.

## 5. Test görs svagare för att få grönt – avvisa

**Situation:** Refaktoreringen gör att ett test misslyckas. Förslaget är att ta bort en assertion utan evidens för att kontraktet ska ändras.

**Förväntat beslut:** Avvisa som säkerhetsstrategi. Utred först om implementationen regresserat, testet är för implementationskopplat eller beteendet ändras avsiktligt.

## 6. Characterization test låser misstänkt buggbeteende

**Situation:** Legacy-koden returnerar ett märkligt men etablerat resultat. Refaktoreringen ska vara beteendebevarande.

**Förväntat beslut:** Characterization test får tillfälligt låsa beteendet men ska dokumentera att det är misstänkt och att eventuell korrigering är en separat funktionell ändring.

## 7. Scope expanderar under refaktoreringen – stoppa

**Situation:** Ett litet extraktionssteg visar sig kräva ändring av API, datamodell och tre orelaterade moduler.

**Förväntat beslut:** Stoppa steget och omplanera. Fortsätt inte genom att smyga in en bred rewrite.

## 8. Regression kan inte isoleras – rollback

**Situation:** Efter refaktorering uppstår intermittenta fel och två fixförsök breddar diffen.

**Förväntat beslut:** Rulla tillbaka till senaste verifierade punkt, dokumentera evidens och lägg vid behov in ett förberedande test-/seam-steg.
