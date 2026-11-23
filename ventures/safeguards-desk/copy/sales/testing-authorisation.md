---
title: Testing authorisation template
contentType: Reference
status: DRAFT for legal review; no scan or test may start until this is signed (CLAUDE.md)
---

# Testing authorisation

<p class="draft">Draft template for legal review. Signed copies are kept with the engagement record. [LEGAL REVIEW]</p>

{{client_legal_name}} ("Client") authorises Countersign Security ("Provider") to perform the activities below, only against the assets listed, only during the window stated.

## Authorised activities

The Client authorises only these activities:

- External vulnerability scanning of the listed internet-facing assets
- Read-only review of Microsoft 365 tenant {{tenant_domain}} through access the Client grants

Not authorised:

- Denial-of-service testing
- Password guessing against live accounts
- Social engineering
- Exploitation beyond confirming a finding
- Changes to any configuration
- Opening or reading message content

## In-scope assets

| Asset (domain, IP address or service) | Owner | Owner consent attached? |
|---|---|---|
| {{asset_1}} | {{owner_1}} | {{yes_or_no}} |

Assets owned by a third party (hosting provider, managed service provider, internet provider) are in scope **only** if that owner's written consent is attached. Microsoft 365 testing follows Microsoft's published rules of engagement.

## Testing window and contacts

Window: {{start_datetime}} to {{end_datetime}} ({{timezone}}). Provider source IP addresses: {{source_ips}}. Client emergency contact: {{name_phone}}. Provider contact: {{founder_name_phone}}. Either party may stop testing at any time by phone.

## Signatures

The person signing confirms they have authority to authorise testing of the Client-owned assets listed.

Client: ____________________ Name/Title: ____________ Date: ________
Provider: __________________ Name/Title: ____________ Date: ________
