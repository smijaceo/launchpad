"""LaunchBrief schema, vendored from gapfinder (`gapfinder/schemas.py`).

Copied verbatim (classes Sourced … Concept, LaunchBrief) so launchpad can validate imported
briefs without installing gapfinder. When gapfinder bumps `brief_version`, re-copy and record
the gapfinder commit below. Source commit: 3901267f54ed (brief schema unchanged since 3788cea).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Url = Field(pattern=r"^https?://\S+$")


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Sourced(Strict):
    claim: str
    url: str = Url


class Feature(Strict):
    feature: str
    why: str


class Competitor(Strict):
    name: str
    url: str = Url
    how_we_differ: str


class Comparable(Strict):
    vendor: str
    price: str
    source: str = Url


class Buyer(Strict):
    role: str
    company_profile: str


class Problem(Strict):
    summary: str
    evidence: list[Sourced] = Field(min_length=3, max_length=8)


class WhyNow(Strict):
    summary: str
    sources: list[str] = Field(min_length=1)


class Mvp(Strict):
    features: list[Feature] = Field(min_length=3, max_length=7)
    out_of_scope: list[str] = Field(min_length=1)


class Build(Strict):
    team: str
    months_to_mvp: int = Field(ge=1, le=36)
    hardest_parts: list[str] = Field(min_length=2, max_length=5)


class Pricing(Strict):
    model: str
    entry_price: str
    rationale: str
    comparables: list[Comparable] = Field(min_length=2, max_length=6)


class GoToMarket(Strict):
    first_customers: str
    channel: str
    wedge: str


class RiskiestAssumption(Strict):
    assumption: str
    test: str
    success_signal: str


class Concept(Strict):
    opening_id: str
    slug: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: str
    one_liner: str
    buyer: Buyer
    user: str
    problem: Problem
    why_now: WhyNow
    mvp: Mvp
    competitors: list[Competitor] = Field(min_length=3, max_length=8)
    differentiation: str
    build: Build
    pricing: Pricing
    go_to_market: GoToMarket
    risks: list[str] = Field(min_length=3, max_length=6)
    riskiest_assumption: RiskiestAssumption
    open_questions: list[str] = Field(min_length=1)
    revision_log: list[str] = Field(default_factory=list)  # Phase 4: what changed and why

    @model_validator(mode="after")
    def why_now_sources_are_urls(self):
        bad = [u for u in self.why_now.sources if not u.startswith(("http://", "https://"))]
        if bad:
            raise ValueError(f"why_now.sources must be URLs: {bad}")
        return self


class LaunchBrief(Strict):
    """Everything a downstream launch repo needs about one concept (exported by gapfinder)."""
    brief_version: Literal[1] = 1
    exported_at: str
    gapfinder_commit: str
    opening_id: str
    concept: Concept
    panel: dict                      # verdict, mean, per-lens scores, vs-history position
    open_objections: list[dict]      # fatal + major objections from the final round
    change_my_mind: list[dict]       # what evidence would raise critics' scores
    evidence_signals: list[dict]     # need statements behind the themes (title, url, source)
    flagged_claims: list[dict]       # claims the fact-checker found unsupported: never reuse
    founder: dict                    # config/founder.yaml (summarised, no name)
    status: Literal["unvalidated", "validated", "rejected"] = "unvalidated"

