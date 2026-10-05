#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

SAFE_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")

CHAT_FILES = [
    "knowledge",
    "schemas",
    "scripts",
    "templates",
]

PLUGIN_SCRIPTS = [
    "derive_next_step.py",
    "detect_technology_profiles.py",
    "generate_refactoring_plan.py",
    "github_pr_decision.py",
    "interpret_progress_command.py",
    "zip_work_status.py",
    "zip_workspace.py",
]

PARITY_MARKERS = [
    "Förstå först, prioritera därefter",
    "Gör nästa steg",
    "Vad är nästa steg?",
    "ny regression",
    "öppen Kodförbättraren-PR",
    "stängd utan merge",
    "komplett ny ZIP",
    "ux_change",
    "ingen refaktorering behövs",
    "Operativ kärna",
    "Auktoritativ status",
]

def normalize_version(raw: str) -> str:
    value = raw.strip()
    if value.startswith("refs/tags/"):
        value = value[len("refs/tags/"):]
    if value.startswith("v") and len(value) > 1 and value[1].isdigit():
        value = value[1:]
    if not SAFE_VERSION.fullmatch(value):
        raise ValueError(f"Ogiltig versionssträng: {raw!r}")
    return value

def zip_tree(source: Path, target: Path) -> None:
    if target.exists():
        target.unlink()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source))
    with zipfile.ZipFile(target) as archive:
        broken = archive.testzip()
    if broken:
        raise RuntimeError(f"Korrupt ZIP {target.name}: {broken}")

def runtime_ignore(directory: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".DS_Store"}:
            ignored.add(name)
        if name.endswith((".pyc", ".pyo", ".swp", ".tmp")):
            ignored.add(name)
    return ignored

def copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, ignore=runtime_ignore)

def load_project_config() -> dict:
    return yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))


def runtime_contract(cfg: dict, runtime_id: str, adapter: dict) -> dict:
    return {
        "schema_version": 1,
        "runtime_id": runtime_id,
        "capabilities": cfg.get("capabilities", {}),
        "artifacts": cfg.get("artifacts", {}),
        "workspace_state": cfg.get("workspace_state", {}),
        "tools": cfg.get("tools", {}),
        "adapter": adapter,
    }


