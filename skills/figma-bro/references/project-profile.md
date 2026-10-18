# Optional project design profile

The conventional entrypoint is `.figma-bro/design-profile.md` in the active repository. AGENTS.md may explicitly name another path. Read the named profile instead of guessing among unrelated files. An absent optional profile is normal; an explicit broken pointer is missing context to report.

Profiles are ordinary project Markdown. They refine the design brief and remain subject to applicable AGENTS.md and repository authority. They do not grant account access, change permissions or authorise engineering/publishing. Resolve links relative to the profile file; keep private references in the project, outside the shared installation.

Include only decisions needed for that project:

- product scope, actual stack and authoritative requirement/handoff documents;
- brand, approved reference screenshots, typography/tokens/components and relevant source Figma destinations;
- distinctive composition or navigation requirements, responsive and interaction states;
- who approves what, evidence of past approval and unresolved decisions;
- handoff conventions and project-specific capability gaps.

Separate approved references, drafts and suggestions. An explicit task destination controls where to work; a profile's source file is not permission to edit it. If destination or essential product decisions are missing, resolve that dependency while continuing independent research/inspection.

A minimal profile can be:

```markdown
# Design profile
Product: a fictional bicycle-repair appointment portal.
Authority: AGENTS.md and the repository's current requirements.
References: approved screenshots in ../docs/designs/; inspect before drawing.
Brand: reuse the actual project tokens and components; do not invent values.
Responsive: phone appointment booking and desktop staff scheduling.
Approval: the product owner reviews the exact draft before UI engineering.
Destination: supplied in each task; existing source references remain read-only.
Unresolved: reminder delivery is outside this feature.
```

For teams, commit the profile in their own repository. Never add their private Figma URLs or validation captures to the shared designer package.
