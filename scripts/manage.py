#!/usr/bin/env python3
"""Copy, update and restore the personal Figma Bro installation (stdlib only)."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid

PACKAGE = Path(__file__).resolve().parents[1]
IDENTITY = "figma-bro-codex"


def digest(path):
    if path.is_symlink():
        raise ValueError("Refusing symlink: " + str(path))
    if not path.exists():
        return None
    files = sorted(path.rglob("*")) if path.is_dir() else [path]
    result = {}
    for item in files:
        if item.is_symlink():
            raise ValueError("Refusing symlink: " + str(item))
        if item.is_file():
            key = str(item.relative_to(path)) if path.is_dir() else "."
            result[key] = hashlib.sha256(item.read_bytes()).hexdigest()
    return result


def guard(path, home):
    current = home
    for part in path.relative_to(home).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Refusing symlink: " + str(current))


def declared_name(path):
    try:
        body = path.read_text(encoding="utf-8")[:4096]
    except (OSError, UnicodeError):
        return None
    match = re.search(r"(?m)^name\s*(?::|=)\s*['\"]?([a-zA-Z0-9_-]+)['\"]?\s*(?:#.*)?$", body)
    return match.group(1) if match else None


def skill_files(base):
    if not base.is_dir():
        return []
    # Include top-level symlinked skill folders, which Codex can also discover.
    found = set(base.rglob("SKILL.md"))
    for folder in base.iterdir():
        if (folder / "SKILL.md").is_file():
            found.add(folder / "SKILL.md")
    return sorted(found)


def duplicates(home, projects):
    home = Path(home).expanduser().resolve()
    found = []
    canonical = home / ".agents/skills/figma-bro/SKILL.md"
    for base in [home / ".agents/skills", home / ".codex/skills"]:
        for item in skill_files(base):
            if item != canonical and declared_name(item) == "figma-bro":
                found.append(str(item))
    agent = home / ".codex/agents/figma-bro.toml"
    for item in (home / ".codex/agents").glob("*.toml"):
        if item != agent and declared_name(item) == "figma_bro":
            found.append(str(item))
    for project in projects:
        cwd = Path(project).expanduser().resolve()
        if not cwd.is_dir():
            raise ValueError("Project directory does not exist: " + str(cwd))
        proc = subprocess.run(["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True)
        root = Path(proc.stdout.strip()).resolve() if proc.returncode == 0 else cwd
        folders = [cwd] + [p for p in cwd.parents if p == root or root in p.parents]
        for folder in folders:
            for base in [folder / ".agents/skills", folder / ".codex/skills"]:
                for item in skill_files(base):
                    if declared_name(item) == "figma-bro":
                        found.append(str(item))
            for item in (folder / ".codex/agents").glob("*.toml"):
                if declared_name(item) == "figma_bro":
                    found.append(str(item))
    return sorted(set(found))


class Manager:
    def __init__(self, home, package=PACKAGE):
        self.home = Path(home).expanduser().resolve()
        if self.home == Path("/"):
            raise ValueError("The home root cannot be the filesystem root")
        self.package = Path(package).resolve()
        self.targets = {"skill": self.home / ".agents/skills/figma-bro",
                        "agent": self.home / ".codex/agents/figma-bro.toml"}
        self.root = self.home / ".codex" / IDENTITY
        self.state_path = self.root / "install.json"
        for path in list(self.targets.values()) + [self.state_path]:
            guard(path, self.home)
        if self.targets["skill"].exists() and not self.targets["skill"].is_dir():
            raise ValueError("Skill target must be a directory")
        if self.targets["agent"].exists() and not self.targets["agent"].is_file():
            raise ValueError("Agent target must be a file")

    def hashes(self):
        return {key: digest(path) for key, path in self.targets.items()}

    def state(self):
        if not self.state_path.exists():
            return None
        state = json.loads(self.state_path.read_text())
        if state.get("package") != IDENTITY or state.get("schema") != 1:
            raise ValueError("Unrecognised installation state; preserve it for manual recovery")
        if set(state.get("hashes", {})) != set(self.targets):
            raise ValueError("Invalid installation hashes")
        baseline = state.get("baseline")
        if baseline is not None:
            parts = Path(baseline).parts
            if len(parts) != 2 or parts[0] != "backups" or parts[1] in (".", ".."):
                raise ValueError("Unsafe baseline pointer")
            guard(self.root / baseline, self.home)
        if set(state.get("baseline_hashes", {})) != set(self.targets):
            raise ValueError("Invalid baseline hashes")
        return state

    @contextmanager
    def locked(self):
        guard(self.root, self.home)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        lock = self.root / "manager.lock"
        try:
            descriptor = os.open(str(lock), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise ValueError("Another manager or stale lock exists: " + str(lock))
        try:
            with os.fdopen(descriptor, "w") as stream:
                stream.write(str(os.getpid()) + "\n")
            yield
        finally:
            lock.unlink()

    def snapshot(self, hashes, state):
        if not any(value is not None for value in hashes.values()) and state is None:
            return None
        name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:10]
        relative = "backups/" + name
        folder = self.root / relative
        guard(folder, self.home)
        folder.mkdir(parents=True, mode=0o700)
        for key, path in self.targets.items():
            if hashes[key] is not None:
                self.copy(path, folder / key)
        (folder / "manifest.json").write_text(json.dumps(hashes, indent=2) + "\n")
        if state is not None:
            (folder / "previous-install.json").write_text(json.dumps(state, indent=2) + "\n")
        return relative

    @staticmethod
    def copy(source, target):
        digest(source)  # Refuse linked content before copying it.
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)

    @staticmethod
    def remove(path):
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

    def apply(self, sources, new_state):
        entries = []
        state_temp = None
        try:
            for key, target in self.targets.items():
                guard(target, self.home)
                target.parent.mkdir(parents=True, exist_ok=True)
                stage = Path(tempfile.mkdtemp(prefix=".figma-bro-stage-", dir=str(target.parent)))
                entry = {"target": target, "stage": stage, "moved": False, "written": False}
                entries.append(entry)
                if sources[key] is not None:
                    self.copy(sources[key], stage / "new")
            for key, entry in zip(self.targets, entries):
                target, stage = entry["target"], entry["stage"]
                if target.exists():
                    os.replace(str(target), str(stage / "old"))
                    entry["moved"] = True
                if sources[key] is not None:
                    os.replace(str(stage / "new"), str(target))
                    entry["written"] = True
            if new_state is None:
                self.state_path.unlink()
            else:
                descriptor, name = tempfile.mkstemp(prefix="install-", suffix=".tmp", dir=str(self.root))
                state_temp = Path(name)
                with os.fdopen(descriptor, "w") as stream:
                    json.dump(new_state, stream, indent=2)
                    stream.write("\n")
                os.replace(str(state_temp), str(self.state_path))
        except BaseException:
            for entry in reversed(entries):
                if entry["written"]:
                    self.remove(entry["target"])
                if entry["moved"]:
                    os.replace(str(entry["stage"] / "old"), str(entry["target"]))
            raise
        finally:
            for entry in entries:
                shutil.rmtree(entry["stage"], ignore_errors=True)
            if state_temp is not None and state_temp.exists():
                state_temp.unlink()

    def install(self, replace=False, update=False):
        with self.locked():
            state, current = self.state(), self.hashes()
            if update and state is None:
                raise ValueError("No managed installation; use install")
            if state is None and any(value is not None for value in current.values()) and not replace:
                raise ValueError("Existing unmanaged installation; inspect it, then use install --replace to back it up")
            if state is not None and current != state["hashes"] and not replace:
                raise ValueError("Managed files were edited or removed; reconcile edits or explicitly use --replace")
            sources = {"skill": self.package / "skills/figma-bro",
                       "agent": self.package / "agents/figma-bro.toml"}
            wanted = {key: digest(path) for key, path in sources.items()}
            if not sources["skill"].is_dir() or not (sources["skill"] / "SKILL.md").is_file() or not sources["agent"].is_file():
                raise ValueError("Incomplete package payload")
            version = (self.package / "VERSION").read_text().strip()
            if state and current == wanted and state.get("version") == version:
                return {"result": "already-current", "version": version}
            checkpoint = self.snapshot(current, state)
            new_state = {"package": IDENTITY, "schema": 1, "version": version, "hashes": wanted,
                         "baseline": state["baseline"] if state else checkpoint,
                         "baseline_hashes": state["baseline_hashes"] if state else current}
            self.apply(sources, new_state)
            return {"result": "installed", "version": version, "backup": checkpoint}

    def uninstall(self):
        with self.locked():
            state, current = self.state(), self.hashes()
            if state is None:
                if any(value is not None for value in current.values()):
                    raise ValueError("Unmanaged files exist; refusing to delete them")
                return {"result": "not-installed"}
            if current != state["hashes"]:
                raise ValueError("Managed files were edited or removed; preserve and reconcile edits before uninstall")
            sources = {key: None for key in self.targets}
            for key, expected in state["baseline_hashes"].items():
                if expected is not None:
                    if state["baseline"] is None:
                        raise ValueError("Missing baseline backup")
                    source = self.root / state["baseline"] / key
                    guard(source, self.home)
                    if digest(source) != expected:
                        raise ValueError("Baseline backup was changed or removed; refusing restore")
                    sources[key] = source
            checkpoint = self.snapshot(current, state)
            self.apply(sources, None)
            return {"result": "uninstalled", "restored_baseline": state["baseline"], "backup": checkpoint}

    def status(self):
        state, current = self.state(), self.hashes()
        return {"installed": state is not None, "version": state.get("version") if state else None,
                "modified": bool(state and current != state["hashes"]),
                "unmanaged_targets": bool(not state and any(x is not None for x in current.values())),
                "paths": {key: str(path) for key, path in self.targets.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "update", "uninstall", "status"])
    parser.add_argument("--replace", action="store_true", help="Explicitly snapshot and replace unmanaged/edited targets")
    parser.add_argument("--home-root", type=Path, default=Path.home(), help="Isolated home for lifecycle tests")
    parser.add_argument("--project", type=Path, action="append", default=[], help="Check an active project's duplicate definitions")
    args = parser.parse_args()
    try:
        manager = Manager(args.home_root)
        clashes = duplicates(manager.home, args.project)
        if args.action in ("install", "update") and clashes:
            raise ValueError("Duplicate definitions; preserve project context and remove/rename these definitions first: " + ", ".join(clashes))
        if args.replace and args.action not in ("install", "update"):
            raise ValueError("--replace is only valid for install/update")
        if args.action == "status":
            result = manager.status()
        elif args.action == "uninstall":
            result = manager.uninstall()
        else:
            result = manager.install(replace=args.replace, update=args.action == "update")
        result["duplicate_definitions"] = clashes
        print(json.dumps(result, indent=2))
        return 2 if clashes or result.get("modified") or result.get("unmanaged_targets") else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, "Figma Bro manager: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
