# Kända begränsningar

1. **GitHub write-capability är miljöberoende.** Custom GPT och Chat-runtime kan bara skapa branches,
   commits och PR:ar när den körande miljön faktiskt erbjuder en auktoriserad GitHub write-connector/action.
   Utan den ska GPT:n vara read-only mot GitHub och använda ZIP-läget för kodändringar.
2. **Automatiska E2E-tester verifierar kontrakt och beslutslogik, inte en språkmodell på alla verkliga kodbaser.**
   Releasekvalitet bör därför kompletteras med provkörningar på representativa Java/Quarkus- och React/TypeScript-projekt.
3. **Teknikprofilerna är medvetet selektiva.** Java/Quarkus, JavaScript/TypeScript, React och generell backend/webb
   har explicit stöd. Andra stacks analyseras generellt tills fler profiler tillkommer.
4. **UX-slutsatser från enbart kod är hypoteser när faktisk användning inte kan observeras.**
5. **Custom GPT har plattformsgränser.** Kompilerad instruktion och Knowledge är därför en kondenserad variant av Chat ZIP,
   men kritiska beteendekrav ska vara paritetsbevarade.
