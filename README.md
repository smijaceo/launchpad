# launchpad

Turns startup concepts exported by [gapfinder](https://github.com/smijaceo/cybersecurity) into
real businesses, validation first: positioning → brand → copy → website → a real test with real
buyers → full launch only if the test's success signal is met.

- Working rules and guardrails: [CLAUDE.md](CLAUDE.md)
- Plan and status: [docs/ROADMAP.md](docs/ROADMAP.md) · decisions: [docs/DECISIONS.md](docs/DECISIONS.md)
- Current venture: [`ventures/safeguards-desk/positioning.md`](ventures/safeguards-desk/positioning.md)

```bash
pip install -e '.[dev]'
python -m launchpad --help
python -m launchpad import-brief <slug> --gapfinder ../cybersecurity   # copy + checksum a brief
python -m launchpad check-brief safeguards-desk
python -m launchpad positioning-check safeguards-desk
python -m pytest
```

Layout: `briefs/<slug>/` (imported, never edited) · `ventures/<slug>/` (derived work) ·
`launchpad/` (schemas, checks, CLI) · `docs/rubrics/` + `.claude/agents/` (one per agent step).
