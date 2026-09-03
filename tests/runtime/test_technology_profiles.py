import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "detect_technology_profiles.py"
FIX = ROOT / "tests" / "fixtures" / "profiles"

def detect(name):
    r = subprocess.run([sys.executable, str(SCRIPT), str(FIX/name)], text=True, capture_output=True, check=True)
    return json.loads(r.stdout)

def test_java_quarkus_profile_and_wrapper_commands():
    d=detect("java-quarkus")
    assert "java-quarkus" in d["profiles"]
    assert "./mvnw test" in d["commands"]["test"]
    assert "./mvnw verify" in d["commands"]["build"]

def test_typescript_profile_derives_package_scripts():
    d=detect("typescript")
    assert d["profiles"] == ["javascript-typescript"]
    assert "pnpm test" in d["commands"]["test"]
    assert "pnpm lint" in d["commands"]["lint"]
    assert "pnpm typecheck" in d["commands"]["typecheck"]

def test_react_combines_profiles_and_uses_declared_scripts():
    d=detect("react")
    assert "javascript-typescript" in d["profiles"] and "react" in d["profiles"]
    assert "npm run build" in d["commands"]["build"]
    assert "npm run test" in d["commands"]["test"]

def test_generic_backend_is_fallback_not_invented_stack():
    d=detect("generic-backend")
    assert d["profiles"] == ["generic-backend-web"]
    assert not d["commands"]["test"]

def test_profile_knowledge_has_dependency_guardrail():
    t=(ROOT/"knowledge"/"technology-profiles.md").read_text(encoding="utf-8").lower()
    assert "modernisera inte" in t
    assert "inte normal refaktorering" in t
