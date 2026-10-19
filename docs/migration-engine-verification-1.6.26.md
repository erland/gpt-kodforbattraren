# Teknisk migrationskontroll – 2026-10-19

## Verifierat

- Källa: bifogad `gpt-byggaren-chat-1.6.26.zip`.
- Den kanoniska motorn finns under `distribution-engine/`.
- Migreringskommandot `migrate_legacy_copy.py --source SOURCE --destination DESTINATION [--upgrade-build] [--version VERSION]` stöder ZIP och arbetskatalog och skriver aldrig över originalet.
- `selftest_distribution_engine.py` kördes lokalt och avslutades utan fel. Resultatet rapporterade SHA-256-verifiering av 62 filer, installerad byggmotor samt sex skapade arkiv (projekt och fem distributioner).
- GitHub-projektets bascommit: `24a294e6c6f343600e78309d806d4ed365687706`. Migrationsgrenen är `migration/gpt-byggaren-1.6.26`.

## Vad självtestet inte bevisar

Självtestet testar motorns egen fixture och **inte** Kodförbättrarens källträd. Det är därför inte tillräckligt för att markera migreringen eller runtimeparitet som godkänd.

## Återstående indata

GitHub-anslutningen erbjuder individuella filer, men tillhandahöll inte hela källträdet som lokal ZIP i denna körmiljö. För fullständig säker migrering används följande låsta basarkiv:

https://github.com/erland/gpt-kodforbattraren/archive/24a294e6c6f343600e78309d806d4ed365687706.zip

När ZIP-filen finns i en lokal körmiljö kan följande kommando köras:

```bash
python distribution-engine/scripts/migrate_legacy_copy.py \
  --source kodforbattraren-source.zip \
  --destination kodforbattraren-migrated \
  --upgrade-build \
  --version 1.6.26
```

Detta är ett föreslaget körkommando, inte ett påstående om att Kodförbättrarens migrering har körts.

## Nästa kvalitetsgrind

Granska migreringsrapporten, kör den befintliga testsviten på basversionen och migrationen, jämför canonicals, bygg fem distributioner, kontrollera parity, och uppdatera därefter CI/release. Lämna PR som utkast tills detta passerar.
