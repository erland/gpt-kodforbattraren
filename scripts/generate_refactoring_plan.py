#!/usr/bin/env python3
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from pathlib import Path
import json
import yaml

PRIORITY = {"critical": 0, "high": 1, "medium": 2, "low": 3, "defer": 4}

def load(path: Path):
    text = path.read_text(encoding="utf-8")
    return json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)

def dump_yaml(data, path: Path):
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

def load_findings(directory: Path):
    items = []
    for path in sorted(directory.glob("*")):
        if path.suffix.lower() not in {".yaml", ".yml", ".json"}:
            continue
        item = load(path)
        if item.get("status") in {"resolved", "accepted", "wont_fix"} or item.get("priority") == "defer":
            continue
        items.append(item)
    return sorted(items, key=lambda f: (PRIORITY.get(f.get("priority"), 99), f["id"]))

def build_plan(analysis: dict, findings: list[dict], args) -> tuple[dict, dict[str, list[str]]]:
    finding_by_id = {f["id"]: f for f in findings}
    allowed = set(analysis.get("findings", []))
    findings = [f for f in findings if f["id"] in allowed]

    steps = []
    mapping: dict[str, list[str]] = {}
    finding_primary_step: dict[str, str] = {}
    counter = 1

    need_guard = (
        analysis.get("baseline", {}).get("testability", {}).get("level") in {"weak", "unknown"}
        and any(
            f.get("priority") in {"critical", "high"}
            and f.get("impact", {}).get("failure_risk") == "high"
            for f in findings
        )
    )
    guard_id = None
    if need_guard:
        guard_id = f"R-{counter:03d}"; counter += 1
        risky_ids = [f["id"] for f in findings if f.get("priority") in {"critical", "high"} and f.get("impact", {}).get("failure_risk") == "high"]
        steps.append({
            "id": guard_id, "order": len(steps)+1,
            "title": "Etablera testskydd för riskfyllda förändringar",
            "goal": "Skapa reproducerbar baseline och fokuserat beteendeskydd innan hög-riskkod ändras.",
            "status": "ready", "change_classification": "refactoring",
            "finding_ids": risky_ids, "depends_on": [], "scope": [],
            "out_of_scope": ["Produktionsbeteende ska inte ändras i detta steg."],
            "risk": "low",
            "done_when": ["Relevant baseline är dokumenterad.", "Kritiska befintliga beteenden kan verifieras reproducerbart."],
            "verification": ["Kör de nya/fokuserade testerna och relevanta befintliga kontrollerna."],
            "notes": "Skyddssteg skapat eftersom testability är weak/unknown och minst en högprioriterad finding har high failure_risk."
        })
        for fid in risky_ids:
            mapping.setdefault(fid, []).append(guard_id)

    # Create one primary implementation step per finding. This is intentionally conservative.
    for f in findings:
        sid = f"R-{counter:03d}"; counter += 1
        deps = []
        if guard_id and f.get("priority") in {"critical", "high"} and f.get("impact", {}).get("failure_risk") == "high":
            deps.append(guard_id)
        risk = "high" if f.get("impact", {}).get("failure_risk") == "high" else ("medium" if f.get("priority") in {"critical", "high"} else "low")
        steps.append({
            "id": sid, "order": len(steps)+1,
            "title": f["title"],
            "goal": f["recommended_action"],
            "status": "planned", "change_classification": f["change_classification"],
            "finding_ids": [f["id"]], "depends_on": deps,
            "scope": [e["path"] for e in f.get("evidence", [])],
            "out_of_scope": [], "risk": risk,
            "done_when": [f"Finding {f['id']} är åtgärdad eller explicit omklassificerad med evidens.", "Ändringen håller sig inom stegets definierade scope."],
            "verification": ["Kör relevanta tester/build/lint/typkontroller för berört område.", "Kontrollera att inga oplanerade beteendeförändringar introducerats."],
            "notes": f.get("rationale", "")
        })
        finding_primary_step[f["id"]] = sid
        mapping.setdefault(f["id"], []).append(sid)

    # Translate finding dependencies into step dependencies.
    for dep in analysis.get("dependencies", []):
        before, after = dep["before"], dep["after"]
        if before in finding_primary_step and after in finding_primary_step:
            target = next(s for s in steps if s["id"] == finding_primary_step[after])
            predecessor = finding_primary_step[before]
            if predecessor not in target["depends_on"]:
                target["depends_on"].append(predecessor)

    # Mark runnable non-guard steps ready if dependencies are empty.
    for s in steps:
        if s["status"] == "planned" and not s["depends_on"]:
            s["status"] = "ready"

    plan = {
        "schema_version": 1,
        "plan_id": args.plan_id,
        "project": {"name": args.project_name, **({"repository": args.repository} if args.repository else {})},
        "source_snapshot": {"mode": args.mode, "captured_at": args.captured_at, "base_identifier": args.base_identifier},
        "objectives": ["Genomför prioriterade förbättringar inkrementellt och verifierbart."],
        "constraints": ["Undvik rewrites och orelaterade förändringar.", "Beteendeförändringar ska klassificeras explicit."],
        "steps": steps,
    }
    return plan, mapping

