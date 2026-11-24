# Roadmap

**Goal:** take one gapfinder concept at a time from an unvalidated brief to a real business:
first a launch-quality *validation* that runs the brief's riskiest-assumption test, then a full
launch only if the success signal is met.

**Founder / PM:** repository owner. **Implementer:** Claude Code sessions.
**Current venture:** `safeguards-desk` (D2). **Current phase:** L3–L5 prepared; waiting on the founder's checklist ([FOUNDER-CHECKLIST.md](FOUNDER-CHECKLIST.md)) before release and outreach.

## Rules for changing this plan

1. This file is the source of truth. A phase starts only when the founder approves the previous
   phase's gate; approvals are recorded in [DECISIONS.md](DECISIONS.md).
2. Changing scope, order or gates needs the founder's approval and a DECISIONS entry.
3. Status changes are committed with the work they report.
4. `python -m pytest` passes before every commit.

Status values: `not started` · `in progress` · `awaiting approval` · `done` · `blocked (reason)`

---

## L0 — Setup · `done`

| Deliverable | Status |
|---|---|
| Package `launchpad` (schemas, checks, CLI), `pyproject.toml`, `.gitignore` | done |
| `CLAUDE.md` with the handoff's guardrails; ROADMAP; DECISIONS | done |
| Schemas: vendored `LaunchBrief`, `ImportRecord`, `Positioning`, `ClaimsLedgerEntry`, `ValidationResult` | done |
| `import-brief` / `check-brief` (byte copy, sha256, source commit) | done |
| `safeguards-desk` brief imported and validated | done |
| Tests (`pytest`, no network) | done |
| Cloud environment `launchpad` (personal) with a setup script that installs the package | done (script unproven until a fresh session) |

**Exit:** `pytest` passes; brief imported and validated. ✅

Notes: the first session started on the Default environment. The founder approved a personal
`launchpad` environment (D5) whose setup script runs `pip install -e '.[dev]'` in the repo. It
allows package registries only, with no extra hosts; add hosts when a phase actually needs them.

## L1 — Positioning · `done` (D6)

From the brief only: ideal customer, top three pains with evidence URLs, alternatives
(including do-nothing and DIY), one-sentence value proposition, offer and price, and an answer
to every open objection. Agent: `positioning-strategist` ([rubric](rubrics/positioning.md)).

| Deliverable | Status |
|---|---|
| `ventures/safeguards-desk/positioning.json` (schema `Positioning`) | done |
| `positioning-check` passes: all 28 objections answered, sources in brief, no flagged claims | done |
| `positioning.md` rendered for review | done |
| Founder decisions on the open questions in positioning.md | done: defaults adopted (D6) |

**Exit:** positioning approved by the founder; every claim traceable to the brief.

## L2 — Brand · `awaiting founder` (D7)

| Deliverable | Status |
|---|---|
| 18 name candidates, shortlist of 4, live .com checks | done (`brand/names.json`) |
| Logo: 3 directions, wordmark, icon, favicon, avatar, light and dark (hand-drawn SVG, no spend) | done |
| Palette with WCAG AA check (`palette-check`), typography, voice guide | done |
| Trademark search, domain purchase, handle check | founder |


Names (10–20 candidates incl. Shopify `generate-business-names`; shortlist 3–5; domains via
`generate-domain-names`; **founder buys the domain** and runs the trademark search), logo
(Higgsfield `generate_image`, cost estimate first, founder chooses free allowance vs credits;
3 directions × 2 variants → wordmark, icon, favicon, avatar, light/dark), WCAG-AA palette checked
by script, Google Fonts pairing, voice guide for a tax-office owner.
Agents: brand-namer, logo-designer, brand-critic.
**Exit:** founder picks name, logo, palette; domain registered by the founder.

## L3 — Copy · `in progress`

| Deliverable | Status |
|---|---|
| 8 site pages, one-pager, owner/MSP emails, LinkedIn notes | done |
| Interview guide, proposal/SOW, testing authorisation, report template | done (legal drafts) |
| Claims ledger + `claims-check` (markers, sources, flagged claims, banned phrases) | done: 0 errors, 3 founder confirmations pending |
| Primary sources verified (16 CFR 314.2/314.4/314.6, IRS IR-2026-92) | done (`sources/primary-excerpts.md`) |
| Independent reviews: claims-checker, buyer-reader (simulated), Vercel guidelines | running / applying fixes |


Homepage, offer page, pricing, About (confirmed founder credentials), FAQ, privacy/terms
templates (flagged for legal review), one-pager, outreach emails/LinkedIn, interview guide,
proposal/SOW and test-authorisation templates. Claims-checker (adversarial) against
`claims-ledger.jsonl`; buyer-reader simulated panel (labelled simulated).
**Exit:** zero unsupported claims; founder approves copy.

## L4 — Website · `in progress`

Option B chosen (static site in this repo). Rebuilt on Next.js with 21st.dev components (D10); copy still comes from the claim-checked Markdown. Preview builds carry `noindex` and a banner; `--release` refuses while anything in the founder checklist is open.

| Deliverable | Status |
|---|---|
| Static build, OG image, favicon, sitemap, robots, 404 | done |
| Playwright QA, phone + desktop, light + dark (`qa/site-qa.js`) | done: 36 page views pass |
| Lighthouse ≥ 90 (`qa/lighthouse.sh`, release-like build, compressed) | done: perf 94–98, a11y 100, best practices 100, SEO 100 |
| 21st.dev component redesign (D10) | done |
| Taste-skill design pass | blocked (permission system) |
| Mobbin reference review | waiting for the founder to connect Mobbin |
| Live on the founder's domain | founder |


Founder chooses A) Higgsfield `create_website` (plain `website` type, `deploy_website`, never
`publish_website`) or B) static site in this repo (e.g. Astro on Cloudflare/GitHub Pages).
Mobile-first, WCAG AA, SEO, OG image, privacy-friendly analytics, one CTA tied to the success
signal, booking and payment links (founder creates the accounts). Playwright screenshots +
Lighthouse. **Exit:** live on the founder's domain; Lighthouse ≥ 90 perf/a11y/SEO; approval.

## L5 — Validation · `ready to start` (after the founder checklist)

Kit: `ventures/safeguards-desk/validation/README.md` (target-list method, outreach rules), `ValidationResult` schema with D6 tags, `weekly-review` and `feedback` commands.


Run the brief's test exactly. Target list from public business sources within their terms;
Gmail drafts only, founder sends; interviews logged; `validation/results.jsonl`
(`ValidationResult`) and a weekly review against the success signal. Feed the outcome back to
gapfinder. **Exit:** signal met → L6, or a documented "no" → next brief.

## L6 — Full launch · `not started`

Only after validation: expanded site, case study (written client permission), collateral,
sustainable content calendar, MSP partner programme, onboarding and delivery playbooks. Paid
channels only with an approved budget.

---

## Brief queue

| Brief | Verdict | Founder fit | Status here |
|---|---|---|---|
| `safeguards-desk` | PROMISING (5.62) | 7 | imported, L1 |
| `agent-hardening-sprint` | PROMISING (5.75) | 6 | next if safeguards-desk returns "no" |
| `quietwin` | WEAK (5.5) | 7 | not recommended without new evidence |
