"""Cross-file checks that a schema alone can't express."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .brief_schema import LaunchBrief
from .briefs import BRIEFS, brief_urls, load_brief
from .schemas import Positioning, load_json

ROOT = Path(__file__).resolve().parent.parent
VENTURES = ROOT / "ventures"

# Phrases public-facing text must never contain (CLAUDE.md "Truthful marketing").
BANNED = [
    r"\bFTC[- ](approved|certified|endorsed)\b",
    r"\bguarantee[sd]?\b.{0,30}\bcompli",
    r"\b(100%|fully) compliant\b",
    r"\btrusted by\b",
    r"\btestimonial",
    r"\bcertified (by|compliant)\b",
    r"\bas seen (in|on)\b",
]
MONEY = re.compile(r"(?:[$€£]|EUR\s?|USD\s?)\s?\d[\d,.]*k?", re.I)


def banned_phrases(text: str) -> list[str]:
    return [m.group(0) for p in BANNED for m in re.finditer(p, text, re.I)]


def flagged_hits(text: str, brief: LaunchBrief) -> list[str]:
    """Flagged claims (or their distinctive figures) reused in `text`."""
    hits = []
    low = text.lower()
    for f in brief.flagged_claims:
        claim = f.get("claim", "")
        if claim and claim.lower() in low:
            hits.append(claim)
        brief_text = json.dumps(brief.concept.model_dump()).lower()
        for tok in MONEY.findall(claim):
            # a figure only counts if it is unique to the flagged claim, not elsewhere in the brief
            if tok.lower() in low and tok.lower() not in brief_text:
                hits.append(f"{tok} (from flagged claim: {claim[:60]}…)")
    return hits


def resolve_brief_path(brief: LaunchBrief, ref: str) -> bool:
    """`brief:concept.pricing.entry_price` or `brief:open_objections[3]` exists in the brief."""
    node = json.loads(brief.model_dump_json())
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", ref.removeprefix("brief:")):
        try:
            node = node[int(part[1:-1])] if part.startswith("[") else node[part]
        except (KeyError, IndexError, TypeError, ValueError):
            return False
    return True


def check_positioning(slug: str, ventures: Path = VENTURES, briefs: Path = BRIEFS) -> list[str]:
    """Return a list of problems (empty = ok)."""
    brief, rec = load_brief(slug, briefs)
    pos = load_json(ventures / slug / "positioning.json", Positioning)
    errs: list[str] = []

    if pos.slug != slug:
        errs.append(f"slug {pos.slug!r} != {slug!r}")
    if pos.brief_sha256 != rec.sha256:
        errs.append("brief_sha256 does not match the imported brief")

    # every open objection answered, lens matches
    n = len(brief.open_objections)
    got = {o.index: o for o in pos.objections}
    missing = sorted(set(range(n)) - set(got))
    extra = sorted(set(got) - set(range(n)))
    if missing:
        errs.append(f"objections not answered: {missing}")
    if extra:
        errs.append(f"objection indices not in brief: {extra}")
    for i, o in got.items():
        if i < n and o.lens != brief.open_objections[i].get("lens"):
            errs.append(f"objection {i}: lens {o.lens!r} != brief {brief.open_objections[i].get('lens')!r}")

    # the test is the brief's test, word for word
    ra = brief.concept.riskiest_assumption
    for field in ("assumption", "test", "success_signal"):
        if getattr(pos.test, field) != getattr(ra, field):
            errs.append(f"test.{field} differs from brief.concept.riskiest_assumption.{field}")

    # sources come from the brief
    urls = brief_urls(brief)
    cited = [(f"pains[{i}]", p.source_url) for i, p in enumerate(pos.pains)]
    cited += [(f"alternatives[{i}]", a.source_url) for i, a in enumerate(pos.alternatives)
              if a.source_url]
    cited += [(f"claims[{i}]", c.source) for i, c in enumerate(pos.claims)]
    for where, src in cited:
        if src.startswith("brief:"):
            if not resolve_brief_path(brief, src):
                errs.append(f"{where}: {src} does not exist in the brief")
        elif src not in urls:
            errs.append(f"{where}: source not in brief: {src}")

    # no flagged claims anywhere; no banned marketing phrases in buyer-facing parts
    text = pos.model_dump_json()
    errs += [f"reuses flagged claim: {h}" for h in flagged_hits(text, brief)]
    facing = " ".join([pos.value_proposition] + [o.model_dump_json() for o in pos.offers])
    errs += [f"banned phrase in value proposition/offers: {h!r}" for h in banned_phrases(facing)]
    return errs


def render_positioning(slug: str, ventures: Path = VENTURES, briefs: Path = BRIEFS) -> str:
    """Human-readable positioning.md, generated from positioning.json."""
    brief, _ = load_brief(slug, briefs)
    p = load_json(ventures / slug / "positioning.json", Positioning)
    L = [f"# Positioning: {brief.concept.name}",
         "",
         f"> Generated from `positioning.json` by `python -m launchpad render-positioning {slug}`. "
         "Edit the JSON, not this file.",
         f"> Brief status: **{brief.status}**. Panel: {brief.panel.get('decision')} "
         f"({brief.panel.get('mean')}). Nothing here is validated by real buyers yet.",
         "",
         "## Value proposition", "", p.value_proposition, "",
         "## Ideal customer", "", p.ideal_customer, "",
         "**Qualifies if:**", *[f"- {q}" for q in p.qualifiers], "",
         "**Not a fit if:**", *[f"- {q}" for q in p.disqualifiers], "",
         "## Top three pains", ""]
    for i, x in enumerate(p.pains, 1):
        L += [f"{i}. **{x.pain}**",
              f"   - Source wording (as summarised in the brief): {x.words} "
              f"([source]({x.source_url}), {x.source_kind.replace('_', ' ')})"]
        if x.note:
            L.append(f"   - Note: {x.note}")
    L += ["", "## Current alternatives", "", "| Alternative | Kind | What the buyer gets | Our answer |",
          "|---|---|---|---|"]
    for a in p.alternatives:
        name = f"[{a.name}]({a.source_url})" if a.source_url else a.name
        L.append(f"| {name} | {a.kind.replace('_', ' ')} | {a.what_buyer_gets} | {a.our_answer} |")
    L += ["", "## Offer", ""]
    for o in p.offers:
        L += [f"### {o.name} — {o.price}", "", f"For: {o.for_whom}", "", "Includes:",
              *[f"- {d}" for d in o.deliverables], "", "Not included:",
              *[f"- {d}" for d in o.not_included], "", "Before work starts:",
              *[f"- {d}" for d in o.prerequisites], "", f"Call to action: **{o.call_to_action}**", ""]
    L += ["## Validation test (from the brief, unchanged)", "",
          f"- **Assumption:** {p.test.assumption}", f"- **Test:** {p.test.test}",
          f"- **Success signal:** {p.test.success_signal}", "",
          "## Answers to the panel's open objections", "",
          "Status: *answered* · *offer changed* · *test will tell* (we don't know yet) · "
          "*accepted risk*.", "", "| # | Lens | Status | Answer |", "|---|---|---|---|"]
    for o in sorted(p.objections, key=lambda o: o.index):
        L.append(f"| {o.index} | {o.lens} | {o.status.replace('_', ' ')} | {o.answer} |")
    L += ["", "## Claims and sources", ""]
    L += [f"- {c.claim} — {c.source if c.source.startswith('brief:') else f'<{c.source}>'}"
          for c in p.claims]
    if p.decisions_for_founder:
        L += ["", "## Decisions for the founder", "",
              *[f"{i}. {d}" for i, d in enumerate(p.decisions_for_founder, 1)]]
    return "\n".join(L) + "\n"