def write_runtime_contract(path: Path, cfg: dict, runtime_id: str, adapter: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(runtime_contract(cfg, runtime_id, adapter), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_chat(version: str, staging: Path) -> Path:
    chat = staging / "chat"
    chat.mkdir(parents=True, exist_ok=True)
    (chat / "assistant").mkdir()
    shutil.copy2(ROOT / "src/instructions/system.md", chat / "assistant/instructions.md")
    cfg = load_project_config()
    write_runtime_contract(
        chat / "assistant/runtime-contract.json",
        cfg,
        "chatgpt_chat",
        {
            "mode": "chat_zip",
            "workspace_first": True,
            "host_tools": True,
            "local_scripts_are_runtime_tools": False,
            "canonical_instruction": "assistant/instructions.md",
        },
    )
    for name in CHAT_FILES:
        src = ROOT / name
        if src.exists():
            shutil.copytree(src, chat / name, ignore=runtime_ignore)

    start = f"""# START HERE – Kodförbättraren {version}

Läs och följ alltid `assistant/instructions.md` som canonical runtime-instruktion.
Knowledge under `knowledge/` fördjupar bedömningarna men ersätter aldrig kärnkontraktet.

För projekt som ZIP eller GitHub-repository: analysera först, skapa en prioriterad plan,
och genomför därefter exakt ett steg när användaren säger **Gör nästa steg** eller **Fortsätt**.
Frågan **Vad är nästa steg?** är read-only.

I ZIP-läge ska en komplett uppdaterad ZIP levereras efter ett lyckat steg.
I GitHub-läge ska faktisk repo-/PR-status läsas innan branch/PR väljs.
"""
    (chat / "START-HERE.md").write_text(start, encoding="utf-8")
    (chat / "runtime.json").write_text(json.dumps({
        "name": "Kodförbättraren",
        "runtime": "chat_zip",
        "version": version,
        "entrypoint": "START-HERE.md",
        "canonical_instruction": "assistant/instructions.md",
        "self_contained": True,
        "requires_project_history": False,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    target = DIST / f"kodforbattraren-chat-{version}.zip"
    zip_tree(chat, target)
    return target

def validate_custom_source(custom: Path) -> None:
    instruction = (custom / "INSTRUCTIONS.md").read_text(encoding="utf-8")
    if len(instruction) > 8000:
        raise RuntimeError(f"Custom GPT-instruktionen är {len(instruction)} tecken (>8000)")
    knowledge = [p for p in (custom / "knowledge").iterdir() if p.is_file()]
    if len(knowledge) > 20:
        raise RuntimeError(f"Custom GPT har {len(knowledge)} Knowledge-filer (>20)")
    missing = [marker for marker in PARITY_MARKERS if marker.lower() not in instruction.lower()]
    if missing:
        raise RuntimeError("Custom GPT saknar kritiska parity-markörer: " + ", ".join(missing))

def build_custom(version: str, staging: Path) -> Path:
    source = ROOT / "src/custom-gpt"
    if not source.exists():
        raise RuntimeError("Saknar src/custom-gpt – kör Custom GPT-kompileringen först")
    custom = staging / "custom-gpt"
    copy_tree(source, custom)
    validate_custom_source(custom)
    cfg = load_project_config()
    write_runtime_contract(
        custom / "runtime-contract.json",
        cfg,
        "chatgpt_custom",
        {
            "mode": "custom_gpt",
            "workspace_first": False,
            "host_tools": True,
            "local_scripts_are_runtime_tools": False,
            "github_write_requires_external_capability": True,
        },
    )
    (custom / "VERSION").write_text(version + "\n", encoding="utf-8")
    target = DIST / f"kodforbattraren-custom-gpt-{version}.zip"
    zip_tree(custom, target)
    return target

def build_opencode(version: str, staging: Path) -> Path:
    cfg = load_project_config()
    out = staging / "opencode"
    out.mkdir(parents=True, exist_ok=True)

    canonical = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    adapter = """\n\n## OpenCode runtime\n\nArbeta workspace-first. Använd värdens fil-, shell-, build/test- och Git-verktyg när de finns. Projektets `scripts/` är hjälpscript och blir inte automatiskt runtime-tools. Muterande kommandon ska följa värdens behörighetsmodell och projektets verifieringskrav.\n"""
    (out / "AGENTS.md").write_text(canonical + adapter, encoding="utf-8")

    opencode_dir = out / ".opencode"
    skill_dir = opencode_dir / "skills" / "kodforbattraren"
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        "# Kodförbättraren\n\n"
        "Analysera före bred förändring. Läs maskinläsbar projektstatus före progression. "
        "Genomför ett avgränsat steg, kör relevant verifiering och markera inte steget klart medan verifiering fallerar. "
        "Fortsätt på relevant öppen PR; efter merge utgå från aktuell default branch.\n",
        encoding="utf-8",
    )
    (out / "opencode.json").write_text(
        json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "permission": {"edit": "ask", "bash": "ask", "skill:*": "allow"},
        }, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_runtime_contract(
        opencode_dir / "runtime-contract.json",
        cfg,
        "opencode",
        {
            "mode": "opencode_workspace",
            "workspace_first": True,
            "host_tools": True,
            "local_scripts_are_runtime_tools": False,
            "canonical_instruction": "AGENTS.md",
            "skill": ".opencode/skills/kodforbattraren/SKILL.md",
        },
    )

    for name in ("knowledge", "schemas", "scripts", "templates"):
        src = ROOT / name
        if src.exists():
            shutil.copytree(src, out / name, ignore=runtime_ignore)

    (out / "README.md").write_text(
        f"# Kodförbättraren – OpenCode {version}\n\n"
        "Öppna projektets workspace i OpenCode. AGENTS.md är runtimeinstruktionen. "
        "OpenCode använder värdens lokala verktyg; scripts/ är stödresurser och deklareras inte som egna runtime-tools.\n",
        encoding="utf-8",
    )
    (out / "VERSION").write_text(version + "\n", encoding="utf-8")

    target = DIST / f"kodforbattraren-opencode-{version}.zip"
    zip_tree(out, target)
    return target


def build_plugin(version: str, staging: Path) -> Path:
    cfg = load_project_config()
    out = staging / "plugin"
    out.mkdir(parents=True, exist_ok=True)

    skill_id = cfg["runtime"]["openai_plugin"]["skill_id"]
    skill = out / "skills" / skill_id
    references = skill / "references"
    scripts_dir = skill / "scripts"
    assets = skill / "assets"
    references.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)

    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": skill_id,
        "version": version,
        "description": "Säker och inkrementell förbättring av befintlig källkod med workspace-first status, verifiering och ZIP/GitHub-flöden.",
    }
    (out / "plugin.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    adapter = {
        "mode": "openai_plugin",
        "skills_first": True,
        "workspace_first": True,
        "canonical_instruction": f"skills/{skill_id}/SKILL.md",
        "state_authority": "workspace_file",
        "state_path": cfg["runtime"]["openai_plugin"]["state_path"],
        "host_tools": True,
        "local_scripts_are_runtime_tools": False,
        "script_resources": {
            "packaged": PLUGIN_SCRIPTS,
            "mcp_required_for_resource_use": False,
        },
        "host_requirements": {
            "filesystem_read": "required",
            "filesystem_write": "required_for_implementation",
            "persistent_state": "required",
            "shell": "required_for_full_parity",
            "code_execution": "required_for_full_parity",
            "github_write": "optional_external_capability",
            "archive_output": "required_for_zip_delivery",
        },
        "fallback_policy": {
            "without_writable_workspace": "analysis_and_planning_only",
            "without_shell_or_code_execution": "do_not_mark_implementation_verified",
            "without_github_write": "github_read_only_or_zip_mode",
            "without_archive_output": "do_not_claim_updated_zip_delivered",
        },
    }
    write_runtime_contract(out / "runtime-contract.json", cfg, "openai_plugin", adapter)

    canonical = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8").strip()
    skill_text = (
        "---\n"
        "name: kodforbattraren\n"
        "description: Säker och inkrementell förbättring av befintlig källkod med faktisk workspace-status och deterministisk verifiering.\n"
        "---\n\n"
        "# Kodförbättraren\n\n"
        "## Plugin-runtime\n\n"
        "- Arbeta workspace-first och läs alltid faktisk maskinläsbar projektstatus före progression.\n"
        "- Samtalsminne ersätter aldrig workspace-state.\n"
        "- Ändra inte kod utan writable workspace.\n"
        "- Markera aldrig ett implementeringssteg verifierat om build/test/lint eller annan obligatorisk kontroll inte faktiskt har körts och passerat.\n"
        "- I GitHub-läge kräver branch/commit/PR en faktisk auktoriserad GitHub-capability; annars arbeta read-only eller använd ZIP-läge.\n"
        "- I ZIP-läge får en komplett uppdaterad ZIP endast påstås levererad när hosten faktiskt kan skapa och integritetskontrollera arkivet.\n"
        "- Paketerade Pythonfiler är stödresurser, inte canonical tools, och kräver ingen MCP-wrapper enbart för att användas.\n"
        "- Projektets egna build/release/CI-validatorer ingår inte i Plugin-runtime-resurserna.\n\n"
        "## Canonical behavior\n\n"
        + canonical
        + "\n"
    )
    (skill / "SKILL.md").write_text(skill_text, encoding="utf-8")

    shutil.copytree(ROOT / "knowledge", references / "knowledge", ignore=runtime_ignore)
    shutil.copytree(ROOT / "schemas", references / "schemas", ignore=runtime_ignore)
    policy_target = references / "runtime-policy"
    policy_target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "src/runtime-policy/operational-execution-policy.md", policy_target / "operational-execution-policy.md")
    shutil.copytree(ROOT / "templates", assets / "templates", ignore=runtime_ignore)

    for script_name in PLUGIN_SCRIPTS:
        shutil.copy2(ROOT / "scripts" / script_name, scripts_dir / script_name)

    (out / "README.md").write_text(
        f"# Kodförbättraren – OpenAI Plugin {version}\n\n"
        "Skills-first peer runtime med equivalent_runtime_dependent parity. "
        "Full implementation kräver writable workspace, persistent state, shell/code execution och vid behov GitHub/archive-capability. "
        "Paketerade scripts är stödresurser och kräver inte MCP-wrapper.\n",
        encoding="utf-8",
    )
    (out / "VERSION").write_text(version + "\n", encoding="utf-8")

    target = DIST / f"kodforbattraren-plugin-{version}.zip"
    zip_tree(out, target)
    return target


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True, help="Release-tag eller versionsnummer, t.ex. v1.0.0")
    args = parser.parse_args()
    try:
        version = normalize_version(args.version)
        DIST.mkdir(exist_ok=True)
        # Ta bort äldre genererade distributions-ZIP:ar så en release aldrig råkar
        # ladda upp artefakter från en tidigare lokal/CI-körning.
        for pattern in ("kodforbattraren-chat-*.zip", "kodforbattraren-custom-gpt-*.zip", "kodforbattraren-opencode-*.zip", "kodforbattraren-plugin-*.zip"):
            for old in DIST.glob(pattern):
                old.unlink()
        manifest_path = DIST / "release-manifest.json"
        if manifest_path.exists():
            manifest_path.unlink()

        staging = DIST / ".staging"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir()

        chat = build_chat(version, staging)
        custom = build_custom(version, staging)
        opencode = build_opencode(version, staging)
        plugin = build_plugin(version, staging)

        manifest = {
            "version": version,
            "artifacts": {
                chat.name: {"sha256": checksum(chat)},
                custom.name: {"sha256": checksum(custom)},
                opencode.name: {"sha256": checksum(opencode)},
                plugin.name: {"sha256": checksum(plugin)},
            },
        }
        (DIST / "release-manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        shutil.rmtree(staging)
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
