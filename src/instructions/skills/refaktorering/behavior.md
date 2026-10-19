## 3. Små, verifierbara steg

Föredra inkrementella transformationer framför stora omskrivningar.

Ett genomförandesteg ska normalt:

- ha ett tydligt mål,
- ha begränsad och begriplig diff,
- kunna verifieras oberoende,
- lämna projektet i ett användbart och helst grönt tillstånd,
- inte blanda flera orelaterade problem,
- dokumentera vad som ändrades och varför.

Om ett planerat steg innehåller flera riskfyllda ansvar, flera oberoende beteendeförändringar eller inte rimligen kan verifieras som en enhet ska du dela upp det innan implementation.

Gör inte en full rewrite när en säker inkrementell väg finns. Byt inte ramverk, huvudarkitektur eller centrala dependencies som en bieffekt av refaktorering utan uttryckligt och välmotiverat beslut.

## 4. Verifiering och testskydd

Före en riskfylld förändring ska du förstå hur befintligt beteende verifieras.

Använd i första hand befintliga tester, build, lint, typkontroll och andra projektspecifika kontroller. Om viktig legacy-logik saknar skydd och refaktoreringen riskerar att ändra beteende ska du överväga characterization tests eller annan fokuserad verifiering innan strukturen ändras.

Efter varje genomfört steg ska relevanta kontroller köras när verktyg och projekt gör det möjligt. Redovisa fel öppet; markera inte steget som klart om dess klart-kriterier eller nödvändig verifiering inte är uppfyllda.

För riskfyllda förändringar ska du etablera en reproducerbar baseline före produktionsändringen. Om tester redan är röda ska du dokumentera de befintliga felen och skilja dem från nya regressioner; samma kända fel kan innebära `pass_with_known_red`, men får aldrig beskrivas som helt grönt. Anpassa verifieringen efter förändringens konsekvensrisk, inte bara diffstorlek.

Om ett hög-risksteg saknar tillförlitligt testskydd ska du normalt skapa ett mindre förberedande skyddssteg, använda fokuserade characterization tests eller markera steget blockerat. Gör inte tester svagare enbart för att få refaktoreringen att passera. Stoppa eller rulla tillbaka när en ny regression inte kan isoleras inom stegets scope, när oplanerad beteendeförändring krävs eller när diffen växer så mycket att steget inte längre kan verifieras oberoende.

När Knowledge är tillgänglig ska `knowledge/refactoring-test-safety.md` användas som fördjupning för risknivåer, baseline, characterization tests och stopp-/rollback-beslut.

