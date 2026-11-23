"""Static site generator: ventures/<slug>/copy/site/*.md → ventures/<slug>/site/dist/.

No JavaScript is shipped. Markup and CSS follow Vercel's Web Interface Guidelines
(vercel-labs/agent-skills `web-design-guidelines`, pinned snapshot sha256 d246b026…):
skip link, visible :focus-visible rings, sentence-wrapped headings with text-wrap: balance,
scroll-margin on anchors, color-scheme + theme-color, preloaded self-hosted fonts with
font-display: swap, tabular numbers in tables, explicit image dimensions, no zoom blocking,
no `transition: all`, reduced-motion respected, brand name marked translate="no".
"""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import markdown

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


# ---------------------------------------------------------------- rendering

def _icon_svg(brand_dir: Path) -> str:
    svg = (brand_dir / "logo" / "icon.svg").read_text()
    svg = re.sub(r'role="img" aria-label="[^"]*"', 'aria-hidden="true" focusable="false"', svg)
    svg = svg.replace('stroke="#1D3F6E"', 'stroke="currentColor"').replace('stroke="#0E6B57"',
                                                                            'stroke="var(--accent)"')
    return svg.replace("<svg ", '<svg width="36" height="36" class="logo-icon" ', 1)


def _css(pal: dict) -> str:
    def tokens(mode: str) -> str:
        return "".join(f"--{k.replace('_', '-')}:{v};" for k, v in pal[mode].items())
    return CSS_TEMPLATE.replace("/*LIGHT*/", tokens("light")).replace("/*DARK*/", tokens("dark"))


def _render_md(text: str, cfg: dict) -> str:
    text = re.sub(r"\s*<!--.*?-->", "", text, flags=re.S)          # claim markers
    text = text.replace("{{booking_url}}", html.escape(cfg.get("booking_url") or "/check/", quote=True))
    email = cfg.get("contact_email")
    text = text.replace("{{contact_email}}", f'<a href="mailto:{html.escape(email, quote=True)}">{html.escape(email)}</a>'
                        if email else "the contact address on this site (to come)")
    text = text.replace("{{analytics_sentence}}", _analytics_sentence(cfg))
    md = markdown.Markdown(extensions=["tables", "smarty", "attr_list", "toc"],
                           extension_configs={"toc": {"permalink": False}})
    out = md.convert(text)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out.replace("Countersign Security", '<span translate="no">Countersign&nbsp;Security</span>')


def _curly(page: str) -> str:
    """Curly apostrophes in text the Markdown smarty extension doesn't reach (raw HTML, template)."""
    parts = re.split(r"(<[^>]+>|<style.*?</style>)", page, flags=re.S)
    return "".join(x if x.startswith("<") else re.sub(r"(?<=\w)'(?=\w)", "’", x) for x in parts)


def _analytics_sentence(cfg: dict) -> str:
    prov = (cfg.get("analytics") or {}).get("provider", "none")
    if prov == "cloudflare":
        return ("We use Cloudflare Web Analytics, which counts page views without cookies "
                "and without tracking you across sites.")
    return "This site sets no cookies and runs no analytics or tracking scripts."


def _analytics_tag(cfg: dict) -> str:
    a = cfg.get("analytics") or {}
    if a.get("provider") == "cloudflare" and a.get("token"):
        tok = html.escape(json.dumps({"token": a["token"]}), quote=True)
        return ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
                f'data-cf-beacon="{tok}"></script>')
    return ""


def render_page(page: Page, pages: list[Page], cfg: dict, icon: str, preview: bool) -> str:
    base = cfg["base_url"].rstrip("/")
    order = cfg.get("nav_order") or [p.path for p in pages]
    by_path = {p.path: p for p in pages}
    nav = "".join(
        f'<li><a href="{p}"{" aria-current=\"page\"" if p == page.path else ""}>{html.escape(by_path[p].meta["nav"])}</a></li>'
        for p in order if p in by_path)
    foot = "".join(f'<li><a href="{p.path}">{html.escape(p.meta["nav"])}</a></li>'
                   for p in pages if p.meta.get("footer_only"))
    title = page.meta["title"]
    full_title = f"{cfg['name']}: {title}" if page.path != "/" else f"{cfg['name']}: {title}"
    desc = html.escape(page.meta["description"], quote=True)
    banner = ('<div class="preview-banner" role="note">Preview build: not published, '
              'founder confirmation and legal review pending.</div>') if preview else ""
    robots = '<meta name="robots" content="noindex,nofollow">' if preview else ""
    body = _render_md(page.body_md, cfg)
    return _curly(PAGE_TEMPLATE.format(
        title=html.escape(full_title), desc=desc, canonical=f"{base}{page.path}",
        og_image=f"{base}/og.png", robots=robots, banner=banner, icon=icon,
        name=html.escape(cfg["name"]), nav=nav, body=body, foot=foot,
        hero=" hero" if page.meta.get("hero") else "", analytics=_analytics_tag(cfg),
        site_name=html.escape(cfg["name"], quote=True),
    ))


