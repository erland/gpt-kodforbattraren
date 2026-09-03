#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".DS_Store"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".swp", ".tmp"}
REQUIRED = [
    "README.md", "PROJECT.md", "STATUS.md", "gpt-project.yaml", "project-status.yaml",
    "src/instructions/system.md", "docs/development-plan.md", "docs/release-readiness.md",
    ".github/workflows/ci.yml", ".github/workflows/release.yml",
]

def main() -> int:
    problems=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): problems.append(f"saknar {rel}")
    for p in ROOT.rglob("*"):
        if p.name in FORBIDDEN_DIRS: problems.append(f"arbetsrest: {p.relative_to(ROOT)}")
        if p.is_file() and p.suffix in FORBIDDEN_SUFFIXES: problems.append(f"arbetsrest: {p.relative_to(ROOT)}")
    # Development-only dev artifacts should not be the final release artifacts.
    for p in (ROOT/"dist").glob("*-0.1.0-dev.zip") if (ROOT/"dist").exists() else []:
        problems.append(f"gammal dev-artefakt i dist: {p.name}")
    if problems:
        for p in problems: print("ERROR:", p, file=sys.stderr)
        return 1
    print("PASS project hygiene")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
