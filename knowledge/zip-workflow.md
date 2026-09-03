# ZIP-arbetsflöde

Detta är Kodförbättrarens canonical fördjupning för arbete med källkodsprojekt som ZIP.

## Mål

En användare ska kunna:
1. lämna en första projekt-ZIP,
2. få analys + plan,
3. säga "Gör nästa steg",
4. få en komplett uppdaterad projekt-ZIP efter ett lyckat implementeringssteg,
5. återanvända den senaste ZIP:en i en ny konversation utan att arbetsstatus tappas.

## 1. Säker import före läsning

ZIP-filen är data, inte körbar kod. Innan uppackning:

- avvisa absoluta sökvägar,
- avvisa `..`-traversering som lämnar projektroten,
- avvisa NUL-tecken och tvetydiga path-former,
- avvisa symlink-/specialfilsposter i arkivet,
- tillämpa rimliga gränser för antal poster, enskild okomprimerad fil och total okomprimerad storlek,
- skriv endast under den avsedda workspace-roten,
- kör aldrig script från arkivet bara för att "inspektera" ZIP:en.

Om säker import inte kan garanteras ska arbetet blockeras och ingen partiell output kallas färdig.

## 2. Projektrot och wrapper-katalog

Bevara originalets struktur. Om ZIP:en har exakt en gemensam wrapper-katalog ska den normalt bevaras i leveransen.
Intern analys får identifiera en logisk projektrot, men paketeringen får inte godtyckligt flytta filer upp eller ner.

Monorepo behandlas som ett projekt med flera delprojekt, inte som flera orelaterade ZIP:ar, om användaren inte ber om annat.

## 3. Metadata för återupptagning

Kodförbättrarens arbetsmetadata lagras i:

`.kodforbattraren/`

Rekommenderade filer:
- `work-status.yaml` – faktisk maskinläsbar status,
- `refactoring-plan.yaml` – canonical plan,
- `refactoring-plan.md` – mänskligt läsbar plan,
- `STATUS.md` – kort mänsklig progress,
- `source-manifest.json` – snapshot/fingeravtryck av relevanta filer.

Metadata får inte ersätta användarens egna projektfiler och ska undvika hemligheter.
Om projektet redan innehåller `.kodforbattraren/` ska befintlig metadata valideras innan den används.

## 4. Vad ska följa med i ny ZIP?

Default är **preserve by default**:
- källkod,
- konfiguration,
- dokumentation,
- tester,
- resurser/assets,
- lockfiler,
- migrations,
- CI,
- okända filer.

Följande kan normalt utelämnas som säkra transienter:
- `__pycache__/`,
- `.pytest_cache/`,
- `.mypy_cache/`,
- `.ruff_cache/`,
- `.coverage` och vanliga lokala coverage-cachefiler,
- `*.pyc`,
- `.DS_Store`.

Följande får **inte** tas bort enbart på katalognamn:
- `dist/`,
- `build/`,
- `target/`,
- `out/`,
- `node_modules/`,
- vendor-kataloger,
- binära assets.

De kan vara genererade eller irrelevanta, men kan också vara en avsiktlig del av leveransen. Exkludering kräver explicit policy/evidens och ska dokumenteras.

## 5. Binära filer

Binära filer ska i normalfallet bevaras byte-identiskt om steget inte uttryckligen ändrar dem.
Försök inte "normalisera" okända binärformat.

## 6. Source snapshot

För att upptäcka drift mellan analys och genomförande:
- beräkna ett deterministiskt manifest över relevanta filer,
- sortera paths,
- hash:a filinnehåll,
- exkludera endast Kodförbättrarens egna dynamiska statusfiler och säkra transienter från snapshot när det behövs.

Om snapshot inte längre matchar basen för den planerade ändringen ska GPT:n göra en fokuserad omanalys eller markera `reanalysis_required`.

## 7. Genomförandesteg

Vid "Gör nästa steg" i ZIP-läge:

1. validera `.kodforbattraren/` om den finns,
2. fastställ plan och faktisk status,
3. kontrollera source drift,
4. välj nästa körbara steg,
5. gör endast det steget,
6. verifiera enligt test-/säkerhetsstrategin,
7. uppdatera findings, plan och work-status,
8. uppdatera mänsklig `STATUS.md`,
9. skapa en komplett ZIP från den nya workspace-versionen,
10. beräkna output-ZIP:ens SHA-256 och redovisa leveransen.

Misslyckad verifiering innebär att steget inte markeras completed. Om ändringen rullas tillbaka ska ZIP:en representera det återställda tillståndet och statusen säga varför.

## 8. Första ZIP kontra återupptagen ZIP

### Första ZIP
Om `.kodforbattraren/` saknas:
- behandla projektet som ny källa,
- skapa metadata efter initial analys/planering,
- registrera input-ZIP:ens namn och SHA-256 som bas.

### Återupptagen ZIP
Om metadata finns:
- validera schema/version,
- kontrollera att metadata hör till projektets snapshot,
- använd status + plan som primär återupptagningskälla,
- förlita dig inte på samtalsminne.

Om metadata är inkompatibel eller motsägelsefull: blockera automatisk fortsättning och gör en kontrollerad återkonstruktion/omanalys.

## 9. Namngivning av leveranser

Använd ett stabilt namn som signalerar att ZIP:en är en komplett projektversion, exempelvis:

`<projekt>-kodforbattraren-step-R-003.zip`

Undvik namn som antyder patch-only om arkivet faktiskt är fullständigt.

## 10. Integritetskontroll före leverans

Före leverans:
- öppna ZIP:en igen,
- kör ZIP-integritetskontroll,
- kontrollera att minst en projektfil finns,
- kontrollera att `.kodforbattraren/` finns när serien är etablerad,
- säkerställ att inga tillfälliga arbetskataloger eller verktygscacher följt med,
- kontrollera att status säger samma completed/next-step som leveransen.

En ZIP får inte kallas klar om integritetskontrollen misslyckar.
