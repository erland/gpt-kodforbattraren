#!/usr/bin/env python3
"""Stamp generated Skill metadata from the release version; refresh delivery hashes."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stamp(content: str, version: str) -> str:
    """Update YAML frontmatter without creating duplicate headers or literal escapes."""
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?=\r?\n|$)", content, flags=re.DOTALL)
    if not match:
        frontmatter = f'---\nmetadata:\n  version: "{version}"\n---\n\n'
        return frontmatter + content
    frontmatter = match.group(1)
    if re.search(r"(?m)^metadata:\s*$", frontmatter):
        if re.search(r"(?m)^  version:", frontmatter):
            frontmatter = re.sub(r'(?m)^  version:.*$', f'  version: "{version}"', frontmatter)
        else:
            frontmatter = re.sub(r"(?m)^metadata:\s*$", f'metadata:\n  version: "{version}"', frontmatter)
    else:
        frontmatter += f'\nmetadata:\n  version: "{version}"'
    return "---\n" + frontmatter + "\n---" + content[match.end():]

def main(dist: Path, version: str) -> None:
    if not (version == "migration-ci" or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-.][A-Za-z0-9.-]+)?", version)):
        raise ValueError("Invalid version")
    changed = {}
    total = 0
    for package in sorted(dist.glob("kodforbattraren-*.zip")):
        with zipfile.ZipFile(package) as source:
            filenames = source.namelist()
            skills = [n for n in filenames if n.endswith("/SKILL.md")]
            if not skills:
                continue
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w") as dest:
                for member in source.infolist():
                    data = source.read(member.filename)
                    if member.filename in skills:
                        data = stamp(data.decode("utf-8"), version).encode("utf-8")
                        total += 1
                    dest.writestr(member, data)
        package.write_bytes(output.getvalue())
        with zipfile.ZipFile(package) as verify:
            assert verify.testzip() is None
            for skill in skills:
                content = verify.read(skill).decode("utf-8")
                assert '  version: "' + version + '"' in content.split("---", 2)[1], skill
        changed[package.name] = (sha(package), package.stat().st_size)
    if not total:
        raise ValueError("No generated Skill files found")

    manifest_file = dist / "DELIVERY-MANIFEST.json"
    checksum_file = dist / "SHA256SUMS.txt"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert manifest["version"] == version, "Delivery version mismatch"
    lines = checksum_file.read_text(encoding="utf-8").splitlines()
    updated = []
    for line in lines:
        match = re.fullmatch(r"([a-f0-9]{64})  (.+)", line)
        if not match:
            raise ValueError("Invalid SHA256SUMS line: " + line)
        filename = match.group(2)
        digest = changed[filename][0] if filename in changed else match.group(1)
        updated.append(digest + "  " + filename)
    checksum_file.write_text("\n".join(updated) + "\n", encoding="utf-8")
    for entry in manifest["artifacts"]:
        filename = entry.get("file")
        if filename in changed:
            entry["sha256"], entry["size"] = changed[filename]
        elif filename == checksum_file.name:
            entry["sha256"] = sha(checksum_file)
            entry["size"] = checksum_file.stat().st_size
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for name,digest in ((p.name,sha(p)) for p in dist.glob("*.zip")):
        assert any(l == digest + "  " + name for l in updated), "Checksum mismatch: " + name
    print(f"PASS stamped {total} generated Skills across {len(changed)} ZIP files: {version}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    main(args.dist, args.version)
