# figma-bro-codex

A reusable Codex designer for editable Figma product screens, visual inspection, revisions and engineering handoff. It reads the active project's instructions and optional design profile; brands, private references and approval decisions stay with that project.

An independent adaptation, not the original Figma Bro template or an official Figma/OpenAI product. The code, documentation, generic workflow and fictional examples authored for this package are [MIT licensed](LICENSE). Third-party services and excluded source material retain their own rights; see [attribution and license scope](docs/ATTRIBUTION.md).

## Install

Paste this into Codex for the full setup:

```text
Install Figma Bro from https://github.com/marklindsay99/figma-bro-codex.
Read its AGENTS.md and follow the full setup in docs/INSTALLATION.md to
install both the skill and figma_bro custom agent. Preserve existing
configuration and report any Figma connection still needed.
```

Or install just the skill with one terminal command:

```sh
npx skills add marklindsay99/figma-bro-codex --skill figma-bro --agent codex --global --copy
```

This uses the third-party [skills CLI](https://github.com/vercel-labs/skills), requires Node.js/npm and Git, and copies the skill and its references to `~/.agents/skills/figma-bro/`. No manual clone or Python is needed for this route. It does not install the optional custom agent. If you already used our full installer, keep using that installer for updates; do not install over its managed files with another tool.

Start a fresh Codex chat in your project and ask:

> Use $figma-bro to design this feature in the supplied Figma destination, inspect the relevant states and return a draft handoff.

For design work, install/connect the official Figma plugin and allow access to the destination file and libraries. The skill supplies the workflow; it does not bundle Figma tooling or credentials. See [tool requirements](skills/figma-bro/references/tools.md).

The [full setup](docs/INSTALLATION.md#full-setup-skill-and-custom-agent) also installs `~/.codex/agents/figma-bro.toml` and provides backup, safe update and uninstall support. It requires Python 3.9+ and Codex with personal custom-agent support. After that setup you can ask Codex to have `figma_bro` use `$figma-bro`. Model/reasoning and integrations inherit from the parent session.

## Project context

Read the [profile contract](skills/figma-bro/references/project-profile.md). The optional default is `.figma-bro/design-profile.md` in the active repository; AGENTS.md can name another profile. Missing optional profiles fall back to the current brief and repository guidance. Context is resolved from the active project, never the installation directory or another customer's previous task.

See the [fictional brief](examples/brief.md), [example project instructions](examples/AGENTS.md) and [example profile](examples/.figma-bro/design-profile.md). No private examples or design captures are bundled.

## Update and uninstall

For the one-command skill installation:

```sh
npx skills update figma-bro --global
npx skills remove figma-bro --global
```

Preserve local edits first; removal removes this skill across agents in the chosen scope. For the full setup, use `scripts/manage.py update` or `uninstall` from your checkout; it protects modified installations and restores the pre-install baseline. See [installation/recovery](docs/INSTALLATION.md) for exact commands and switching between the two routes. Choose one manager for the same installation.

## Verification and provenance

Run `python3 -m unittest discover -s tests -v` and `python3 scripts/check_package.py`. [Verification](docs/VERIFICATION.md) records runtime coverage; a tool appearing in a catalog is not proof it works.

[Attribution](docs/ATTRIBUTION.md) inventories origins and excluded third-party material. Official Figma tools and skills are documented dependencies, not vendored copies. [Release policy](docs/RELEASE.md) and the [release review](docs/RELEASE-REVIEW.md) document the publication boundaries and verification limits.

Format references: [personal custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [skill discovery](https://learn.chatgpt.com/docs/build-skills), checked 18 October 2026. Installed Codex compatibility must be verified by discovery and actual role dispatch.
