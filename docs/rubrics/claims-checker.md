# Claims-checker rubric (L3, adversarial)

Input: `ventures/<slug>/claims-ledger.jsonl`, the copy under `ventures/<slug>/copy/`, `briefs/<slug>/brief.json`, `ventures/<slug>/sources/primary-excerpts.md`.
Output: `ventures/<slug>/reviews/claims-review.jsonl`, one `ClaimReview` per ledger entry. Validate with `python -m launchpad review-check claims <path>`.

Your job is to find where the copy says more than the evidence. Assume every claim is wrong until you've read the source yourself.

- Open every `primary` source URL yourself (`curl -sL`; eCFR, IRS and FTC hosts are allowed). Don't trust the excerpts file; compare it with the live page.
- For `brief:` sources, read that path in the brief.
- `founder` claims: verdict `not_checkable`; note that founder confirmation is pending.
- Read every sentence that carries the claim's marker. If the sentence says more than the source (wider scope, stronger verb, missing condition such as "absent effective continuous monitoring"), verdict `overstated` and say exactly where.
- Also report, as extra rows with `claim_id: "unmarked:<file>:<line>"`, any factual statement in public copy with no marker, and anything implying certification, guarantees, FTC/IRS affiliation, existing clients or a track record.
- `fix` gives replacement wording, not advice.
