# Installation, updates and recovery

## Quick install: skill only

With Node.js/npm and Git installed:

```sh
npx skills add marklindsay99/figma-bro-codex --skill figma-bro --agent codex --global --copy
```

The third-party [skills CLI](https://github.com/vercel-labs/skills) discovers `skills/figma-bro/` and copies its instructions, references, metadata and MIT license to `~/.agents/skills/figma-bro/`. It does not copy this repository's custom agent or run our Python manager. Invoke `$figma-bro` directly. Figma's official plugin and account connection are separate prerequisites for design work.

For a project-only install, omit `--global` and run in that project's root. Avoid installing the same skill at both project and user scope: Codex can discover both. `--copy` avoids a dependency on a symlink target or temporary checkout.

Use the same manager for later operations, preserving local edits first:

```sh
npx skills list --agent codex --global
npx skills update figma-bro --global
npx skills remove figma-bro --global
```

Removal targets this skill across agents in the chosen scope. Omit `--agent codex` for removal: agent-specific removal can leave the shared canonical folder discoverable by Codex when other agents use it.

Omit `--global` for list/remove of a project-only install; use `--project` instead of `--global` for its update. These operations have the skills CLI's behavior, not our manager's backup/rollback guarantees. Do not use these commands on a full setup managed by `scripts/manage.py`.

## Full setup: skill and custom agent

Requires Git, Python 3.9+ and Codex with personal custom-agent support. Ask Codex to install from this repository using the prompt in the [README](../README.md), or run:

```sh
git clone https://github.com/marklindsay99/figma-bro-codex.git
cd figma-bro-codex
python3 scripts/manage.py install
```

The full setup copies the skill to `~/.agents/skills/figma-bro/` and the custom agent to `~/.codex/agents/figma-bro.toml`. Installed copies work independently of the checkout.

When fulfilling an install request as an agent: inspect a reviewed checkout, read this document, and check `python3 scripts/manage.py status --project /path/to/active/project` first. For an existing unmodified managed installation, use `update`; for an absent installation, use `install`. Stop before replacing edited/unmanaged files or resolving duplicates destructively. Report the installed paths, duplicate status and the actual Figma connection state. Keep project instructions and design profiles in the target project; installation does not authorize editing them.

Update or uninstall from the retained checkout:

```sh
git pull --ff-only
python3 scripts/manage.py update
python3 scripts/manage.py uninstall
```

If transitioning from the skill-only route, first preserve any edits and remove that skill with its original installer, then run the full setup. If transitioning from the full setup, use its `uninstall` before the quick command. Uninstall can restore an earlier baseline: inspect the reported paths and any restored files before switching. Never use two managers to update the same targets.

## Managed installation safety

Run the reviewed `scripts/manage.py` with Python 3.9+ from this checkout. It uses only the standard library and copies a small allowlisted payload. The script is relocatable; the installed files refer to the active project and official integrations, not the source checkout.

## Existing files

A clean install is:

```sh
python3 scripts/manage.py install
```

A second run is idempotent. A managed update is `python3 scripts/manage.py update`. The manager checks hashes before updating or uninstalling; local modifications or added files cause refusal.

If you have inspected an existing unmanaged installation or intentionally want to replace local edits:

```sh
python3 scripts/manage.py install --replace
```

This explicitly snapshots the existing targets before replacement. Updates retain the original pre-install baseline. Uninstall restores that baseline, rather than the preceding package version. Backups are retained for manual recovery; they can contain your prior private instructions and belong in your private home directory.

State and backups live under `~/.codex/figma-bro-codex/`. No credentials or global config are read or written. The two destinations are copied through a guarded transaction; failure rolls back target changes. Unexpected target types, symlinks and unsafe state pointers are refused. Close other installers before running one; a lock prevents simultaneous manager operations. If a process is killed or the machine loses power, inspect retained backups and staging directories before recovery. A stale lock is removed manually only after verifying its recorded process is no longer running; the manager does not guess at crash recovery.

If edited files block uninstall, preserve/reconcile your edits first. An explicit install --replace snapshots them; subsequent uninstall restores the initial baseline. Do not delete an installation-state file to bypass protection.

## Duplicate definitions

Codex does not merge same-name skills. Check each active repository:

```sh
python3 scripts/manage.py status --project /path/to/repository
```

This reports project/legacy same-name skill and custom-role definitions. Install/update with --project refuses duplicates before changing files. The manager never deletes project files.

Preserve project-specific context in `.figma-bro/design-profile.md` and its references. Remove the old project `.agents/skills/figma-bro/` and `.codex/agents/figma-bro.toml` in that project's own reviewed commit. Also inspect any legacy `.codex/skills` definitions. Keep prior commits/backups for recovery. Do not keep a renamed folder whose SKILL.md still declares name: figma-bro inside a discovery path. Check status again; one enabled personal definition should remain.

The separately named global figma-product-design skill is a different capability, not a duplicate of figma-bro; this installer leaves unrelated skills alone.

## Fresh sessions and account connection

Restart/start a fresh Codex chat after installation. Verify one discovered figma-bro skill at the personal path and native selection of figma_bro. Configure Figma in the parent session with access to the target file/libraries; the role inherits that connection. No Figma token environment variable is required by the package. Use the integration's supported authentication, never a committed token.

## Testing without changing your installation

`--home-root /temporary/directory` targets an isolated test home for lifecycle tests. It never reassigns the HOME or CODEX_HOME environment variables. It is not a way to change the active Codex home; default personal paths remain the documented installation.
