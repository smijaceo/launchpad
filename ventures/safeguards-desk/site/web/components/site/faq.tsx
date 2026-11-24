"use client";
// Uses the 21st.dev "Accordion" (wensity/accordion, Base UI) in its faq variant.
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

export function Faq({ items }: { items: { q: string; a: string }[] }) {
  return (
    <Accordion type="multiple" variant="faq" className="w-full">
      {items.map((it, i) => (
        <AccordionItem key={i} value={`q${i}`}>
          <AccordionTrigger className="text-left text-lg font-semibold">
            <span dangerouslySetInnerHTML={{ __html: it.q }} />
          </AccordionTrigger>
          <AccordionContent>
            <div className="prose prose-neutral max-w-none text-base leading-relaxed text-muted-foreground prose-a:text-ink" dangerouslySetInnerHTML={{ __html: it.a }} />
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
