# Founder checklist

Things only you can do: the agent prepares, you act (CLAUDE.md guardrails). Tick them off here or in DECISIONS.md.

## Before the site goes live

- [ ] Run a USPTO trademark search for "Countersign" (classes 42 and 45); record the result in DECISIONS (D7)
- [ ] Buy `countersignsecurity.com` (it was available on 2026-11-23; any registrar) and check the LinkedIn, X and GitHub handles in `ventures/safeguards-desk/brand/names.json`
- [ ] Confirm, or correct, the three founder facts in `ventures/safeguards-desk/claims-ledger.jsonl` (`founder-creds`, `founder-skills`, `founder-solo`) and set their status to `supported`
- [ ] Create a free Cal.com event (20-minute scoping call) and a business email on the domain; put both in `ventures/safeguards-desk/site/site.json`
- [ ] Choose hosting: Cloudflare Pages or GitHub Pages (both free); Vercel only on a paid plan for commercial use (D8)
- [ ] Have a lawyer review `copy/site/privacy.md` and `terms.md`, then remove `legal_draft: true`
- [ ] Run `python -m launchpad build-site safeguards-desk --release`; it must pass before you deploy

## Before the first paid check (D6 hard gate)

- [ ] Form the business entity
- [ ] Have a lawyer review `copy/sales/proposal-sow.md` and `copy/sales/testing-authorisation.md`, including the liability cap
- [ ] Get an E&O/cyber insurance quote for a solo security tester; decide on cover
- [ ] Create a Stripe Payment Link for $490 and add it to `site.json` (`payment_url`)
- [ ] Produce the sample report against your own Microsoft 365 test tenant, labelled "Sample"

## During the test

- [ ] Build the target lists by hand (`ventures/safeguards-desk/validation/README.md`)
- [ ] Review and send each outreach draft yourself; log every contact in `validation/results.jsonl`
- [ ] Run `python -m launchpad weekly-review safeguards-desk` each Friday
