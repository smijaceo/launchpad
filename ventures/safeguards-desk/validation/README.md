# L5 validation playbook: safeguards-desk

This folder runs the brief's two-week test and records the outcome. The test and its success signal are fixed by the brief (see `../positioning.md`); changing either needs a DECISIONS entry.

## Day 0: before the first email

Complete these before any outreach goes out:

- Domain bought, site released (`python -m launchpad build-site safeguards-desk --release` passes)
- Booking link (Cal.com free tier) and contact email live; Stripe Payment Link for $490 created
- Founder facts confirmed in the claims ledger (status `supported`, `checked_by: founder`)
- Postal address for the CAN-SPAM footer (a PO box or registered-agent address works)
- Calls can start now; **no paid check is delivered** until the D6 hard gate is cleared (engagement letter, authorisation, liability cap, entity, insurance quote)

## Building the target lists

Each list is built by hand from public business sources, used within their terms. Never scrape a site whose terms forbid it, and never buy lists.

| List | Size | Where to look (manually) | Record per row |
|---|---|---|---|
| MSPs serving accounting or mortgage firms | 15 | MSP websites that name accounting, CPA, tax or mortgage clients (web search); local chamber of commerce member directories; state CPA society vendor or sponsor pages | company, owner name, business email or contact page, source URL, why they fit |
| Mortgage brokers | 20 | State regulator licence lookups and NMLS Consumer Access (use for confirming licence status only, per its terms); broker websites for contact details | business name, contact name, business email, licence state, source URL |
| Established tax and CPA offices (5 to 20 staff) | 20 | Firm websites (staff pages show size and years in business); state CPA society "find a CPA" directories within their terms; IRS directory of preparers with credentials (contact only via the firm's own site) | business name, contact name, business email, staff count estimate, source URL |

Rows go into `private/targets.csv` (git-ignored; template below). Business contacts only, minimal fields, deleted on request.

```csv
id,list,business,contact_name,role,business_email,source_url,fit_note,network,status
```

## Running outreach

- Agents prepare Gmail drafts from `copy/outreach/`; **the founder reviews, edits and sends every one**. Never more than 10 a day.
- Log every contact as a row in `results.jsonl` (schema `ValidationResult`) the day it happens, including no-replies after 5 business days.
- Tag `network` (own/cold/referral) and `has_msp_or_mdr` on every row (D6).
- Calls follow `copy/sales/interview-guide.md`.

## Reviewing the test

Run `python -m launchpad weekly-review safeguards-desk` every Friday; it writes `weekly-review.md` against the signal. At day 14:

- Signal met: `python -m launchpad feedback safeguards-desk validated`, record the decision, move to L6.
- Not met: `python -m launchpad feedback safeguards-desk rejected`, record what was learned, and the PM copies `gapfinder-feedback.json` to gapfinder. A fast, documented "no" is a good outcome.
