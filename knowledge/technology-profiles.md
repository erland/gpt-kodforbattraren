# Språk- och ramverksspecifika profiler

Detta dokument fördjupar Kodförbättrarens generella arbetsflöde med teknikberoende signaler. Profilerna får aldrig ersätta analys av det faktiska projektet.

## Grundregler

1. Detektera teknik från konkreta projektfiler och beroenden, inte från gissningar eller filändelser ensamma.
2. Härled build/test/lint/typecheck från projektets egna scripts, wrappers och konfiguration när de finns.
3. Föredra repositoryts befintliga verktyg och versioner framför egna standardkommandon.
4. Modernisera inte ramverk, språkversioner eller dependencies som bieffekt av refaktorering utan separat motiv, riskbedömning och verifiering.
5. Om flera profiler matchar får de kombineras, exempelvis `javascript-typescript` + `react`.
6. Om evidensen är svag används `generic-backend-web` och osäkerheten redovisas.

## Java / Quarkus

### Detektionssignaler
- `pom.xml` eller `build.gradle[.kts]` med Quarkus-plugin/dependencies.
- Maven wrapper (`mvnw`) eller Gradle wrapper (`gradlew`) ska föredras när de finns.

### Heuristiker
- Håll domänlogik separerad från REST-resurser, persistence-entiteter och integrationsdetaljer när detta ger tydligare ansvar och testbarhet.
- Granska transaktionsgränser, CDI-scope och persistence-livscykel när refaktorering flyttar ansvar.
- Undvik att göra JPA-entiteter till universella API-/domänmodeller om det skapar stark koppling.
- Var försiktig med byte mellan blocking/reactive, RESTEasy Classic/Reactive eller stora Quarkus-versioner: detta är migrationsarbete, inte normal refaktorering.

### Kommandohärledning
- Maven wrapper: `./mvnw test`, eventuellt projektets befintliga `verify`/formatter/checkstyle-kommandon.
- Gradle wrapper: `./gradlew test` och projektets befintliga check-task.
- Läs `pom.xml`, Gradle-filer och CI innan du antar profiler som native build eller integrationstest.

## JavaScript / TypeScript

### Detektionssignaler
- `package.json`, `tsconfig*.json`, lockfil och scripts.
- `typescript` dependency eller TS-konfiguration ger stark TypeScript-evidens.

### Heuristiker
- Bevara modulgränser och publik API-yta vid filflyttar.
- Granska implicita `any`, osäkra type assertions och duplicerade runtime/type-modeller när de faktiskt skapar risk.
- Skapa inte utility-abstraktioner bara för syntaktisk likhet.
- Byt inte package manager, module system eller TS-target som bieffekt.

### Kommandohärledning
- Använd package managern som indikeras av lockfil/packageManager.
- Härled scripts från `package.json`: exempelvis `test`, `lint`, `typecheck`, `build`.
- Kör inte `npm update`, `pnpm update` eller motsvarande som refaktorering.

## React

### Detektionssignaler
- React dependency i `package.json` och komponent-/entrypointstruktur.
- React-profilen kombineras normalt med JavaScript/TypeScript-profilen.

### Heuristiker
- Dela komponenter efter ansvar och förändringsorsak, inte enbart radantal.
- Skilj UI-state, server-state och domänregler när sammanblandningen orsakar komplexitet.
- Undvik `useMemo`, `useCallback` och state-normalisering utan konkret behov.
- Flytt av kontroller, flöden, feedback eller rendering som påverkar användaren är `ux_change`, inte ren refaktorering.
- Var uppmärksam på effects som används för härledd state eller orkestrering som enklare kan uttryckas direkt, men ändra inte utan beteendeanalys.

### Kommandohärledning
- Följ `package.json`-scripts och befintlig teststack (Vitest/Jest/RTL/Playwright/Cypress etc.).
- Anta inte en test runner från React-versionen.

## Generell backend/webb

### Detektionssignaler
- Server-/API-projekt som saknar en mer specifik aktiv profil, eller blandad teknik där endast generiska mönster är säkra.

### Heuristiker
- Granska boundary mellan transport/API, domän/applikation, persistence och externa integrationer utifrån faktisk komplexitet.
- Säkerställ att felhantering, timeout/retry och resource-livscykel inte försämras när ansvar flyttas.
- Undvik att införa ports/adapters, repositories eller service-lager mekaniskt.

### Kommandohärledning
- Härled från repositoryts manifest, scripts, wrappers, Makefile/Taskfile och CI.
- Om verifieringskommandon inte kan bestämmas säkert: redovisa `unknown` och fråga inte projektet att installera nya verktyg bara för refaktoreringen.

## Dependency-modernisering

Dependency- eller ramverksuppgradering ska normalt vara ett separat steg när den:
- ändrar kompatibilitet eller runtime-beteende,
- kräver migrationskod,
- innebär stora lockfile-diffar,
- ändrar build-/deploymentmodell,
- inte behövs för den identifierade refaktoreringen.

Tillåt endast en dependency-ändring inom ett refaktoreringssteg när den är direkt nödvändig, liten, välmotiverad och verifierbar; dokumentera den uttryckligen.
