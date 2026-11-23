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

    pal = sub.add_parser("palette-check", help="WCAG contrast check of ventures/<slug>/brand/palette.json")
    pal.add_argument("slug")

    cc = sub.add_parser("claims-check", help="check copy against ventures/<slug>/claims-ledger.jsonl")
    cc.add_argument("slug")
    cc.add_argument("--release", action="store_true", help="warnings (e.g. unconfirmed founder facts) fail too")

    cs = sub.add_parser("claims-sync", help="update used_in in the claims ledger from copy markers")
    cs.add_argument("slug")

    bs = sub.add_parser("build-site", help="build ventures/<slug>/site/dist (preview unless --release)")
    bs.add_argument("slug")
    bs.add_argument("--release", action="store_true", help="refuse to build while anything blocks publishing")
    bs.add_argument("--qa-out", type=Path, help="build a release-like copy here for Lighthouse only (never deploy it)")

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
        elif a.cmd == "palette-check":
            from .brand import check_palette
            lines, fails = check_palette(checks.VENTURES / a.slug / "brand" / "palette.json")
            print("\n".join(lines))
            if fails:
                return 1
        elif a.cmd == "claims-check":
            errs, warns = checks.check_claims(a.slug)
            print("\n".join([f"FAIL {e}" for e in errs] + [f"WARN {w}" for w in warns]) or "ok")
            if errs or (a.release and warns):
                return 1
            if not errs:
                print(f"ok ({len(warns)} warnings)")
        elif a.cmd == "claims-sync":
            print("\n".join(checks.sync_ledger_usage(a.slug)) or "no changes")
        elif a.cmd == "build-site":
            from . import site
            dist, probs = site.build(a.slug, release=a.release, out=a.qa_out, qa=bool(a.qa_out))
            print(f"built {dist} ({'release' if a.release else 'qa' if a.qa_out else 'preview'})")
            if probs and not a.release:
                print(f"{len(probs)} item(s) block a release build:")
                print("\n".join(f"  - {p}" for p in probs))
    except (SchemaError, ValueError, FileExistsError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
