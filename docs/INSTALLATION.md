# Installation, updates and recovery

## Full setup: skill, custom agent and Figma guidance

Requires Node.js 18+/npm, Git, Python 3.9+ available as `python3`, and Codex with personal custom-agent support. Run in the project you want to design for:

```sh
npx --yes github:marklindsay99/figma-bro-codex
```

This downloads the public GitHub package, installs both `~/.agents/skills/figma-bro/` and `~/.codex/agents/figma-bro.toml` through the existing Python manager, then displays the [Figma connection steps and verification prompt](CONNECTING-FIGMA.md). No npm registry publication or account is required. The manifest has no lifecycle scripts or runtime dependencies. `private: true` prevents accidental registry publication; it does not prevent installation from GitHub.

The active project defaults to your calling directory, not the npm cache. Nested directories are checked through their Git root for duplicate definitions. To target a different project, append `--project /path/to/repository`. Project instructions and profiles stay in that project; installation does not modify them.

Existing unmodified managed installations update safely. Edited or unmanaged files are refused with a concrete message. To inspect the installation or repeat the connection guide:

```sh
npx --yes github:marklindsay99/figma-bro-codex status
npx --yes github:marklindsay99/figma-bro-codex connect
```

`connect` only displays guidance. Complete browser authentication through the official Figma plugin in Codex; the verification prompt checks live access in that chat. Installing local files does not authenticate Figma or prove file-edit permissions.

## Updates and uninstall

```sh
npx --yes github:marklindsay99/figma-bro-codex update
npx --yes github:marklindsay99/figma-bro-codex uninstall
```

These use the same installation state and backups as earlier full setups. They work without keeping a checkout. Rerunning the default command is idempotent when current. The explicit `update` requires a managed installation. Modified files remain protected, and uninstall restores the original baseline.

## Existing skill-only installation

Preserve local edits, then remove the skill using its original installer before the full setup. For the skills CLI, `npx skills remove figma-bro --global` removes that skill across agents in user scope; omit `--global` for project scope. Agent-specific removal can leave the shared canonical folder discoverable.

Alternatively, after inspecting the existing files, `npx --yes github:marklindsay99/figma-bro-codex --replace` explicitly backs up and replaces unmanaged/edited targets. The prior files become the pre-install baseline and return on uninstall. This does not transfer another installer's lock metadata; stop updating these targets with that other installer while the full setup manages them. Symlinks and duplicate project/user definitions still require resolution first.

## Manual fallback and install requests in Codex

The standard-library Python installer remains available without Node.js:

```sh
git clone https://github.com/marklindsay99/figma-bro-codex.git
cd figma-bro-codex
python3 scripts/manage.py install --project /path/to/your/repository
```

Use `python3 scripts/manage.py update`, `status` or `uninstall` from that checkout for later operations, and read the [Figma connection guide](CONNECTING-FIGMA.md). Unlike the npx wrapper, direct Python calls only check projects explicitly supplied with `--project`.

You can ask Codex: "Install Figma Bro from https://github.com/marklindsay99/figma-bro-codex. Read its AGENTS.md, install both the skill and custom agent, preserve existing configuration, and guide me through connecting Figma."

When fulfilling that request as an agent: inspect this repository, follow the full setup, check the managed status and active project's duplicates, and report actual installation and connection results separately. Preserve edited/unmanaged files and resolve conflicts explicitly. Keep project instructions and design profiles in their project.

## Skill-only alternative

```sh
npx skills add marklindsay99/figma-bro-codex --skill figma-bro --agent codex --global --copy
```

The third-party [skills CLI](https://github.com/vercel-labs/skills) copies the skill, references, metadata and license. It does not install the custom agent or run the full installer. Invoke `$figma-bro` directly and follow the [Figma connection guide](CONNECTING-FIGMA.md). Updates use `npx skills update figma-bro --global`; removal uses `npx skills remove figma-bro --global`. Preserve local edits first. Avoid duplicate project/user installs and two managers updating the same paths.

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
