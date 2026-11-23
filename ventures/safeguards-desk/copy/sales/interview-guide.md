---
title: Owner and MSP interview guide
contentType: How-to
internal: true
use: every scoping or discovery call during the L5 test; log answers in validation/results.jsonl
---

# Interview guide

The calls test the brief's riskiest assumption: that offices above 5,000 consumers, or MSPs on their behalf, will pay for verified configuration and testing on top of the WISP and insurance they already have. Ask about the past and the present, never "would you buy". Don't pitch until the last five minutes, and only if asked.

## Before the call

Record in the results row: contact type, channel, how you found them (`source`), and whether they came from your own network (`network: own` or `cold`).

## Owner questions (20 minutes)

Ask these in order, writing down their words:

1. Roughly how many clients' or borrowers' records do you keep, counting past years you still hold?
2. Who looks after your computers and Microsoft 365: you, a staff member, an IT person or an MSP?
3. Do you pay anyone for monitoring or endpoint protection? Which provider?
4. Do you have a written information security plan? Where did it come from, and when was it last updated?
5. Has anyone (insurer, examiner, bank, client, auditor) ever asked you for proof that your systems were tested? What did you send?
6. When you renewed cyber insurance, which security questions were on the form?
7. Has your office ever had a vulnerability scan or a penetration test? When, by whom, what did it cost?
8. What's the last security problem you dealt with (phishing, a hacked mailbox, a lost laptop)? What did it cost you?
9. If you needed a test done, which budget would it come from?
10. Who else would need to agree before you spent $490 on this? <!--c:price-490-->

Close: "Would it be useful if I sent the details of the check?" Record whether they ask to book or pay without prompting.

## MSP questions (20 minutes)

1. How many of your clients are tax, accounting or mortgage offices, and roughly what size?
2. Have any of them asked about the Safeguards Rule or about testing? What did they ask for?
3. Which tools do you run for those clients: scanning, penetration testing, compliance or GRC, Microsoft 365 baselines?
4. What do those tools not give you for Safeguards clients?
5. How would you feel about a third party's report on a client tenant you manage?
6. What would you need to resell a testing check: price, branding, terms?
7. Would a letter of intent covering about 10 offices be realistic? What would stop it?

## After the call

Within the hour, add a row to `validation/results.jsonl` with their words in `quote` (only with permission) and tag `signal_reached` only for: a paid check, a signed letter of intent, or an owner above 5,000 consumers who has no annual test or assessment **and** says they would pay to have one.
