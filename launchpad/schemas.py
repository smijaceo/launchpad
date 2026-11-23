"""Schemas for launchpad's structured outputs (pydantic).

Every agent step writes JSON or JSON Lines that validates against a model here. Cross-file
checks (e.g. "every URL comes from the brief") live in `launchpad/checks.py`.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .brief_schema import LaunchBrief  # noqa: F401  (re-export)

Url = Field(pattern=r"^https?://\S+$")
Slug = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ---------------------------------------------------------------- L0 import

class ImportRecord(Strict):
    """Written next to an imported brief: where it came from and its exact bytes."""
    slug: str = Slug
    source_repo: str                 # e.g. smijaceo/cybersecurity
    source_path: str                 # e.g. exports/safeguards-desk/brief.json
    source_head: str                 # gapfinder HEAD when imported (the brief records its own export commit)
    brief_gapfinder_commit: str      # copied from brief.gapfinder_commit
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    imported_at: str


# ---------------------------------------------------------------- L1 positioning

class Pain(Strict):
    pain: str                        # the pain, stated plainly
    words: str                       # closest wording from the source; not shown as a verbatim quote
    source_url: str = Url            # must appear in the brief
    source_kind: Literal["named_buyer", "proxy_buyer", "regulation", "market"]
    note: str = ""                   # e.g. why a proxy source stands in for the named buyer


class Alternative(Strict):
    name: str
    kind: Literal["do_nothing", "diy", "free", "competitor", "bundle", "partner"]
    what_buyer_gets: str
    our_answer: str                  # why switch, or honestly why they shouldn't
    source_url: str | None = None


class Offer(Strict):
    name: str
    price: str
    for_whom: str
    deliverables: list[str] = Field(min_length=1)
    not_included: list[str] = Field(min_length=1)
    prerequisites: list[str] = Field(min_length=1)   # e.g. signed scope and authorisation
    call_to_action: str


class ObjectionAnswer(Strict):
    index: int = Field(ge=0)         # position in brief.open_objections
    lens: str
    status: Literal["answered", "offer_changed", "test_will_tell", "accepted_risk"]
    answer: str


class Claim(Strict):
    claim: str
    source: str                      # a URL that appears in the brief, or "brief:<json path>"


class TestPlan(Strict):
    assumption: str
    test: str
    success_signal: str


class Positioning(Strict):
    slug: str = Slug
    brief_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    ideal_customer: str
    qualifiers: list[str] = Field(min_length=2)       # questions that put a prospect in or out
    disqualifiers: list[str] = Field(min_length=1)
    pains: list[Pain] = Field(min_length=3, max_length=3)
    alternatives: list[Alternative] = Field(min_length=3)
    value_proposition: str
    offers: list[Offer] = Field(min_length=1)
    objections: list[ObjectionAnswer]
    claims: list[Claim] = Field(min_length=1)
    test: TestPlan
    decisions_for_founder: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def shape(self):
        kinds = {a.kind for a in self.alternatives}
        missing = {"do_nothing", "diy"} - kinds
        if missing:
            raise ValueError(f"alternatives must include {sorted(missing)}")
        if len(self.value_proposition.split()) > 35:
            raise ValueError("value_proposition must be 35 words or fewer")
        idx = [o.index for o in self.objections]
        if len(idx) != len(set(idx)):
            raise ValueError("each objection index may be answered once")
        return self


# ---------------------------------------------------------------- L3 claims ledger

class ClaimsLedgerEntry(Strict):
    """One public factual claim → its source. File: ventures/<slug>/claims-ledger.jsonl."""
    id: str
    claim: str
    used_in: list[str] = Field(min_length=1)          # file paths where the claim appears
    source: str                                        # URL or "brief:<json path>"
    source_kind: Literal["brief", "primary", "founder"]  # founder = founder-confirmed fact
    status: Literal["supported", "needs_confirmation", "unsupported", "flagged"] = "supported"
    checked_by: str = ""                               # agent or person who checked it
    note: str = ""


# ---------------------------------------------------------------- L5 validation

class ValidationResult(Strict):
    """One outreach or interview outcome. File: ventures/<slug>/validation/results.jsonl."""
    id: str
    contact_type: Literal["owner", "office_manager", "msp", "insurer", "association", "other"]
    channel: Literal["email", "linkedin", "phone", "referral", "event", "other"]
    date: date
    response: Literal["no_reply", "declined", "replied", "call_booked", "interviewed",
                      "paid", "loi_signed"]
    signal_reached: bool             # did this contact count toward the success signal?
    quote: str = ""                  # their words, with permission to record
    follow_up: str = ""
    source: str = ""                 # where the contact came from (directory URL etc.)
    network: Literal["own", "cold", "referral", "unknown"] = "unknown"   # D6 tag
    has_msp_or_mdr: bool | None = None                                     # D6 tag
    above_5000: bool | None = None   # owner says they hold data on 5,000+ consumers
    has_annual_test: bool | None = None  # has an annual pen test or 6-monthly vuln assessment
    would_pay: bool | None = None    # says they'd pay to have the test done
    paid_usd: int = 0                # money actually received
    loi_offices: int = 0             # offices covered by a signed MSP letter of intent

    @model_validator(mode="after")
    def signal_needs_outcome(self):
        if self.signal_reached and self.response in {"no_reply", "declined"}:
            raise ValueError("signal_reached requires a positive response")
        return self


# ---------------------------------------------------------------- helpers

M = TypeVar("M", bound=BaseModel)


class SchemaError(ValueError):
    pass


def _fmt(exc: ValidationError) -> str:
    first = exc.errors()[0]
    loc = ".".join(str(p) for p in first["loc"])
    return f"{loc}: {first['msg']}" if loc else first["msg"]


def load_json(path: str | Path, model: type[M]) -> M:
    try:
        return model.model_validate_json(Path(path).read_text())
    except ValidationError as exc:
        raise SchemaError(f"{Path(path).name}: {_fmt(exc)}") from None


def load_jsonl(path: str | Path, model: type[M]) -> list[M]:
    rows = []
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(model.model_validate_json(line))
        except ValidationError as exc:
            raise SchemaError(f"{Path(path).name} line {n}: {_fmt(exc)}") from None
    return rows


# ---------------------------------------------------------------- L3 reviews

class ClaimReview(Strict):
    """claims-checker output, one JSON line per ledger entry (adversarial, opens sources)."""
    claim_id: str
    verdict: Literal["supported", "overstated", "unsupported", "not_checkable"]
    source_opened: str                # URL or brief path actually read
    evidence: str                     # short quote from the source, or why it can't be checked
    copy_issue: str = ""              # where the copy says more than the ledger/source
    fix: str = ""


class ReaderReport(Strict):
    """buyer-reader output, one JSON line per persona × page. Always simulated."""
    simulated: Literal[True] = True
    persona: str
    page: str
    understood: str                   # what they think is offered, in their words
    would_act: Literal["yes", "maybe", "no"]
    next_action: str
    objections: list[str] = Field(default_factory=list)
    confusing: list[str] = Field(default_factory=list)
    trust_signals_missing: list[str] = Field(default_factory=list)
