#!/usr/bin/env python3
"""Inventory files changed on disk, independently from an agent review panel."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

WORDS = {
    "en": ("added", "modified", "deleted", "No changed files", "Invalid inventory"),
    "fr": ("ajoutés", "modifiés", "supprimés", "Aucun fichier modifié", "Inventaire invalide"),
    "es": ("añadidos", "modificados", "eliminados", "Ningún archivo modificado", "Inventario no válido"),
}
NOTES = {
    "en": "Compares workspace files, not the files displayed by Codex. Ignored files are excluded.",
    "fr": "Compare les fichiers du répertoire, pas ceux affichés par Codex. Les fichiers ignorés sont exclus.",
    "es": "Compara los archivos del directorio, no los mostrados por Codex. Se excluyen los archivos ignorados.",
}


def git_root(repo):
    command = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if command.returncode:
        raise ValueError("path is not a Git worktree")
    return Path(command.stdout.strip()).resolve()


def snapshot(repo):
    root = git_root(repo)
    command = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                             capture_output=True)
    if command.returncode:
        raise ValueError("git ls-files failed")
    paths = sorted(set(name.decode("utf-8", "surrogateescape") for name in command.stdout.split(b"\0") if name))
    files = {}
    for name in paths:
        path = root / name
        if path.is_symlink():
            data = os.fsencode(os.readlink(path))
        elif path.is_file():
            data = path.read_bytes()
        else:
            continue
        files[name] = hashlib.sha256(data).hexdigest()
    return {"format": 1, "files": files}


def compare(before, after, lang="en"):
    if not isinstance(before, dict) or before.get("format") != 1 or not isinstance(before.get("files"), dict):
        raise ValueError("baseline format is invalid")
    old, new = before["files"], after["files"]
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in old.items()):
        raise ValueError("baseline file hashes are invalid")
    return {"added": sorted(new.keys() - old.keys()),
            "deleted": sorted(old.keys() - new.keys()),
            "modified": sorted(name for name in old.keys() & new.keys() if old[name] != new[name]),
            "note": NOTES[lang]}


def demo(lang="en"):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
        (root / "app.py").write_text("print('before')\n")
        before = snapshot(root)
        (root / "app.py").write_text("print('after')\n")
        (root / "new.txt").write_text("added\n")
        return compare(before, snapshot(root), lang)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("demo", "snapshot", "compare"))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--lang", choices=WORDS, default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            result = demo(args.lang)
        elif args.command == "snapshot":
            if args.out is None:
                parser.error("snapshot requires --out")
            root = git_root(args.repo)
            if args.out.resolve().is_relative_to(root):
                parser.error("store the baseline outside the worktree")
            result = snapshot(root)
            args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        else:
            if args.baseline is None:
                parser.error("compare requires --baseline")
            result = compare(json.loads(args.baseline.read_text(encoding="utf-8")), snapshot(args.repo), args.lang)
    except (ValueError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"{WORDS[args.lang][4]}: {type(error).__name__}", file=sys.stderr)
        return 1
    if args.json or args.command == "snapshot":
        print(json.dumps(result, ensure_ascii=False))
    else:
        labels = WORDS[args.lang]
        if not any(result[key] for key in ("added", "modified", "deleted")):
            print(labels[3])
        for key, label in zip(("added", "modified", "deleted"), labels):
            if result[key]:
                print(f"{label}: {', '.join(result[key])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
