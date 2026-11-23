"""Import gapfinder launch briefs into briefs/<slug>/ (never edited after import)."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .schemas import ImportRecord, LaunchBrief, load_json

ROOT = Path(__file__).resolve().parent.parent
BRIEFS = ROOT / "briefs"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(repo: Path, *args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                              check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def import_brief(gapfinder_repo: Path, slug: str, source_repo: str, briefs_dir: Path = BRIEFS,
                 force: bool = False) -> ImportRecord:
    src = gapfinder_repo / "exports" / slug / "brief.json"
    brief = load_json(src, LaunchBrief)          # refuse invalid briefs
    if brief.concept.slug != slug:
        raise ValueError(f"brief slug {brief.concept.slug!r} != {slug!r}")
    dest_dir = briefs_dir / slug
    dest = dest_dir / "brief.json"
    if dest.exists() and not force:
        raise FileExistsError(f"{dest} exists; briefs are not overwritten (use --force for a "
                              "new gapfinder export, and record why in DECISIONS.md)")
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)                   # byte-for-byte copy
    rec = ImportRecord(
        slug=slug, source_repo=source_repo,
        source_path=str(src.relative_to(gapfinder_repo)),
        source_head=_git(gapfinder_repo, "rev-parse", "HEAD") or "unknown",
        brief_gapfinder_commit=brief.gapfinder_commit,
        sha256=sha256(dest),
        imported_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    (dest_dir / "import.json").write_text(rec.model_dump_json(indent=2) + "\n")
    return rec


def load_brief(slug: str, briefs_dir: Path = BRIEFS) -> tuple[LaunchBrief, ImportRecord]:
    """Load and verify an imported brief: schema-valid and unchanged since import."""
    d = briefs_dir / slug
    brief = load_json(d / "brief.json", LaunchBrief)
    rec = load_json(d / "import.json", ImportRecord)
    if sha256(d / "brief.json") != rec.sha256:
        raise ValueError(f"briefs/{slug}/brief.json changed since import (sha256 mismatch); "
                         "briefs must not be edited")
    return brief, rec


def brief_urls(brief: LaunchBrief) -> set[str]:
    """Every URL string anywhere in the brief."""
    urls: set[str] = set()

    def walk(x):
        if isinstance(x, str):
            # whole-field URLs and URLs embedded in text, e.g. "https://a ; concept:mvp"
            for tok in x.split():
                if tok.startswith(("http://", "https://")):
                    urls.add(tok.rstrip(".,;)"))
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(json.loads(brief.model_dump_json()))
    return urls
