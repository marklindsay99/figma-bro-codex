#!/usr/bin/env python3
"""Check the working payload and every reachable commit for release hazards."""
import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TOP = {"AGENTS.md", "README.md", "VERSION", ".gitignore", "LICENSE-RECOMMENDATION.md", "LICENSE", "package.json", "bin",
       "skills", "agents", "examples", "docs", "scripts", "tests"}
EXTENSIONS = {".md", ".py", ".json", ".yaml", ".toml", ".cjs"}
PATTERNS = [
    r"figma\.com/(?:design|file|proto)/[A-Za-z0-9]{10,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\bgh[pousr]_[A-Za-z0-9]{30,}",
    r"\bgithub_pat_[A-Za-z0-9_]{40,}",
    r"\bsk-[A-Za-z0-9_-]{30,}",
    r"X-Amz-Signature=[0-9a-fA-F]{20,}",
    r"/" + r"Users/[^/\s]+/",
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def check(name, data, where):
    path = Path(name)
    if path.parts[0] not in TOP or (path.name not in {"VERSION", ".gitignore", "LICENSE"} and path.suffix not in EXTENSIONS):
        raise ValueError("Unexpected payload path: " + where + ":" + name)
    if len(data) > 256 * 1024 or b"\0" in data:
        raise ValueError("Oversized/binary payload: " + where + ":" + name)
    text = data.decode("utf-8")
    if any(re.search(pattern, text) for pattern in PATTERNS):
        raise ValueError("Possible private reference or secret: " + where + ":" + name)


def check_notices():
    license_text = (ROOT / "LICENSE").read_text()
    if not license_text.startswith("MIT License\n"):
        raise ValueError("Missing MIT grant")
    if (ROOT / "skills/figma-bro/LICENSE").read_text() != license_text:
        raise ValueError("Installed skill license differs from root license")
    agent_notice = "".join(("# " + line if line else "#") + "\n" for line in license_text.splitlines())
    if not (ROOT / "agents/figma-bro.toml").read_text().startswith(agent_notice):
        raise ValueError("Installed agent lacks full MIT notice")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-noreply", action="store_true",
                        help="Require GitHub no-reply author/committer emails in reachable history")
    args = parser.parse_args()
    check_notices()
    names = git("ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0")
    count = 0
    for name in filter(None, names):
        path = ROOT / name
        if path.is_symlink():
            raise ValueError("Symlink in package: " + name)
        if not path.exists():
            continue
        data = path.read_bytes()
        check(name, data, "working-tree")
        count += 1
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", data.decode()):
                if "://" not in target and not target.startswith("#"):
                    destination = (path.parent / target.split("#")[0]).resolve()
                    if ROOT not in destination.parents or not destination.exists():
                        raise ValueError("Broken/external local link in " + name + ": " + target)
    # Check reachable history too, so removing a private file from HEAD is insufficient.
    revisions = subprocess.run(["git", "rev-list", "--all"], cwd=ROOT, capture_output=True, text=True)
    if revisions.returncode:
        raise ValueError("Cannot inspect reachable history")
    seen = set()
    for revision in revisions.stdout.splitlines():
        message = git("show", "-s", "--format=%B", revision).decode()
        if any(re.search(pattern, message) for pattern in PATTERNS):
            raise ValueError("Possible private reference/secret in commit message: " + revision[:8])
        if args.require_noreply:
            emails = git("show", "-s", "--format=%ae%n%ce", revision).decode().splitlines()
            if not all(email.endswith("@users.noreply.github.com") for email in emails):
                raise ValueError("Non-no-reply commit identity: " + revision[:8])
        for row in git("ls-tree", "-r", "-z", revision).split(b"\0"):
            if not row:
                continue
            metadata, name = row.split(b"\t", 1)
            mode, kind, oid = metadata.decode().split()
            name = name.decode()
            if kind != "blob" or mode == "120000":
                raise ValueError("Unexpected history object: " + name)
            pair = (oid, name)
            if pair not in seen:
                check(name, git("cat-file", "blob", oid), revision[:8])
                seen.add(pair)
    print("PASS: %d working files; %d unique history file versions; text/link/privacy/license guards" % (count, len(seen)))


if __name__ == "__main__":
    main()
