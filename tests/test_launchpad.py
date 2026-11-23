import json
import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError

from launchpad import briefs, checks
from launchpad.cli import main
from launchpad.schemas import (ClaimsLedgerEntry, LaunchBrief, SchemaError, ValidationResult,
                               load_json, load_jsonl)

ROOT = Path(__file__).resolve().parent.parent
SLUG = "safeguards-desk"


@pytest.fixture
def repo(tmp_path):
    """A throwaway copy of briefs/ and ventures/ for the venture under test."""
    b, v = tmp_path / "briefs", tmp_path / "ventures"
    shutil.copytree(ROOT / "briefs" / SLUG, b / SLUG)
    shutil.copytree(ROOT / "ventures" / SLUG, v / SLUG)
    return b, v


def edit_positioning(v, fn):
    p = v / SLUG / "positioning.json"
    data = json.loads(p.read_text())
    fn(data)
    p.write_text(json.dumps(data))


# ---------------------------------------------------------------- briefs

def test_imported_brief_is_valid_and_unchanged():
    brief, rec = briefs.load_brief(SLUG)
    assert brief.concept.slug == SLUG
    assert rec.brief_gapfinder_commit == brief.gapfinder_commit
    assert brief.status == "unvalidated"


def test_import_copies_bytes_and_refuses_overwrite(tmp_path):
    gap = tmp_path / "gapfinder"
    (gap / "exports" / SLUG).mkdir(parents=True)
    shutil.copyfile(ROOT / "briefs" / SLUG / "brief.json", gap / "exports" / SLUG / "brief.json")
    out = tmp_path / "briefs"
    rec = briefs.import_brief(gap, SLUG, "owner/gapfinder", briefs_dir=out)
    assert (out / SLUG / "brief.json").read_bytes() == (gap / "exports" / SLUG / "brief.json").read_bytes()
    assert rec.source_head == "unknown"          # not a git repo
    with pytest.raises(FileExistsError):
        briefs.import_brief(gap, SLUG, "owner/gapfinder", briefs_dir=out)


def test_import_rejects_invalid_brief(tmp_path):
    gap = tmp_path / "gapfinder"
    (gap / "exports" / SLUG).mkdir(parents=True)
    (gap / "exports" / SLUG / "brief.json").write_text('{"brief_version": 1}')
    with pytest.raises(SchemaError):
        briefs.import_brief(gap, SLUG, "x/y", briefs_dir=tmp_path / "out")


def test_edited_brief_is_detected(repo):
    b, _ = repo
    p = b / SLUG / "brief.json"
    p.write_text(p.read_text().replace("unvalidated", "validated", 1))
    with pytest.raises(ValueError, match="changed since import"):
        briefs.load_brief(SLUG, b)


def test_brief_urls_splits_embedded_urls():
    brief = load_json(ROOT / "briefs" / SLUG / "brief.json", LaunchBrief)
    urls = briefs.brief_urls(brief)
    assert "https://www.sbtpg.com/all-in-one-cybersecurity/" in urls
    assert not any(" " in u or ";" in u for u in urls)


# ---------------------------------------------------------------- positioning

def test_positioning_passes(repo):
    assert checks.check_positioning(SLUG, *reversed(repo)) == []


def test_missing_objection_fails(repo):
    _, v = repo
    edit_positioning(v, lambda d: d["objections"].pop())
    assert any("not answered" in e for e in checks.check_positioning(SLUG, v, repo[0]))


def test_wrong_lens_fails(repo):
    _, v = repo
    edit_positioning(v, lambda d: d["objections"][0].update(lens="founder-fit"))
    assert any("lens" in e for e in checks.check_positioning(SLUG, v, repo[0]))


def test_changed_test_fails(repo):
    _, v = repo
    edit_positioning(v, lambda d: d["test"].update(success_signal="1 paid check"))
    assert any("success_signal" in e for e in checks.check_positioning(SLUG, v, repo[0]))


def test_source_outside_brief_fails(repo):
    _, v = repo
    edit_positioning(v, lambda d: d["claims"].append({"claim": "x", "source": "https://example.com/"}))
    edit_positioning(v, lambda d: d["claims"].append({"claim": "y", "source": "brief:concept.nope"}))
    errs = checks.check_positioning(SLUG, v, repo[0])
    assert any("example.com" in e for e in errs)
    assert any("brief:concept.nope" in e for e in errs)


def test_flagged_claim_figure_fails(repo):
    _, v = repo
    edit_positioning(v, lambda d: d["claims"].append(
        {"claim": "Vanta Essentials costs $14,000", "source": "brief:concept.pricing"}))
    assert any("flagged" in e for e in checks.check_positioning(SLUG, v, repo[0]))


def test_banned_phrase_fails(repo):
    _, v = repo
    edit_positioning(v, lambda d: d.update(value_proposition="FTC-approved testing, trusted by 50 firms."))
    errs = checks.check_positioning(SLUG, v, repo[0])
    assert sum("banned phrase" in e for e in errs) == 2


def test_banned_phrases():
    assert checks.banned_phrases("We guarantee you'll be compliant")
    assert checks.banned_phrases("100% compliant")
    assert not checks.banned_phrases("Not legal advice; no promise of compliance.")


def test_rendered_markdown_is_current():
    assert (ROOT / "ventures" / SLUG / "positioning.md").read_text() == checks.render_positioning(SLUG)


# ---------------------------------------------------------------- other schemas

def test_validation_result_rules(tmp_path):
    ok = {"id": "r1", "contact_type": "owner", "channel": "email", "date": "2026-12-01",
          "response": "paid", "signal_reached": True}
    ValidationResult.model_validate(ok)
    with pytest.raises(ValidationError):
        ValidationResult.model_validate({**ok, "response": "no_reply"})
    p = tmp_path / "results.jsonl"
    p.write_text(json.dumps(ok) + "\n\n" + json.dumps({**ok, "channel": "fax"}) + "\n")
    with pytest.raises(SchemaError, match="line 3"):
        load_jsonl(p, ValidationResult)


def test_claims_ledger_entry():
    ClaimsLedgerEntry.model_validate({"id": "c1", "claim": "x", "used_in": ["copy/site/home.md"],
                                      "source": "brief:concept", "source_kind": "brief"})


# ---------------------------------------------------------------- CLI

def test_cli(capsys):
    assert main(["check-brief", SLUG]) == 0
    assert main(["positioning-check", SLUG]) == 0
    assert main(["check-brief", "no-such-brief"]) == 1
