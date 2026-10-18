# figma-bro-codex

A reusable Codex designer for editable Figma product screens, visual inspection, revisions and engineering handoff. It reads the active project's instructions and optional design profile; brands, private references and approval decisions stay with that project.

An independent adaptation, not the original Figma Bro template or an official Figma/OpenAI product. The code, documentation, generic workflow and fictional examples authored for this package are [MIT licensed](LICENSE). Third-party services and excluded source material retain their own rights; see [attribution and license scope](docs/ATTRIBUTION.md).

## Install

Requires Python 3.9+, Codex with personal custom-agent support and a connected official Figma plugin for design work. No third-party Python packages are needed.

```sh
python3 scripts/manage.py install
python3 scripts/manage.py status --project /path/to/your/repository
```

The installer copies the skill to `~/.agents/skills/figma-bro/` and the personal role to `~/.codex/agents/figma-bro.toml`. It does not edit global config, connect accounts or change subscriptions. Existing unmanaged/edited files are refused unless you explicitly choose the documented backup-and-replace path. The installed copies do not depend on this checkout.

Start a fresh Codex chat in your target repository. Ask:

> Have figma_bro use $figma-bro to design this feature in the supplied Figma destination, inspect the relevant states and return a draft handoff.

You can also invoke `$figma-bro` directly. Model/reasoning and integrations inherit from the parent session.

## Project context

Read the [profile contract](skills/figma-bro/references/project-profile.md). The optional default is `.figma-bro/design-profile.md` in the active repository; AGENTS.md can name another profile. Missing optional profiles fall back to the current brief and repository guidance. Context is resolved from the active project, never the installation directory or another customer's previous task.

See the [fictional brief](examples/brief.md), [example project instructions](examples/AGENTS.md) and [example profile](examples/.figma-bro/design-profile.md). No private examples or design captures are bundled.

## Update and uninstall

```sh
git pull --ff-only
python3 scripts/manage.py update
python3 scripts/manage.py uninstall
```

Update from a reviewed checkout. Modified installations are protected. Uninstall removes managed copies and restores any files present before the first install. Backups remain in `~/.codex/figma-bro-codex/backups/`. See [installation/recovery](docs/INSTALLATION.md), including duplicate project/user definitions.

## Verification and provenance

Run `python3 -m unittest discover -s tests -v` and `python3 scripts/check_package.py`. [Verification](docs/VERIFICATION.md) records runtime coverage; a tool appearing in a catalog is not proof it works.

[Attribution](docs/ATTRIBUTION.md) inventories origins and excluded third-party material. Official Figma tools and skills are documented dependencies, not vendored copies. [Release policy](docs/RELEASE.md) and the [release review](docs/RELEASE-REVIEW.md) document the publication boundaries and verification limits.

Format references: [personal custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [skill discovery](https://learn.chatgpt.com/docs/build-skills), checked 18 October 2026. Installed Codex compatibility must be verified by discovery and actual role dispatch.
