# Connect Figma in Codex

1. Open Codex in the repository you want to design for. Open Plugins in the app, or type `/plugins` in the interactive Codex CLI. Find the official Figma plugin and install it if needed. If it is already connected, proceed to verification.
2. Choose Connect when prompted. Complete Figma's browser sign-in and authorization using the account with access to your design file and libraries. Return to Codex. Do not paste a token into this installer or commit credentials.
3. Start a fresh chat in that project. Paste the verification prompt below and supply your intended Figma file or node link when asked. The native role must be discovered as `figma_bro`; the skill must appear once as `figma-bro`.
4. Continue design work after verification. A successful identity call proves authentication; reading the chosen file proves its read access. Neither proves canvas-edit permission. The first authorized design task must verify editable writes in its authorized draft and inspect the rendered result. Missing editable-write tools are a capability gap to resolve, not a reason to substitute a flattened screenshot.

Verification prompt to paste into Codex:

```text
Have figma_bro load $figma-bro and this repository's AGENTS.md and optional
design profile. Verify the official Figma plugin connection. If missing,
discover the official plugin and guide me through connecting it using the
supported plugin flow. Use an actual identity call, then ask for a target
file/node link if I have not supplied one. Read that target and inspect a
render where supported. Report authentication, file access, required official
skills, editable-write tools and rendering separately. Do not create or edit
a design, implement product code, or change a subscription during setup.
```

If Figma is unavailable in the plugin directory, check your workspace's allowed plugins and account connection. Use the current official setup instructions below; do not install an unverified substitute or assume a read-only MCP connection can edit the canvas.

Setup reference: https://learn.chatgpt.com/docs/plugins
Figma capability reference: https://developers.figma.com/docs/figma-mcp-server/

The installer prints this guide without inspecting tokens, connecting accounts, opening a browser or starting a model session. Account/tool verification happens in the Codex chat. No Figma credential environment variable is required by this package.
