# Decision log

Scope, brand and spend decisions, with the founder's approval. New entries are appended;
superseded ones are marked, not deleted. "Proposed" entries wait for the founder.

| ID | Date | Decision | Why | Approved |
|---|---|---|---|---|
| D1 | 2026-11-23 | **Follow gapfinder's handoff** (`docs/HANDOFF-launch-repo.md` at gapfinder `3901267`): phases L0–L6, validation before full launch, guardrails in CLAUDE.md. | Founder's starter prompt. | Founder (starter prompt) |
| D2 | 2026-11-23 | **First venture: `safeguards-desk`.** | Recommended order in the handoff: best founder fit (7/10) and its test can earn revenue. Founder named it in the starter prompt. | Founder (starter prompt) |
| D3 | 2026-11-23 | **Vendor gapfinder's `LaunchBrief` schema** (`launchpad/brief_schema.py`) instead of installing gapfinder as a dependency. Briefs are byte copies with a sha256 and source commit in `import.json`. | gapfinder pulls in heavy ML dependencies; the brief schema is small and versioned (`brief_version`). | Implementer (L0 detail) |
| D4 | 2026-11-23 | **Raw contact lists are git-ignored** (`ventures/*/validation/private/`); only aggregated results with sources are committed. | Privacy: business contacts minimal and deletable; a git history can't forget. | Proposed |