def render_markdown(plan: dict, mapping: dict[str, list[str]], analysis: dict) -> str:
    lines = [f"# Refaktoreringsplan – {plan['project']['name']}", "", "## Sammanfattning", "",
             "Planen är genererad från den prioriterade initialanalysen och ska genomföras stegvis.", "",
             "## Källsnapshot", "", f"- Läge: `{plan['source_snapshot']['mode']}`", f"- Identifierare: `{plan['source_snapshot'].get('base_identifier','')}`", f"- Fångad: {plan['source_snapshot']['captured_at']}", "",
             "## Mål", ""]
    lines += [f"- {o}" for o in plan["objectives"]]
    lines += ["", "## Begränsningar", ""] + [f"- {c}" for c in plan.get("constraints", [])]
    lines += ["", "## Genomförandeplan", ""]
    for s in sorted(plan["steps"], key=lambda x: x["order"]):
        lines += [f"### {s['id']} – {s['title']}", "", f"**Mål:** {s['goal']}", "", f"**Klassificering:** `{s['change_classification']}`  ", f"**Risk:** `{s['risk']}`  ", f"**Status:** `{s['status']}`", ""]
        if s["finding_ids"]: lines += ["**Findings:** " + ", ".join(f"`{x}`" for x in s["finding_ids"]), ""]
        if s["depends_on"]: lines += ["**Beroenden:** " + ", ".join(f"`{x}`" for x in s["depends_on"]), ""]
        lines += ["**Klart när:**"] + [f"- {x}" for x in s["done_when"]]
        lines += ["", "**Verifiering:**"] + [f"- {x}" for x in s["verification"]] + [""]
    lines += ["## Finding → steg", ""]
    for fid in sorted(mapping): lines.append(f"- `{fid}` → " + ", ".join(f"`{s}`" for s in mapping[fid]))
    lines += ["", "## Medvetna non-actions från analysen", ""]
    for item in analysis.get("non_actions", []):
        lines.append(f"- **{item['decision']}** – {item['observation']}: {item['reason']}")
    lines += ["", "## Omplanering", "", "Om ny evidens, blockerare eller källdrift uppstår ska planändringen registreras explicit i work status innan arbetet fortsätter.", ""]
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--analysis", required=True, type=Path)
    p.add_argument("--findings-dir", required=True, type=Path)
    p.add_argument("--out-plan", required=True, type=Path)
    p.add_argument("--out-markdown", required=True, type=Path)
    p.add_argument("--plan-id", default="refactoring-plan-1")
    p.add_argument("--project-name", required=True)
    p.add_argument("--mode", choices=["zip", "github"], required=True)
    p.add_argument("--base-identifier", required=True)
    p.add_argument("--repository")
    p.add_argument("--captured-at", default=datetime.now(timezone.utc).isoformat())
    args = p.parse_args()
    analysis = load(args.analysis)
    findings = load_findings(args.findings_dir)
    plan, mapping = build_plan(analysis, findings, args)
    args.out_plan.parent.mkdir(parents=True, exist_ok=True)
    args.out_markdown.parent.mkdir(parents=True, exist_ok=True)
    dump_yaml(plan, args.out_plan)
    args.out_markdown.write_text(render_markdown(plan, mapping, analysis), encoding="utf-8")
    print(f"Plan: {args.out_plan}")
    print(f"Markdown: {args.out_markdown}")

if __name__ == "__main__": main()
