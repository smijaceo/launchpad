// Reads the claim-checked Markdown copy (ventures/<slug>/copy/site/*.md) at build time.
// The Markdown stays the single source of public copy: `python -m launchpad claims-check`
// validates it, and these pages only lay it out.
import fs from "node:fs";
import path from "node:path";
import { Marked, type Token, type Tokens } from "marked";
import { markedSmartypants } from "marked-smartypants";

const COPY_DIR = path.resolve(process.cwd(), "../../copy/site");
const SITE_JSON = path.resolve(process.cwd(), "../site.json");

export type SiteConfig = {
  name: string;
  base_url: string;
  booking_url: string;
  contact_email: string;
  nav_order: string[];
};

export const site: SiteConfig = JSON.parse(fs.readFileSync(SITE_JSON, "utf8"));
export const isPreview = process.env.SITE_MODE !== "release";
export const bookingUrl = site.booking_url || "/check/";

const md = new Marked({ gfm: true }).use(markedSmartypants());

/** Remove claim markers and other HTML comments; fill site placeholders. */
function clean(text: string): string {
  return text
    .replace(/\s*<!--[\s\S]*?-->/g, "")
    .replaceAll("{{booking_url}}", bookingUrl)
    .replaceAll(
      "{{contact_email}}",
      site.contact_email ? `[${site.contact_email}](mailto:${site.contact_email})` : "the contact address on this site (to come)",
    )
    .replaceAll("{{analytics_sentence}}", "This site sets no cookies and runs no analytics or tracking scripts.");
}

export type Page = { slug: string; meta: Record<string, string>; body: string };

function parseFile(file: string): Page {
  const raw = fs.readFileSync(path.join(COPY_DIR, file), "utf8");
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  const meta: Record<string, string> = {};
  let body = raw;
  if (m) {
    for (const line of m[1].split("\n")) {
      const i = line.indexOf(":");
      if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
    }
    body = m[2];
  }
  return { slug: file.replace(/\.md$/, ""), meta, body };
}

export function getPage(slug: string): Page {
  return parseFile(`${slug}.md`);
}

export function allPages(): Page[] {
  return fs.readdirSync(COPY_DIR).filter((f) => f.endsWith(".md")).sort().map(parseFile);
}

export const inline = (text: string) => md.parseInline(clean(text)) as string;
export const html = (text: string) => md.parse(clean(text)) as string;

export type Section = { id: string; title: string; raw: string; tokens: Token[] };

/** Split a page body at its H2 headings; `<!--section:id-->` or `<!--plan:id-->` names each. */
export function sections(body: string): { intro: string; sections: Section[] } {
  const parts = body.split(/\n(?=## )/);
  const intro = parts[0].startsWith("## ") ? "" : parts.shift()!;
  return {
    intro,
    sections: parts.map((part) => {
      const [first, ...rest] = part.split("\n");
      const id = part.match(/<!--(?:section|plan):([a-z0-9-]+)-->/)?.[1] ?? "";
      const raw = rest.join("\n");
      return { id, title: first.replace(/^## /, ""), raw, tokens: md.lexer(clean(raw)) };
    }),
  };
}

export const title = (heading: string) => inline(heading);

/** Paragraph text (as inline HTML) of a section, in order. */
export function paragraphs(tokens: Token[]): string[] {
  return tokens.filter((t): t is Tokens.Paragraph => t.type === "paragraph").map((t) => md.parseInline(t.text) as string);
}

export type Item = { term: string; text: string; html: string };

const cap = (h: string) => h.replace(/^((?:<[^>]+>)*)([a-z])/, (_, tags: string, c: string) => tags + c.toUpperCase());

/** List items; "**Term**: text" items are split into term and text. */
export function listItems(tokens: Token[], which = 0): Item[] {
  const lists = tokens.filter((t): t is Tokens.List => t.type === "list");
  const list = lists[which];
  if (!list) return [];
  return list.items.map((it) => {
    const m = it.text.match(/^\*\*(.+?)\*\*:?\s*([\s\S]*)$/);
    return m
      ? { term: md.parseInline(m[1]) as string, text: cap(md.parseInline(m[2]) as string), html: md.parseInline(it.text) as string }
      : { term: "", text: md.parseInline(it.text) as string, html: md.parseInline(it.text) as string };
  });
}

/** H3 sub-blocks inside a section: [{title, items}] */
export function subLists(raw: string): { title: string; items: Item[] }[] {
  return raw.split(/\n(?=### )/).filter((p) => p.startsWith("### ")).map((p) => {
    const [h, ...rest] = p.split("\n");
    return { title: md.parseInline(clean(h.replace(/^### /, ""))) as string, items: listItems(md.lexer(clean(rest.join("\n")))) };
  });
}

export function navPages() {
  const pages = allPages();
  return site.nav_order
    .map((p) => pages.find((x) => x.meta.path === p))
    .filter(Boolean)
    .map((p) => ({ label: p!.meta.nav, href: p!.meta.path }));
}

export function footerPages() {
  return allPages().filter((p) => p.meta.footer_only === "true").map((p) => ({ label: p.meta.nav, href: p.meta.path }));
}
