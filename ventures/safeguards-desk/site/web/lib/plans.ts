import { bookingUrl, getPage, listItems, paragraphs, sections, inline } from "./content";
import type { Plan } from "@/components/site/plans";

/** Plans come from copy/site/pricing.md (`<!--plan:id-->` sections), so prices stay claim-checked. */
export function planList(): Plan[] {
  const { sections: s } = sections(getPage("pricing").body);
  return s.filter((x) => x.raw.includes("<!--plan:")).map((x) => {
    const [price, description] = paragraphs(x.tokens);
    return {
      id: x.id, name: inline(x.title), price, description,
      features: listItems(x.tokens).map((i) => i.html),
      cta: x.id === "msp" ? "Talk About a Pilot" : "Book a Scoping Call",
      href: bookingUrl,
    };
  });
}
