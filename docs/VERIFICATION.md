# Verification — 18 October 2026

Tested with Codex CLI 0.163.0-alpha.10.2 and Python 3.9.6.

| Check | Result |
|---|---|
| Standard-library lifecycle/recovery tests | 20 tests passed: 11 manager lifecycle/recovery, 8 command/onboarding, and 1 installed-license check |
| Full-install npx entrypoint | Actual GitHub-hosted command and packed npm payload exercised in isolated homes: both files, status, repeat/update, caller-project duplicate refusal, connection guidance and uninstall passed. Unit tests additionally cover edited files, replacement/restore and missing Python. |
| Standard skills CLI | Version 1.7.2 discovered the published skill; isolated project copy retained every skill file including references and LICENSE; update check and canonical-folder removal exercised |
| Official Skill Creator frontmatter validation | Passed |
| Source and installed personal-role TOML | Parsed; required fields and role name valid |
| Codex app-server discovery from two repositories | Exactly one enabled figma-bro skill per context, at the personal installation |
| Native personal custom-agent selection | figma_bro selected successfully from both repositories |
| Package repository with no design profile | Used its AGENTS.md, reported profile absent and did not load example/sibling context |
| Independent application repository with private profile | Loaded that project's own profile, required docs and its named approval policy |
| Configured Figma integration | The same selected designer actually called whoami successfully in both repositories |
| Repeat update | Already-current, no duplicate definitions |
| Public-payload checks | Text/local-link/private-reference guards pass; reachable history checked after commit |

The runtime reports are retained privately by the owner. No project names, paths, Figma file IDs, screenshot data or account/team identity are published here. Read-only test sessions reported incidental toolchain-cache write denials; context resolution and Figma calls still completed.

Native Specs/Code Layers were unavailable in the tested connection. whoami proves account integration access, not edit permission to every file. No account or subscription changes were made. Native design-write coverage comes from the existing private benchmark; packaging did not repeat or modify that draft.

That prior benchmark demonstrated editable responsive screens, local linked components, semantic variables, discrete assets, render inspection and visible-defect revisions. Canonical cross-file component import had failed and local equivalents were labelled. Evidence remains with the private project. This does not establish original template/model identity or universal creative quality.

Version 0.1.1 adds MIT distribution notices and release guards; the designer workflow is unchanged. The [release review](RELEASE-REVIEW.md) covers the publication audit. The automated check is not exhaustive privacy or rights clearance.

Version 0.2.0 adds the GitHub-hosted npx entrypoint. Its npm payload is allowlisted and retains MIT notices, attribution and connection guidance; no official plugin code or credentials are bundled. The installation command prints supported connection steps, not a claim of authenticated Figma access. Earlier runtime/design evidence remains unchanged.
