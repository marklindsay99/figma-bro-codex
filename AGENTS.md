# Agent instructions

This repository packages a reusable Figma designer for Codex.

- Keep the designer independent of any customer, repository, brand, approver or private Figma file. Project decisions belong in the active project's optional design profile.
- Keep installation explicit and reversible. Preserve existing files, refuse silent replacement, and test update/uninstall recovery and duplicate detection.
- Use Python 3.9+ standard library for management code; introduce dependencies only for a demonstrated need.
- Run `python3 -m unittest discover -s tests -v` and `python3 scripts/check_package.py` after changes. Check the staged diff before committing.
- Reference official Figma tooling and skills as dependencies; do not vendor their instructions, connector code, fonts or imagery.
- Keep credentials, private examples, export archives and source project history out of every commit. Public release requires the owner's explicit visibility instruction and license decision.
