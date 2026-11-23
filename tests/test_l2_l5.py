import json
import shutil
from datetime import date
from pathlib import Path

import pytest

from launchpad import brand, checks, site, validation
from launchpad.schemas import ValidationResult

ROOT = Path(__file__).resolve().parent.parent
SLUG = "safeguards-desk"


@pytest.fixture
def repo(tmp_path):
    b, v = tmp_path / "briefs", tmp_path / "ventures"
    shutil.copytree(ROOT / "briefs" / SLUG, b / SLUG)
    shutil.copytree(ROOT / "ventures" / SLUG, v / SLUG, ignore=shutil.ignore_patterns("dist"))
    return b, v


# ---------------------------------------------------------------- brand

def test_contrast_known_values():
    assert brand.contrast("#000000", "#FFFFFF") == pytest.approx(21, rel=1e-3)
    assert brand.contrast("#777777", "#FFFFFF") == pytest.approx(4.48, abs=0.01)


def test_palette_passes():
    _, fails = brand.check_palette(ROOT / "ventures" / SLUG / "brand" / "palette.json")
    assert fails == []


# ---------------------------------------------------------------- claims

def test_claims_check_passes_with_only_founder_warnings(repo):
    b, v = repo
    errs, warns = checks.check_claims(SLUG, v, b)
    assert errs == []
    assert all("founder confirmation" in w for w in warns)


def write(v, rel, text):
    p = v / SLUG / "copy" / rel
    p.write_text(p.read_text() + "\n\n" + text + "\n")


def test_unmarked_fact_fails(repo):
    b, v = repo
    write(v, "site/index.md", "Offices pay $2,000 a year for this.")
    assert any("without a claim marker" in e for e in checks.check_claims(SLUG, v, b)[0])


def test_unknown_marker_fails(repo):
    b, v = repo
    write(v, "site/index.md", "It costs $490. <!--c:nope-->")
    assert any("'nope' not in ledger" in e for e in checks.check_claims(SLUG, v, b)[0])


def test_banned_phrase_fails_but_negation_passes(repo):
    b, v = repo
    write(v, "site/faq.md", "No check can guarantee you'll be compliant.")
    assert not any("banned" in e for e in checks.check_claims(SLUG, v, b)[0])
    write(v, "site/faq.md", "Trusted by tax offices nationwide.")
    assert any("banned" in e for e in checks.check_claims(SLUG, v, b)[0])


def test_unused_ledger_entry_fails(repo):
    b, v = repo
    led = v / SLUG / "claims-ledger.jsonl"
    led.write_text(led.read_text() + json.dumps({
        "id": "orphan", "claim": "x", "used_in": ["copy/site/index.md"], "source": "brief:concept",
        "source_kind": "brief"}) + "\n")
    assert any("orphan" in e for e in checks.check_claims(SLUG, v, b)[0])


def test_internal_files_skip_fact_rule(repo):
    b, v = repo
    write(v, "sales/interview-guide.md", "Owners told us they pay $999.")
    assert checks.check_claims(SLUG, v, b)[0] == []


# ---------------------------------------------------------------- site

def test_preview_build(repo, tmp_path):
    b, v = repo
    dist, probs = site.build(SLUG, ventures=v, briefs=b, out=tmp_path / "dist")
    home = (dist / "index.html").read_text()
    assert 'name="robots" content="noindex' in home and "Preview build" in home
    assert "<!--c:" not in home and 'class="skip-link" href="#main"' in home
    assert "maximum-scale" not in home and "transition:all" not in (dist / "styles.css").read_text()
    assert any("booking_url" in p for p in probs)
    for p in ("check", "faq", "pricing", "msp", "about"):
        assert (dist / p / "index.html").exists()


def test_release_build_blocked_until_resolved(repo, tmp_path):
    b, v = repo
    with pytest.raises(ValueError, match="release blocked"):
        site.build(SLUG, release=True, ventures=v, briefs=b, out=tmp_path / "dist")


# ---------------------------------------------------------------- validation

def row(**kw):
    base = {"id": "x", "contact_type": "owner", "channel": "email", "date": "2026-12-01",
            "response": "interviewed", "signal_reached": False}
    return ValidationResult.model_validate({**base, **kw})


def test_score_signal():
    rows = [row(id=f"p{i}", response="paid", paid_usd=490, signal_reached=True) for i in range(3)]
    rows += [row(id=f"o{i}", above_5000=True, has_annual_test=False, would_pay=i < 4) for i in range(10)]
    s = validation.score(rows)
    assert s["revenue_part_met"] and s["owner_part_met"] and s["signal_met"]
    s2 = validation.score(rows[:2] + rows[3:])
    assert not s2["revenue_part_met"] and not s2["signal_met"]


def test_loi_counts_only_with_10_offices():
    s = validation.score([row(contact_type="msp", response="loi_signed", loi_offices=9, signal_reached=True)])
    assert s["msp_lois_10plus"] == 0


def test_weekly_review_and_feedback(repo):
    b, v = repo
    text = validation.weekly_review(SLUG, v, b, today=date(2026, 12, 7))
    assert "NOT MET" in text
    with pytest.raises(ValueError, match="isn't met"):
        validation.feedback(SLUG, "validated", v, b)
    out = validation.feedback(SLUG, "in_progress", v, b)
    assert out["status"] == "in_progress" and "@" not in json.dumps(out)
