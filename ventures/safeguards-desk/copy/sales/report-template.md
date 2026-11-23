---
title: Safeguards testing check report template
contentType: Reference
use: deliverable; the sample report (D6) is produced from the founder's own test tenant and labelled "Sample"
---

# Safeguards testing check report

**Client:** {{client_legal_name}} · **Report date:** {{date}} · **Testing window:** {{window}} · **Prepared by:** Countersign Security

## Summary for the owner

One paragraph in plain language: what was checked, the 3 most important findings, and what to do first.

## What was checked

The check covered these in-scope assets under the signed authorisation dated {{auth_date}}:

- External services: {{assets}}
- Microsoft 365 tenant: {{tenant_domain}} (licence: {{licence}}; checks the licence doesn't support are listed as "not assessed")

## Findings

| # | Finding | Risk | Where | Fix (for your IT person or MSP) |
|---|---|---|---|---|
| 1 | {{finding}} | High / Medium / Low | {{asset}} | {{fix}} |

## Microsoft 365 configuration

| Check | Result |
|---|---|
| Multi-factor authentication on all accounts | {{result}} |
| Accounts with admin roles | {{result}} |
| External mail forwarding and inbox rules | {{result}} |
| Former staff and inactive accounts | {{result}} |
| Security defaults or conditional access | {{result}} |

## Limits of this check

This check is a point-in-time external scan and a read-only configuration review. It isn't a full penetration test, doesn't cover internal systems or workstations, and isn't a determination of compliance with any law. Your attorney can advise how this report fits your Safeguards program.

## Access removed

Read-only access granted on {{grant_date}} was confirmed removed on {{revoke_date}}.
