#!/usr/bin/env python3
"""Create a *separate* canonical Builder profile; never overwrite legacy configuration.

Example:
 python scripts/prepare_builder_1626.py --engine /path/to/distribution-engine --output /tmp/kod-new
The engine is provided by GPT Byggaren Chat ZIP 1.6.26.
"""
import argparse
from copy import deepcopy
from pathlib import Path
import shutil
import yaml

p=argparse.ArgumentParser()
p.add_argument("--engine",type=Path,required=True)
p.add_argument("--output",type=Path,required=True)
args=p.parse_args()
source=Path(__file__).resolve().parents[1]
engine=args.engine.resolve()
out=args.output.resolve()
if out == source or source in out.parents or out == engine or engine in out.parents:
    p.error("output must be a separate directory outside source and engine")
if out.exists(): p.error("output already exists: "+str(out))
base=yaml.safe_load((engine/"gpt-project.yaml").read_text(encoding="utf-8"))
shutil.copytree(source,out,ignore=shutil.ignore_patterns(".git","dist","build","builder","builder.zip","migration-artifacts","__pycache__",".pytest_cache"))
cfg=yaml.safe_load((out/"gpt-project.yaml").read_text(encoding="utf-8"))
cfg["project"]["description"]="Analys och säker stegvis förbättring av befintliga kodprojekt."
cfg["structure"]=deepcopy(base["structure"])
cfg["build_system"]=deepcopy(base["build_system"])
for name in ("chat_zip","plugin","claude","opencode"):
    cfg.setdefault("runtime",{})[name]=deepcopy(base["runtime"][name])
cfg["runtime"]["opencode"]["skills"]["definitions"]=[]
cfg["runtime"]["custom_gpt"]["enabled"]=False
cfg["runtime"]["openai_plugin"]["enabled"]=False
cfg["instructions"]["mode"]="modular_skills"
cfg["instructions"]["core"]="src/instructions/core.md"
cfg["instructions"]["assembly"]="canonical/modular-assembly.json"
cfg["skills"]={"contract_version":1,"mode":"inferred","resource_policy":"explicit","definitions":[]}
for ident,desc,reference in (
 ("kodanalys","Analysera kodprojekt och prioritera förbättringar","knowledge/code-quality-refactoring.md"),
 ("refaktorering","Genomför avgränsad refaktorering med testskydd","knowledge/refactoring-test-safety.md"),
 ("leverans-och-status","Hantera arbetsstatus och leverans","knowledge/github-pr-workflow.md"),
):
    rel=f"src/instructions/skills/{ident}/behavior.md"
    if not (out/rel).is_file() or not (out/reference).is_file():
        raise SystemExit("Missing required source/reference: "+rel+" / "+reference)
    cfg["skills"]["definitions"].append({
       "id":ident,"name":ident,"description":desc,
       "source":rel,"scripts":[],"references":[reference],"assets":[]})
for item in (engine/"templates").rglob("*"):
    if item.is_file() and item.suffix==".tpl":
        target=out/"templates"/item.relative_to(engine/"templates")
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(item,target)
cfg["release_ready"]["status"]=False
(out/"gpt-project.yaml").write_text(yaml.safe_dump(cfg,sort_keys=False,allow_unicode=True),encoding="utf-8")
print("Prepared separate canonical source:",out)
print("Next: install matching engine scripts in that copy; build and validate. No active configuration was overwritten.")
