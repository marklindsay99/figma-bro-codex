# Official Figma dependency and capability checks

Install/connect the official Figma plugin in the parent Codex session. Use its current tools and supplied skills rather than a vendored API manual. The personal role inherits the parent's configured integrations and permissions. This package neither installs a connector nor carries credentials.

Relevant official skills include figma-use for Plugin API execution, figma-generate-design for composed screens, figma-generate-library for components/tokens, and figma-create-new-file before creating a file. Load the official prerequisite for any other tool workflow you actually use. Discover exact current tool schemas instead of copying an old host's call format.

| Needed capability | Supported route | Verify |
|---|---|---|
| Identity and file access | whoami, file reads | Connected account and actual target access, without storing identity secrets |
| Structure, components and tokens | scoped use_figma; metadata/library/search/variable tools when available | Actual hierarchy, font/style/variable data; usable component imports |
| Editable composition | use_figma native Design API | Frames, text, auto layout, linked instances, bindings and persisted geometry |
| Assets | supported upload, source-image-byte transfer or SVG import | Individual asset fill renders and crop/provenance are correct |
| Rendered inspection | get_screenshot or supported native exports | Save durable render bytes and inspect every deliverable |
| Interactions | prototype reaction API and player | Distinguish wiring read-back, static states and actual playback |

REST inspection/Dev Mode alone does not prove canvas-write capability. File-local image hashes and unavailable canonical library imports require an observed fallback, not a claim of parity. Report missing features accurately. Ordinary Markdown and editable text can carry a handoff if native Specs is unavailable.

Code Connect, code layers/Make, motion, FigJam, video, shaders, generative plugins, AI imagery and external workflow runners are optional unless the task needs them. Do not run paid features or alter subscriptions to satisfy an unrelated capability test.

Authenticate through the supported Figma account connection with access to the target file and any required libraries. No credential environment variable is required by this package. If a separately configured integration requires variables, use its official documentation; keep all values in that integration's secret store. Installer state contains only paths, versions and file hashes.

Official references: [Figma MCP](https://developers.figma.com/docs/figma-mcp-server/) and [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents). Available Figma tool surfaces differ; verify editable-write support in the configured session.
