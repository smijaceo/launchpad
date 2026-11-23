---
title: Proposal and statement of work template
contentType: Reference
status: DRAFT for legal review; not to be sent until a lawyer has reviewed it (CLAUDE.md)
---

# Proposal and statement of work: Safeguards testing check

<p class="draft">Draft template. A lawyer must review the terms, liability cap and insurance wording before first use. [LEGAL REVIEW]</p>

Prepared for {{client_legal_name}} ("Client") by Countersign Security, [LEGAL ENTITY] ("Provider"), on {{date}}.

## Scope of work

Provider will perform the following for a fixed fee of $490 (USD): <!--c:price-490-->

1. **Scoping**: a call and questionnaire recording the Client's consumer count, systems, vendors and asset ownership
2. **External vulnerability scan** of the in-scope assets listed in the Testing Authorisation, from the internet only
3. **Read-only Microsoft 365 configuration review** of tenant {{tenant_domain}} using temporary read-only access the Client grants and revokes
4. **Written report** dated on delivery, listing findings by risk with remediation guidance
5. **Walkthrough call** of up to 30 minutes

## Out of scope

Internal network, workstation, phishing and full penetration testing; remediation; legal advice or any compliance determination; ongoing monitoring; any asset not listed in a signed Testing Authorisation.

## Client responsibilities

The Client signs the Testing Authorisation, obtains written consent from any third party that owns an in-scope asset, grants and later revokes read-only access, and names a contact available during testing.

## Schedule

Testing window: {{start_date}} to {{end_date}}. Report delivered within 5 business days of the window closing.

## Fees and payment

$490 fixed, due {{payment_terms}}. Payment link: {{payment_url}}. <!--c:price-490-->

## Data handling

Provider does not open or read message content; Provider reads mailbox settings, including inbox and forwarding rules, as part of the configuration review, and does not store tax returns, Social Security numbers or loan files. Findings belong to the Client. Provider keeps the report and working notes for {{retention_period}} and deletes them earlier on written request. [LEGAL REVIEW: service provider oversight under 16 CFR 314.4(f)]

## Limitations

The check samples configuration and exposure at a point in time and cannot find every weakness. Provider's total liability is limited to [LEGAL REVIEW: cap]. Provider carries [LEGAL REVIEW: E&O/cyber insurance details].

## Acceptance

Client: ____________________ Name/Title: ____________ Date: ________
Provider: __________________ Name/Title: ____________ Date: ________
