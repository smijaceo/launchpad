// Adapted from 21st.dev "Feature Overview Bento" (Hirael feature-10, MIT · Mohammad Shehadeh).
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { Item } from "@/lib/content";
import { SectionHead } from "./section-head";

const CELL = "min-h-full rounded-none border-0 shadow-none gap-3";
const SPANS = [
  "col-span-6 lg:col-span-4 lg:row-span-2",
  "col-span-6 sm:col-span-3 lg:col-span-2",
  "col-span-6 sm:col-span-3 lg:col-span-2",
  "col-span-6 lg:col-span-4",
  "col-span-6 lg:col-span-2",
];

export function Included({ title, intro, items, moreHref, moreLabel }: {
  title: string; intro: string; items: Item[]; moreHref: string; moreLabel: string;
}) {
  return (
    <section aria-labelledby="included" className="border-b border-border">
      <div className="mx-auto max-w-6xl px-5 py-20 sm:px-8 lg:py-28">
        <SectionHead id="included" eyebrow="What you get" title={title} intro={intro} />
        <div className="mt-12 grid grid-cols-6 gap-px overflow-hidden rounded-xl border border-border bg-border">
          {items.map((item, i) => (
            <Card key={item.term} className={cn(CELL, SPANS[i] ?? "col-span-6 lg:col-span-2", i === 0 && "bg-ink text-background")}>
              <CardHeader>
                <CardDescription className={cn("font-mono text-xs uppercase tabular-nums", i === 0 ? "text-background/70" : "text-primary")}>
                  {String(i + 1).padStart(2, "0")} / {String(items.length).padStart(2, "0")}
                </CardDescription>
                <CardTitle
                  className={cn("font-serif font-semibold tracking-tight", i === 0 ? "text-3xl sm:text-4xl" : "text-xl")}
                  dangerouslySetInnerHTML={{ __html: item.term }}
                />
              </CardHeader>
              <CardContent>
                <p
                  className={cn(i === 0 ? "max-w-md text-lg leading-relaxed text-background/85" : "text-sm leading-relaxed text-muted-foreground")}
                  dangerouslySetInnerHTML={{ __html: item.text }}
                />
              </CardContent>
            </Card>
          ))}
        </div>
        <Button asChild variant="outline" className="mt-8 rounded-full">
          <a href={moreHref}>
            {moreLabel} <ArrowRight aria-hidden />
          </a>
        </Button>
      </div>
    </section>
  );
}
