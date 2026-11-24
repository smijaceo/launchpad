"""Site build: the Next.js app in ventures/<slug>/site/web renders ventures/<slug>/copy/site/*.md.

The copy stays the single source of public text and is claim-checked before every build.
Components come from 21st.dev (shadcn/ui based, adapted; see site/web/components/site/).
Preview builds are noindex with a banner; release builds refuse while anything in
`release_problems` is open (founder facts, contact links, legal drafts, claims).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from . import checks
from .briefs import BRIEFS

VENTURES = checks.VENTURES


@dataclass
class Page:
    src: Path
    meta: dict
    body_md: str

    @property
    def path(self) -> str:
        return self.meta["path"]

    @property
    def out(self) -> str:
        return "index.html" if self.path == "/" else self.path.strip("/") + "/index.html"


def load_pages(slug: str, ventures: Path = VENTURES) -> list[Page]:
    pages = []
    for f in sorted((ventures / slug / "copy" / "site").glob("*.md")):
        meta, body = checks.strip_front_matter(f.read_text())
        for key in ("title", "description", "path", "nav"):
            if key not in meta:
                raise ValueError(f"{f.name}: front matter needs {key!r}")
        pages.append(Page(f, meta, body))
    paths = [p.path for p in pages]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate page paths")
    return pages


def release_problems(slug: str, cfg: dict, pages: list[Page], ventures: Path = VENTURES,
                     briefs: Path = BRIEFS) -> list[str]:
    """Everything that must be resolved before the site may be published."""
    probs = []
    for key in ("booking_url", "contact_email"):
        if not cfg.get(key):
            probs.append(f"site.json: {key} is empty")
    errs, warns = checks.check_claims(slug, ventures, briefs)
    probs += errs + warns
    probs += [f"{p.src.name}: legal draft not yet reviewed" for p in pages if p.meta.get("legal_draft")]
    return probs



def build(slug: str, release: bool = False, ventures: Path = VENTURES, briefs: Path = BRIEFS,
          out: Path | None = None, qa: bool = False) -> tuple[Path, list[str]]:
    """Build the static site. qa=True renders like a release (indexable, no banner) for audits
    only; never deploy a qa build."""
    vdir = ventures / slug
    cfg = json.loads((vdir / "site" / "site.json").read_text())
    pages = load_pages(slug, ventures)
    probs = release_problems(slug, cfg, pages, ventures, briefs)
    errs, _ = checks.check_claims(slug, ventures, briefs)
    if errs:
        raise ValueError("claims check fails:\n" + "\n".join(errs))
    if release and probs:
        raise ValueError("release blocked:\n" + "\n".join(probs))
    web = vdir / "site" / "web"
    if not (web / "node_modules").exists():
        raise ValueError(f"run `npm ci` in {web} first")
    env = {**os.environ, "SITE_MODE": "release" if (release or qa) else "preview"}
    res = subprocess.run(["npx", "next", "build"], cwd=web, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        raise ValueError("next build failed:\n" + (res.stdout + res.stderr)[-3000:])
    dist = out or vdir / "site" / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    shutil.copytree(web / "out", dist)
    return dist, probs


def export_relative(dist: Path, out: Path) -> list[Path]:
    """Copy a built site so it works from any path (e.g. a private Claude artifact preview):
    root-relative links become relative, Next.js's `_next/` folder becomes `assets/` (hosts may
    reserve names starting with "_"), CSS font URLs become relative, and the chunk loader derives
    its base URL from its own script URL. Returns the files to publish."""
    import re
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(dist, out, ignore=shutil.ignore_patterns("*.txt", "404", "sitemap.xml", "robots.txt"))
    if (out / "_next").exists():
        (out / "_next").rename(out / "assets")
    for page in out.rglob("*.html"):
        up = "../" * (len(page.relative_to(out).parts) - 1)
        text = page.read_text().replace("/_next/static/", "/assets/static/")

        def fix(m: re.Match) -> str:
            target = m.group(2).lstrip("/")
            if not target or target.endswith("/"):
                target += "index.html"
            return f'{m.group(1)}="{up}{target}"'
        text = re.sub(r'\b(href|src)="(/(?!/)[^"#?]*)"', fix, text)
        text = re.sub(r'(?<![.\w/])/assets/static/', f"{up}assets/static/", text)  # inline RSC payload
        text = re.sub(r'<script src="[^"]*polyfills-[^"]*" noModule=""></script>', "", text)  # legacy-only
        if page == out / "index.html":
            text = text.replace("<!DOCTYPE html>", "")
        page.write_text(text)
    for poly in out.rglob("polyfills-*.js"):
        poly.unlink()  # loaded only by browsers without ES modules; the preview host rejects its bytes
    for css in out.rglob("*.css"):
        css.write_text(css.read_text().replace("url(/_next/static/media/", "url(../media/"))
    for js in (out / "assets" / "static" / "chunks").rglob("*.js"):
        t = js.read_text()
        t2 = t.replace('r.p="/_next/"',
                       'r.p=((document.currentScript&&document.currentScript.src.split("assets/static/")[0])||"/")+"assets/"')
        t2 = t2.replace('"/_next/', '"/assets/')
        if t2 != t:
            js.write_text(t2)
    return sorted(p for p in out.rglob("*") if p.is_file())