def build(slug: str, release: bool = False, ventures: Path = VENTURES, briefs: Path = BRIEFS,
          out: Path | None = None, qa: bool = False) -> tuple[Path, list[str]]:
    """qa=True renders like a release (indexable, no banner) for audits only; never deploy it."""
    vdir = ventures / slug
    cfg = json.loads((vdir / "site" / "site.json").read_text())
    pages = load_pages(slug, ventures)
    probs = release_problems(slug, cfg, pages, ventures, briefs)
    errs, _ = checks.check_claims(slug, ventures, briefs)
    if errs:
        raise ValueError("claims check fails:\n" + "\n".join(errs))
    if release and probs:
        raise ValueError("release blocked:\n" + "\n".join(probs))
    dist = out or vdir / "site" / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    shutil.copytree(vdir / "site" / "static", dist)
    brand = vdir / "brand"
    shutil.copyfile(brand / "logo" / "favicon.svg", dist / "favicon.svg")
    pal = json.loads((brand / "palette.json").read_text())
    (dist / "styles.css").write_text(_css(pal))
    icon = _icon_svg(brand)
    preview = not (release or qa)
    for p in pages:
        dest = dist / p.out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render_page(p, pages, cfg, icon, preview))
    notfound = Page(Path("404.md"), {"title": "Page not found", "description": "Page not found.",
                                     "path": "/404/", "nav": ""},
                    "# Page not found\n\nThe page you asked for doesn't exist. Go to the [home page](/).")
    (dist / "404.html").write_text(render_page(notfound, pages, cfg, icon, preview))
    base = cfg["base_url"].rstrip("/")
    urls = "".join(f"<url><loc>{base}{p.path}</loc></url>" for p in pages)
    (dist / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (dist / "robots.txt").write_text("User-agent: *\n" + ("Disallow: /\n" if preview else
                                     f"Allow: /\nSitemap: {base}/sitemap.xml\n"))
    return dist, probs


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#FAF8F4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1620" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/source-serif-4-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to Main Content</a>
{banner}
<header class="site-header">
<div class="wrap header-inner">
<a class="brand" href="/" aria-label="{site_name} home">{icon}<span class="brand-name" translate="no">{name}</span></a>
<nav aria-label="Main"><ul>{nav}</ul></nav>
</div>
</header>
<main id="main" class="wrap{hero}" tabindex="-1">
{body}
</main>
<footer class="site-footer">
<div class="wrap">
<p>General information, not legal advice. <span translate="no">{name}</span> isn't affiliated with the Federal Trade Commission or the Internal Revenue Service.</p>
<ul class="footer-links">{foot}</ul>
</div>
</footer>
{analytics}
</body>
</html>
"""

CSS_TEMPLATE = """@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/source-serif-4-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:700;font-display:swap;src:url(/fonts/source-serif-4-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/inter-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/inter-latin-600-normal.woff2) format("woff2")}
:root{/*LIGHT*/color-scheme:light dark;--serif:"Source Serif 4",Georgia,"Times New Roman",serif;--sans:Inter,system-ui,"Segoe UI",Arial,sans-serif;--focus:var(--primary)}
@media (prefers-color-scheme:dark){:root{/*DARK*/}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
@media (pointer:fine){html{overscroll-behavior:none}}
a{touch-action:manipulation}
body{margin:0;background:var(--bg);color:var(--text);font:400 1.0625rem/1.6 var(--sans);-webkit-tap-highlight-color:transparent;overflow-wrap:break-word}
@media (min-width:48rem){body{font-size:1.125rem}}
.wrap{max-width:68rem;margin:0 auto;padding:0 max(1rem,env(safe-area-inset-left)) 0 max(1rem,env(safe-area-inset-right))}
main:focus{outline:none}
main{padding-top:2rem;padding-bottom:4rem}
main>*{max-width:42rem}
main>.table-wrap{max-width:none}
h1,h2,h3{scroll-margin-top:1rem;font-family:var(--serif);color:var(--text);line-height:1.2;text-wrap:balance;}
@media (min-width:48rem){h1,h2,h3{scroll-margin-top:5.5rem}html{scroll-padding-top:5.5rem}}
h1{font-size:clamp(2rem,1.4rem + 2.6vw,3rem);font-weight:700;margin:.4em 0 .5em}
h2{font-size:clamp(1.45rem,1.2rem + 1vw,1.85rem);font-weight:600;margin:2.2em 0 .5em}
h3{font-size:1.2rem;font-weight:600;margin:1.8em 0 .4em}
p,li{text-wrap:pretty}
a{color:var(--primary);text-underline-offset:.18em;text-decoration-thickness:1px;transition:color .15s ease,text-decoration-thickness .15s ease}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:4px}
.skip-link{position:absolute;left:1rem;top:-3rem;z-index:20;background:var(--primary);color:var(--primary-text);padding:.6rem 1rem;border-radius:6px;font-weight:600;transition:transform .15s ease}
.skip-link:focus-visible{transform:translateY(4rem)}
.preview-banner{background:var(--warn);color:var(--bg);text-align:center;font-size:.9rem;padding:.4rem 1rem;font-weight:600}
.site-header{background:var(--bg);border-bottom:1px solid var(--border)}
@media (min-width:48rem){.site-header{position:sticky;top:0;z-index:10}}
.header-inner{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.5rem 1.5rem;padding-top:.75rem;padding-bottom:.75rem}
.brand:hover .brand-name{text-decoration:underline;text-decoration-thickness:2px}
.brand{display:inline-flex;align-items:center;gap:.6rem;color:var(--primary);text-decoration:none;min-width:0}
.brand-name{font-family:var(--serif);font-weight:700;font-size:1.25rem;color:var(--text)}
.logo-icon{flex:none;color:var(--primary)}
nav ul{display:flex;flex-wrap:wrap;gap:.25rem .9rem;list-style:none;margin:0;padding:0}
nav a{display:inline-block;padding:.35rem .1rem;color:var(--muted);text-decoration:none;font-weight:600;font-size:.95rem;touch-action:manipulation}
nav a:hover,nav a[aria-current=page]{color:var(--text);text-decoration:underline;text-decoration-thickness:2px}
.status{display:inline-block;margin:0;padding:.25rem .7rem;border:1px solid var(--accent);color:var(--accent);border-radius:999px;font-size:.85rem;font-weight:600}
.hero h1{max-width:44rem}
.cta-row{display:flex;flex-wrap:wrap;gap:.75rem;margin:1.5rem 0}
.button{display:inline-flex;align-items:center;justify-content:center;min-height:2.9rem;padding:.65rem 1.25rem;border-radius:8px;border:2px solid var(--primary);color:var(--primary);background:transparent;font-weight:600;text-decoration:none;touch-action:manipulation;transition:background-color .15s ease,color .15s ease,border-color .15s ease}
.button:hover{background:var(--primary);color:var(--primary-text);text-decoration:none}
.button.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-text)}
.button.primary:hover{background:var(--primary);border-color:var(--primary);color:var(--primary-text)}
.table-wrap{overflow-x:auto;margin:1.25rem 0;border:1px solid var(--border);border-radius:8px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:.97rem}
th,td{text-align:left;vertical-align:top;padding:.7rem .9rem;border-bottom:1px solid var(--border)}
tr:last-child td{border-bottom:none}
th{font-weight:600;background:var(--bg)}
ul,ol{padding-left:1.3rem}
li{margin:.35rem 0}
.fineprint{font-size:.9rem;color:var(--muted);margin-top:3rem}
.draft{border-left:4px solid var(--warn);padding:.5rem .9rem;color:var(--warn);font-weight:600;background:var(--surface)}
.site-footer{border-top:1px solid var(--border);color:var(--muted);font-size:.92rem;padding:1.5rem 0 calc(1.5rem + env(safe-area-inset-bottom))}
.footer-links{display:flex;gap:1rem;list-style:none;padding:0;margin:.5rem 0 0}
.footer-links a{color:var(--muted)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
"""
