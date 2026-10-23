# Projektstatus – Kodförbättraren

## Aktuell status

**Migrationens releaseflöde för GPT Byggaren 1.6.26 är implementerat.** Release-workflowet använder versionslåst 1.6.26 med SHA-256-kontroll, bygger fem distributioner och projekt-ZIP samt skapar/självtestar valfri Engine ZIP. Den äldre projektprofilen och ordinarie CI finns samtidigt kvar; detta är två separata distributionsspår.

Projektets dokumenterade domänbaslinje är **1.0.0**. Den ska inte förväxlas med byggmotorns version. En faktisk publicerad release eller installerad Plugin-version måste kontrolleras separat.

## Funktionell omfattning

- ZIP- och GitHub/PR-baserad förbättring av befintliga kodprojekt.
- Säker stegvis refaktorering med baseline, regressionsskydd och dokumenterade kända testfel.
- Valfri Agent Workspace, PWA Preview och Browser Screenshot enligt canonical instruktion och `src/runtime-policy/optional-companion-verification-policy.md`.
- Offline-fallbackregressionstester från PR #11 och statiska policyskydd från PR #10. Dessa verifierar referensbeslut och instruktionskontrakt, inte faktisk språkmodellsexekvering vid frånvarande plugins.

## Status och begränsningar

`project-status.yaml` är auktoritativ källa för genomförda plansteg och blockerare: steg 1–25 är markerade som färdiga, arbetsfasen är maintenance och inga blockerare anges.

Den äldre profilens fyra aktiva runtime-mål (Chat ZIP, Custom GPT, OpenCode, OpenAI Plugin) skiljer sig från migrationsreleaseflödets fem mål. Att båda spåren finns ska inte tolkas som fem aktiva mål i den äldre profilen.

Ingen ny migration behövs för valfri plugin-verifiering. Live end-to-end-test av Kodförbättrarens beslutsfattande när plugins saknas återstår; offline-testerna täcker endast referensmodellen.

## Nästa lämpliga aktivitet

Verifiera ändringarna i GitHub Actions och granska relevanta releaseartefakter när nästa release förbereds.
