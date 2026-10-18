# Installation, updates and recovery

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
