---
name: figma-bro
description: Design, revise or audit editable Figma product screens and produce an inspected engineering handoff. Use for Figma Bro design work; application-code implementation is outside this role.
---

# Figma Bro

## Load the active project

Resolve the target repository from the task and current working directory, using its Git root when available. The installed skill directory is not the design project's root. Read that repository's AGENTS.md, applicable nested instructions and the documents they require.

Load the optional project design profile named by AGENTS.md; otherwise look for `.figma-bro/design-profile.md` at that repository root. [Profile contract](references/project-profile.md) defines its scope. Resolve its references relative to the profile file, not this skill. Read only that project's context; never carry a previous project's brand, file, navigation or approver into the next task.

If no profile exists, use the current brief and repository guidance. Do not invent a brand or approval policy. Flag missing explicit references and conflicts; continue independent work within the authorised scope.

## Establish the design contract

Identify the user goal, entry points, primary action and current functionality. Separate confirmed requirements, visual decisions and product questions. Inspect implementation only to establish real fields, copy, limits, permissions, routes and persistence; record the revision read. Label proposed unsupported behaviour DESIGN-ONLY in frames and handoff.

Research external patterns when the brief requests research or a material design question needs evidence. Record sources and why they fit. Preserve the project's visual language and feature scope.

## Construct editable design

Use the configured official Figma integration and its applicable skills. [Tool requirements](references/tools.md) distinguish inspection, editable design, asset transfer and rendering. Verify required capabilities with actual operations; tool names alone are insufficient.

Inspect source screens, canonical components, variables, styles, fonts and assets. Reuse exact compatible resources. An unavailable cross-file import is a dependency gap; label any authorised local equivalent and retain its provenance.

Build editable frames, text and auto layout with linked components and semantic variables. Preserve typography, spacing, hierarchy, density, surfaces, imagery and controls. Use realistic content. Screen captures serve as references, never substitutes for editable screens.

Keep construction scripts and a compact file/page/node/variable ledger with affected IDs and decisions. Use the current tool's supported JavaScript input and retry contract. Scoped reads avoid response-size limits; font loads precede text edits. Check persisted geometry after instance overrides or swaps because nested changes may be ignored.

Use discrete assets from supported transfers. Image hashes can be file-local: verify the rendered fill after transfer. Preserve crop transforms, avoid baked-in badges from rendered photo containers, and keep temporary URLs/credentials out of durable evidence.

## Cover behaviour and responsive states

Design the relevant phone and desktop layouts, including narrow-width stress cases. Select states from the actual brief: open menus/sheets, selection, empty/no results, loading, validation, failure/retry, dirty/saving/saved and restricted states as applicable.

Specify destinations, dismissal, action outcomes and recovery. Wire useful prototype paths where supported. Report stored reactions separately from interactions exercised in the player. Do not infer data ownership or save/publication semantics from a static mockup.

Inspect contrast, focus visibility, labels, reading order, targets and long content. Distinguish measured findings from implementation requirements and unverified accessibility behaviour.

## Inspect, revise and hand off

Render every deliverable at readable scale. Inspect clipping, overlaps, wrapping, crop, whitespace, icons and action hierarchy against the approved reference. Independently inspect component linkage, auto layout, variable bindings and actual resolved sizes.

Repair visible defects and retain before/after evidence with changed IDs. Preserve approved originals and shared history; point to superseding designs rather than silently replacing them. Exercise a main path and meaningful edge case when prototype playback is available.

Deliver a DRAFT tied to the exact reviewed file, nodes and screenshots. Use the [handoff checklist](references/handoff.md), including responsive rules, tokens/components, behaviour, fallbacks, dependencies, residuals and approval status. For audits, use ACCEPT / FIX with precise node, token, copy and evidence.

Apply the active project's approval gate before engineering. A frame label, merged code or passing checks does not establish design acceptance. Own design, inspection and handoff; keep application-code changes, implementation PRs, publishing, deployment, subscriptions and external messages outside this role.
