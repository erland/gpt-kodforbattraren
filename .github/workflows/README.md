# GitHub Actions

- `ci.yml` kör schema-/runtimevalidering, tester och ett distributionsbygge på push och pull request.
- `release.yml` triggas när en GitHub Release publiceras och bygger Chat ZIP + Custom GPT ZIP med
  versionsnumret från release-taggen. Artefakterna laddas både upp som workflow artifact och bifogas
  den publicerade releasen.
- `workflow_dispatch` finns för manuell verifiering av releasebygget och kräver ett versionsvärde.

Versionsnumret underhålls alltså inte manuellt i runtime-paketen.
