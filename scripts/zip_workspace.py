\
#!/usr/bin/env python3
"""Safe ZIP import/package helpers for Kodförbättraren.

This utility does not execute project code. It provides:
  inspect <zip>
  extract <zip> <workspace>
  manifest <workspace> [--output FILE]
  package <workspace> <zip>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import zipfile

SAFE_EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
SAFE_EXCLUDE_FILES = {".DS_Store", ".coverage", ".eslintcache"}
SAFE_EXCLUDE_SUFFIXES = {".pyc", ".pyo"}

DEFAULT_MAX_ENTRIES = 100_000
DEFAULT_MAX_TOTAL = 2 * 1024 * 1024 * 1024
DEFAULT_MAX_SINGLE = 512 * 1024 * 1024

class ZipSafetyError(RuntimeError):
    pass

def _normalized_member(name: str) -> PurePosixPath:
    if "\x00" in name:
        raise ZipSafetyError("NUL byte in ZIP member")
    # ZIP paths are POSIX-like regardless of host.
    name = name.replace("\\", "/")
    p = PurePosixPath(name)
    if p.is_absolute() or name.startswith("/"):
        raise ZipSafetyError(f"absolute ZIP path rejected: {name!r}")
    if any(part == ".." for part in p.parts):
        raise ZipSafetyError(f"parent traversal rejected: {name!r}")
    if p.parts and ":" in p.parts[0]:
        # Reject drive-like paths such as C:/x.
        raise ZipSafetyError(f"drive-like ZIP path rejected: {name!r}")
    clean = PurePosixPath(*[part for part in p.parts if part not in ("", ".")])
    if str(clean) in ("", "."):
        return PurePosixPath()
    return clean

def _unix_mode(info: zipfile.ZipInfo) -> int:
    return (info.external_attr >> 16) & 0xFFFF

def _reject_special(info: zipfile.ZipInfo) -> None:
    mode = _unix_mode(info)
    if not mode:
        return
    ftype = stat.S_IFMT(mode)
    allowed = {0, stat.S_IFREG, stat.S_IFDIR}
    if ftype not in allowed:
        raise ZipSafetyError(f"symlink/special ZIP entry rejected: {info.filename!r}")

def inspect_zip(path: Path, max_entries=DEFAULT_MAX_ENTRIES,
                max_total=DEFAULT_MAX_TOTAL, max_single=DEFAULT_MAX_SINGLE) -> dict:
    total = 0
    files = 0
    dirs = 0
    with zipfile.ZipFile(path) as zf:
        infos = zf.infolist()
        if len(infos) > max_entries:
            raise ZipSafetyError(f"too many ZIP entries: {len(infos)} > {max_entries}")
        seen = set()
        for info in infos:
            rel = _normalized_member(info.filename)
            _reject_special(info)
            key = str(rel)
            if key in seen and key:
                raise ZipSafetyError(f"duplicate normalized ZIP path: {key!r}")
            seen.add(key)
            if info.file_size > max_single:
                raise ZipSafetyError(f"ZIP member too large: {info.filename!r}")
            total += info.file_size
            if total > max_total:
                raise ZipSafetyError(f"ZIP total uncompressed size exceeds limit: {total}")
            if info.is_dir():
                dirs += 1
            elif key:
                files += 1
    return {"entries": files + dirs, "files": files, "directories": dirs,
            "total_uncompressed_bytes": total}

def safe_extract(path: Path, workspace: Path) -> dict:
    summary = inspect_zip(path)
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            rel = _normalized_member(info.filename)
            _reject_special(info)
            if not str(rel):
                continue
            dest = (workspace / Path(*rel.parts)).resolve()
            if dest != workspace and workspace not in dest.parents:
                raise ZipSafetyError(f"ZIP member escapes workspace: {info.filename!r}")
            if info.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info, "r") as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst)
    return summary

def is_safe_transient(rel: Path) -> bool:
    parts = rel.parts
    if any(part in SAFE_EXCLUDE_DIRS for part in parts):
        return True
    if rel.name in SAFE_EXCLUDE_FILES:
        return True
    if rel.suffix.lower() in SAFE_EXCLUDE_SUFFIXES:
        return True
    return False

def iter_project_files(workspace: Path, include_metadata: bool = True):
    workspace = workspace.resolve()
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if is_safe_transient(rel):
            continue
        if not include_metadata and rel.parts and rel.parts[0] == ".kodforbattraren":
            continue
        yield path, rel

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def build_manifest(workspace: Path) -> dict:
    files = []
    root = hashlib.sha256()
    for path, rel in iter_project_files(workspace, include_metadata=False):
        digest = sha256_file(path)
        size = path.stat().st_size
        rel_s = rel.as_posix()
        files.append({"path": rel_s, "sha256": digest, "size": size})
        root.update(rel_s.encode("utf-8"))
        root.update(b"\0")
        root.update(digest.encode("ascii"))
        root.update(b"\0")
        root.update(str(size).encode("ascii"))
        root.update(b"\n")
    return {"schema_version": 1, "algorithm": "sha256",
            "files": files, "root_digest": root.hexdigest()}

def package_workspace(workspace: Path, output: Path) -> dict:
    workspace = workspace.resolve()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED,
                         allowZip64=True) as zf:
        for path, rel in iter_project_files(workspace, include_metadata=True):
            zf.write(path, rel.as_posix())
            count += 1
    with zipfile.ZipFile(output) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP integrity failure at {bad}")
    return {"files": count, "sha256": sha256_file(output),
            "bytes": output.stat().st_size}

def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("inspect")
    p.add_argument("zip", type=Path)
    p = sub.add_parser("extract")
    p.add_argument("zip", type=Path)
    p.add_argument("workspace", type=Path)
    p = sub.add_parser("manifest")
    p.add_argument("workspace", type=Path)
    p.add_argument("--output", type=Path)
    p = sub.add_parser("package")
    p.add_argument("workspace", type=Path)
    p.add_argument("zip", type=Path)
    args = ap.parse_args()

    if args.cmd == "inspect":
        result = inspect_zip(args.zip)
    elif args.cmd == "extract":
        result = safe_extract(args.zip, args.workspace)
    elif args.cmd == "manifest":
        result = build_manifest(args.workspace)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif args.cmd == "package":
        result = package_workspace(args.workspace, args.zip)
    else:
        raise AssertionError(args.cmd)
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
