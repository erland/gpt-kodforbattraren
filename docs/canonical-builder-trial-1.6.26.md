# Kanonisk byggprofil – tekniskt försök 2026-10-19

Arbetsunderlag: uppladdat commitlåst källarkiv och GPT Byggaren Chat ZIP 1.6.26.

## Utfört i isolerad arbetskopia

1. Körde `migrate_legacy_copy.py --upgrade-build`. Motorn stoppade på `plugin_mapping_review`, som väntat.
2. Skapade en **experimentell** `build_system.runtime_targets`-mappning med fem runtimes och `project`, explicit reducerad/inaktiv Plugin och avaktiverad Custom GPT.
3. Körde `install_distribution_engine.py --project-root <kopia>`. Motorn installerade sju kanoniska script/resursfiler och en OpenCode README-mall i kopian. Ingen fil ändrades i huvudprojektet eller PR.
4. Första byggförsöket: `Missing/unsafe canonical skill resource: docs/dynamic-planning.md`. Orsak: Builderns egna OpenCode skill-definitioner hade kopierats och refererade en fil som Kodförbättraren inte har.
5. Tog bort just denna Builder-specifika skill-definition i experimentprofilen utan att skapa en fiktiv fil. Nästa byggförsök stoppade med `KeyError: 'structure'` när den kanoniska Chat-byggaren läste `structure.conversation_starters.path`.

## Resultat

**Ej färdigbyggt**: Enbart `runtime_targets` räcker inte. Byggaren förutsätter fler kanoniska strukturfält och granskad skill-source ownership, som inte finns i den äldre projektprofilen. En mekanisk kopiering av GPT Byggarens egen gpt-project.yaml skulle skapa felaktiga referenser till dess egna dokument och policies.

## Kodändring i PR

Tillagt `scripts/preflight_gpt_builder_1626.py`: en läsande diagnostikkontroll som rapporterar saknade runtime targets, runtime-mappning, saknat `structure`/assembly-kontrakt och trasiga OpenCode resursreferenser. Den gör **inga** ändringar i projektet.

## Rekommenderat fortsättningssteg

1. Härled en korrekt projektspecifik `structure` och `canonical/assembly.json` från faktiskt innehåll i `src/instructions/system.md`, `knowledge/` och befintliga testfall.
2. Ge kanoniska byggaren egna startfrågor/mallar och projektspecifika skills och låt en validerare säkerställa att inga Builder-interna paths läcker.
3. Flytta sedan om `scripts/build_distributions.py` först när den nya vägen producerar fem validerade ZIP. Behåll legacy builder för rollback tills dess.

**Slutsats:** Aktuell PR är fortfarande draft; ingen lyckad femdistributionsbyggkedja har checkats in.
