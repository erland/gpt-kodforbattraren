#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

LOCK_TO_PM = {
    "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "yarn",
    "package-lock.json": "npm",
    "bun.lockb": "bun",
    "bun.lock": "bun",
}

def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def package_json(root: Path):
    p = root / "package.json"
    if not p.exists(): return None
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return None

def detect(root: Path):
    profiles, evidence = [], []
    pom = read(root / "pom.xml")
    gradle = "\n".join(read(p) for p in list(root.glob("build.gradle*"))[:3])
    if "io.quarkus" in pom or "quarkus-maven-plugin" in pom or "io.quarkus" in gradle:
        profiles.append("java-quarkus"); evidence.append("Quarkus marker in Maven/Gradle build")

    pkg = package_json(root)
    if pkg is not None:
        deps = {}
        for k in ("dependencies", "devDependencies", "peerDependencies"):
            deps.update(pkg.get(k, {}) or {})
        if (root / "tsconfig.json").exists() or "typescript" in deps or any(root.glob("tsconfig*.json")):
            profiles.append("javascript-typescript"); evidence.append("package.json + TypeScript evidence")
        elif pkg:
            profiles.append("javascript-typescript"); evidence.append("package.json JavaScript project")
        if "react" in deps or "react-dom" in deps:
            if "javascript-typescript" not in profiles: profiles.append("javascript-typescript")
            profiles.append("react"); evidence.append("React dependency")

    if not profiles:
        profiles.append("generic-backend-web"); evidence.append("No stronger supported profile detected")
    return profiles, evidence

def package_manager(root: Path, pkg):
    if pkg and isinstance(pkg.get("packageManager"), str):
        return pkg["packageManager"].split("@",1)[0]
    found = [pm for f, pm in LOCK_TO_PM.items() if (root/f).exists()]
    return found[0] if len(found)==1 else ("unknown" if not found else "ambiguous")

def commands(root: Path, profiles):
    result = {"build": [], "test": [], "lint": [], "typecheck": [], "source": []}
    pkg = package_json(root)
    if pkg is not None:
        pm = package_manager(root, pkg)
        run_prefix = {"npm":"npm run", "pnpm":"pnpm", "yarn":"yarn", "bun":"bun run"}.get(pm)
        scripts = pkg.get("scripts", {}) or {}
        for kind, names in {
            "build":["build"], "test":["test"], "lint":["lint"], "typecheck":["typecheck","type-check","check:types"]
        }.items():
            for name in names:
                if name in scripts and run_prefix:
                    result[kind].append(f"{run_prefix} {name}")
                    break
        result["source"].append(f"package.json scripts; package manager={pm}")
    if "java-quarkus" in profiles:
        if (root/"mvnw").exists():
            result["test"].append("./mvnw test")
            result["build"].append("./mvnw verify")
            result["source"].append("Maven wrapper")
        elif (root/"gradlew").exists():
            result["test"].append("./gradlew test")
            result["build"].append("./gradlew check")
            result["source"].append("Gradle wrapper")
        elif (root/"pom.xml").exists():
            result["test"].append("mvn test")
            result["build"].append("mvn verify")
            result["source"].append("pom.xml; no wrapper")
    return result

def main():
    root = Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
    profiles, evidence = detect(root)
    out = {"root": str(root), "profiles": profiles, "evidence": evidence, "commands": commands(root, profiles),
           "dependency_policy":"Do not modernize dependencies/frameworks without explicit, evidenced motive."}
    print(json.dumps(out, ensure_ascii=False, indent=2))
if __name__ == "__main__": main()
