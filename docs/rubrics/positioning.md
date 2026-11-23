# Positioning rubric (L1)

Used by the `positioning-strategist` agent. Input: `briefs/<slug>/brief.json` and its
`import.json`. Output: `ventures/<slug>/positioning.json` (schema `launchpad.schemas.Positioning`),
then `positioning.md` rendered from it. Validate with `python -m launchpad positioning-check <slug>`.

The goal is a position the validation test can prove wrong quickly, not a pitch.

## Grounding rules (checked by code)

- Every `source_url` and `claims[].source` must be a URL that appears in the brief, or a
  `brief:<json path>` that exists (e.g. `brief:concept.pricing.entry_price`).
- Nothing from `flagged_claims`, including their figures.
- `test` is copied word for word from `concept.riskiest_assumption`. L1 does not change the test;
  propose changes under `decisions_for_founder`.
- Every entry in `open_objections` gets exactly one answer, with the same `lens`.
- No banned marketing phrases in the value proposition or offers (see `checks.BANNED`).

## Fields

- `ideal_customer`: one paragraph a person can use to say yes/no to a prospect.
- `qualifiers` / `disqualifiers`: questions or facts that put a prospect in or out (e.g. the
  5,000-consumer line, owns its M365 tenant).
- `pains`: exactly three, ranked. `words` is the closest wording in the source. `source_kind`
  says honestly whose words they are: `named_buyer` only if the source is the buyer named in the
  brief; `proxy_buyer` for similar small firms; `regulation` for a legal duty; `market` for
  vendor or pricing evidence. If no named-buyer evidence exists, say so in `note`.
- `alternatives`: at least do-nothing and DIY, plus the free option and the closest paid
  competitors and bundles from the brief. `our_answer` may honestly say "stay with this".
- `value_proposition`: one sentence, ≤ 35 words, in the buyer's language (an office owner,
  not a CISO). No promise of compliance.
- `offers`: the offer the test sells first (price from the brief), with what is and isn't
  included and the prerequisites (signed scope and authorisation, third-party consent).
- `objections[]`: `status` is
  - `answered`: the brief or the offer already handles it; say how.
  - `offer_changed`: this positioning changes scope, wording or price to handle it (list the
    change in `decisions_for_founder` if it needs approval).
  - `test_will_tell`: only buyer evidence settles it; name the interview question or test
    metric that will.
  - `accepted_risk`: real and not fixable now; say what would trigger a rethink.
  Don't argue an objection away; most at this stage are honestly `test_will_tell`.
- `claims`: every factual statement used above that a buyer could check, with its source.
- `decisions_for_founder`: choices the founder must make before L2.

## Quality bar (reviewed by the founder)

- Would a tax-office owner understand the value proposition in one read?
- Does the offer match the brief's test exactly enough that results are comparable?
- Is anything stated more confidently than the evidence allows?
