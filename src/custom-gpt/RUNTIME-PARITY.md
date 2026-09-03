# Runtime parity – Chat ZIP kontra Custom GPT

## Gemensamt
Båda distributionerna härleds från samma canonical beteendekontrakt och ska ha samma beslut kring analys före ändring, prioritering, design patterns, testskydd, UX-klassificering, status, nästa steg och ZIP/PR-livscykel.

## Skillnader
- Chat ZIP innehåller schemas, runtime-scripts och templates direkt i paketet.
- Custom GPT använder en kompilerad instruktion under 8 000 tecken och 19 Knowledge-filer.
- Custom GPT:s GitHub-skrivförmåga beror på om en GitHub Action/connector med write-capability faktiskt konfigureras. Instruktionen får aldrig låtsas att en PR skapats om sådan capability saknas.
- Deterministiska hjälpscript från Chat ZIP kan återskapas eller köras via Code Interpreter när de behövs, men kritiska beslut finns även explicit i `INSTRUCTIONS.md`.

## Parity-krav
Följande får inte försvinna i Custom GPT-kompileringen:
1. analys före bred förändring,
2. evidensbaserad och proportionerlig prioritering,
3. ingen mekanisk refaktorering p.g.a. storlek/pattern,
4. refactoring kontra functional/UX change,
5. baseline/testskydd och stopp vid regression,
6. faktisk plan/status styr `Gör nästa steg`,
7. read-only `Vad är nästa steg?`,
8. komplett ZIP efter lyckat ZIP-steg,
9. öppen PR återanvänds; ny PR efter merge; stängd utan merge blockerar,
10. möjlighet att säga att ingen refaktorering behövs.
