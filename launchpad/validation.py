"""L5: score validation results against the brief's success signal, and write feedback for gapfinder.

safeguards-desk success signal (brief, verbatim): "At least 3 paid $490 checks or 1 MSP letter of
intent covering 10+ client offices, and at least 4 of 10 owners above 5,000 consumers saying they
have no annual test or vulnerability assessment and would pay to have one."
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

from .briefs import BRIEFS, load_brief
from .checks import VENTURES
from .schemas import ValidationResult, load_jsonl


def load_results(slug: str, ventures: Path = VENTURES) -> list[ValidationResult]:
    path = ventures / slug / "validation" / "results.jsonl"
    return load_jsonl(path, ValidationResult) if path.exists() and path.read_text().strip() else []


def score(rows: list[ValidationResult]) -> dict:
    """Signal components for the safeguards-desk test."""
    paid = [r for r in rows if r.response == "paid" and r.paid_usd > 0]
    lois = [r for r in rows if r.response == "loi_signed" and r.loi_offices >= 10]
    owners = [r for r in rows if r.contact_type in ("owner", "office_manager")
              and r.response == "interviewed"]
    above = [r for r in owners if r.above_5000]
    yes = [r for r in above if r.has_annual_test is False and r.would_pay]
    revenue_ok = len(paid) >= 3 or len(lois) >= 1
    owners_ok = len(owners) >= 10 and len(yes) >= 4
    return {
        "contacts": len(rows),
        "by_response": dict(Counter(r.response for r in rows)),
        "paid_checks": len(paid),
        "paid_checks_cold": sum(1 for r in paid if r.network != "own"),
        "paid_with_msp_or_mdr": sum(1 for r in paid if r.has_msp_or_mdr),
        "msp_lois_10plus": len(lois),
        "owner_interviews": len(owners),
        "owners_above_5000": len(above),
        "owners_above_5000_no_test_would_pay": len(yes),
        "revenue_part_met": revenue_ok,
        "owner_part_met": owners_ok,
        "signal_met": revenue_ok and owners_ok,
    }


def weekly_review(slug: str, ventures: Path = VENTURES, briefs: Path = BRIEFS,
                  today: date | None = None) -> str:
    brief, _ = load_brief(slug, briefs)
    rows = load_results(slug, ventures)
    s = score(rows)
    today = today or date.today()
    ra = brief.concept.riskiest_assumption
    tick = lambda ok: "met" if ok else "not yet"
    lines = [
        f"# Weekly review: {brief.concept.name}, {today.isoformat()}", "",
        f"Success signal (from the brief): {ra.success_signal}", "",
        "| Measure | Count | Needed |", "|---|---|---|",
        f"| Paid $490 checks | {s['paid_checks']} (cold: {s['paid_checks_cold']}, with MSP/MDR: {s['paid_with_msp_or_mdr']}) | 3, or 1 LOI |",
        f"| MSP letters of intent for 10+ offices | {s['msp_lois_10plus']} | 1, or 3 paid checks |",
        f"| Owner interviews | {s['owner_interviews']} | 10 |",
        f"| Owners above 5,000 consumers | {s['owners_above_5000']} | — |",
        f"| …with no annual test and would pay | {s['owners_above_5000_no_test_would_pay']} | 4 of 10 |",
        "",
        f"- Revenue part: **{tick(s['revenue_part_met'])}**",
        f"- Owner part: **{tick(s['owner_part_met'])}**",
        f"- **Success signal: {'MET' if s['signal_met'] else 'NOT MET'}**", "",
        f"Contacts logged: {s['contacts']}. Responses: {s['by_response'] or 'none yet'}.", "",
        "## Quotes this week", "",
    ]
    quotes = [r for r in rows if r.quote]
    lines += [f"- ({r.contact_type}, {r.date}) “{r.quote}”" for r in quotes[-10:]] or ["- none yet"]
    lines += ["", "## Decision", "",
              "Continue / stop / change the test? Changing the test needs a DECISIONS entry. "
              "The two-week window ends 14 days after the first outreach email is sent."]
    return "\n".join(lines) + "\n"


def feedback(slug: str, outcome: str, ventures: Path = VENTURES, briefs: Path = BRIEFS) -> dict:
    """Summary for gapfinder (PM copies validation/gapfinder-feedback.json across)."""
    if outcome not in ("validated", "rejected", "in_progress"):
        raise ValueError("outcome must be validated, rejected or in_progress")
    brief, rec = load_brief(slug, briefs)
    rows = load_results(slug, ventures)
    s = score(rows)
    if outcome == "validated" and not s["signal_met"]:
        raise ValueError("can't mark validated: the success signal isn't met")
    out = {
        "opening_id": brief.opening_id, "slug": slug,
        "brief_gapfinder_commit": rec.brief_gapfinder_commit,
        "status": outcome, "as_of": date.today().isoformat(),
        "test": brief.concept.riskiest_assumption.model_dump(),
        "score": s,
        "quotes": [{"contact_type": r.contact_type, "date": r.date.isoformat(), "quote": r.quote}
                   for r in rows if r.quote],
        "note": "Real buyer evidence from launchpad L5. Contact details are not included.",
    }
    path = ventures / slug / "validation" / "gapfinder-feedback.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    return out
