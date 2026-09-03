# Referensscenarier – ZIP-arbetsflöde

1. **Första ZIP utan metadata**
   - Säkerhetsvalidera och packa upp.
   - Bevara wrapper/projektstruktur.
   - Efter analys/planering skapas `.kodforbattraren/`.
   - Input-ZIP:s SHA-256 registreras.

2. **Återupptagen ZIP från föregående steg**
   - Validera `work-status.yaml` och plan.
   - Jämför source manifest.
   - Härled nästa steg från status, inte samtalsminne.
   - Efter PASS levereras komplett ny ZIP.

3. **Monorepo**
   - Bevara alla delprojekt och gemensamma root-filer.
   - Flytta inte enskilt package till arkivroten.
   - Planen får adressera ett delprojekt i taget.

4. **ZIP med build- och binärartefakter**
   - `dist/`, `build/`, `target/`, `node_modules/` och binära assets tas inte bort enbart på namn.
   - Säkra cachefiler kan utelämnas.
   - Okända binärer bevaras byte-identiskt.

5. **Återupptagning i ny konversation**
   - `.kodforbattraren/work-status.yaml` + plan är primär källa.
   - Om status och source snapshot är konsistenta ska användaren kunna säga "Gör nästa steg" direkt.

6. **Zip Slip**
   - Post som `../../outside.txt`, `/absolute.txt` eller drive-path avvisas före skrivning.

7. **Symlink i ZIP**
   - Symlink/specialfil avvisas; den får inte användas för att skriva utanför workspace.

8. **Misslyckad verifiering**
   - Steget markeras inte completed.
   - Om ändringen rullas tillbaka paketeras återställt projekt och blockerande status.

9. **Source drift**
   - Om användaren modifierat senaste ZIP efter analysen och snapshot inte matchar:
     `reanalysis_required` eller fokuserad omanalys innan ändring.
