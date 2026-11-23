"""launchpad command line: `python -m launchpad --help`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import briefs, checks
from .schemas import SchemaError


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="launchpad", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    imp = sub.add_parser("import-brief", help="copy exports/<slug>/brief.json from a gapfinder checkout")
    imp.add_argument("slug")
    imp.add_argument("--gapfinder", type=Path, required=True, help="path to the gapfinder checkout")
    imp.add_argument("--source-repo", default="smijaceo/cybersecurity")
    imp.add_argument("--force", action="store_true", help="replace an existing import")

    cb = sub.add_parser("check-brief", help="validate an imported brief and its checksum")
    cb.add_argument("slug")

    pc = sub.add_parser("positioning-check", help="validate ventures/<slug>/positioning.json")
    pc.add_argument("slug")

    rp = sub.add_parser("render-positioning", help="write ventures/<slug>/positioning.md")
    rp.add_argument("slug")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "import-brief":
            rec = briefs.import_brief(a.gapfinder, a.slug, a.source_repo, force=a.force)
            print(f"imported briefs/{rec.slug}/brief.json (gapfinder export {rec.brief_gapfinder_commit[:12]}, "
                  f"sha256 {rec.sha256[:12]})")
        elif a.cmd == "check-brief":
            b, rec = briefs.load_brief(a.slug)
            print(f"ok: {b.concept.name}, status {b.status}, {len(b.open_objections)} open objections, "
                  f"{len(b.flagged_claims)} flagged claims")
        elif a.cmd == "positioning-check":
            errs = checks.check_positioning(a.slug)
            if errs:
                print("\n".join(f"FAIL {e}" for e in errs))
                return 1
            print("ok")
        elif a.cmd == "render-positioning":
            out = checks.VENTURES / a.slug / "positioning.md"
            out.write_text(checks.render_positioning(a.slug))
            print(f"wrote {out.relative_to(checks.ROOT)}")
    except (SchemaError, ValueError, FileExistsError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
