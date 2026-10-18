# figma-bro-codex

A reusable Codex designer for editable Figma product screens, visual inspection, revisions and engineering handoff. It reads the active project's instructions and optional design profile; brands, private references and approval decisions stay with that project.

An independent adaptation, not the original Figma Bro template or an official Figma/OpenAI product. The code, documentation, generic workflow and fictional examples authored for this package are [MIT licensed](LICENSE). Third-party services and excluded source material retain their own rights; see [attribution and license scope](docs/ATTRIBUTION.md).

## Install

Run this from your project directory. Requires Node.js 18+/npm, Git, Python 3.9+ as `python3`, and Codex with personal custom-agent support:

```sh
npx --yes github:marklindsay99/figma-bro-codex
```

One command installs both:

- The skill and its references at `~/.agents/skills/figma-bro/`.
- The custom agent at `~/.codex/agents/figma-bro.toml`.

Then it walks you through installing/connecting the official Figma plugin and gives you a verification prompt for a fresh Codex chat. Figma sign-in happens in its supported browser flow; the installer never handles credentials or claims the connection is verified. You can show the steps again with:

```sh
npx --yes github:marklindsay99/figma-bro-codex connect
```

The command downloads this GitHub package directly; no manual clone or separately published npm package is needed. It uses the existing reversible installer, checks your active project for duplicates, protects edited/unmanaged files, and retains backups. Installed files work independently of the download cache. See [installation and recovery](docs/INSTALLATION.md) and [Figma connection guide](docs/CONNECTING-FIGMA.md).

Start a fresh Codex chat in your project and ask:

> Have figma_bro use $figma-bro to design this feature in the supplied Figma destination, inspect the relevant states and return a draft handoff.

Model/reasoning and integrations inherit from the parent session. The official Figma plugin, account/file permissions and required official skills are dependencies; see [tool requirements](skills/figma-bro/references/tools.md). A [skill-only installation](docs/INSTALLATION.md#skill-only-alternative) remains available through the standard skills CLI.

## Project context

Read the [profile contract](skills/figma-bro/references/project-profile.md). The optional default is `.figma-bro/design-profile.md` in the active repository; AGENTS.md can name another profile. Missing optional profiles fall back to the current brief and repository guidance. Context is resolved from the active project, never the installation directory or another customer's previous task.

See the [fictional brief](examples/brief.md), [example project instructions](examples/AGENTS.md) and [example profile](examples/.figma-bro/design-profile.md). No private examples or design captures are bundled.

## Update and uninstall

```sh
npx --yes github:marklindsay99/figma-bro-codex update
npx --yes github:marklindsay99/figma-bro-codex status
npx --yes github:marklindsay99/figma-bro-codex uninstall
```

Updates protect local modifications; uninstall restores the pre-install baseline. These commands also manage earlier full installations made with `scripts/manage.py`. Keep using the original manager for skill-only installs until you follow the [migration instructions](docs/INSTALLATION.md). Choose one manager for the same files.

## Verification and provenance

Run `python3 -m unittest discover -s tests -v` and `python3 scripts/check_package.py`. [Verification](docs/VERIFICATION.md) records runtime coverage; a tool appearing in a catalog is not proof it works.

[Attribution](docs/ATTRIBUTION.md) inventories origins and excluded third-party material. Official Figma tools and skills are documented dependencies, not vendored copies. [Release policy](docs/RELEASE.md) and the [release review](docs/RELEASE-REVIEW.md) document the publication boundaries and verification limits.

Format references: [personal custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [skill discovery](https://learn.chatgpt.com/docs/build-skills), checked 18 October 2026. Installed Codex compatibility must be verified by discovery and actual role dispatch.
