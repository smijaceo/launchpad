import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export function CtaBand({ title, text, href, label }: { title: string; text: string; href: string; label: string }) {
  return (
    <section className="bg-foreground text-background">
      <div className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-8 px-5 py-16 sm:px-8 lg:flex-row lg:items-center">
        <div className="max-w-2xl">
          <h2 className="text-3xl font-semibold tracking-[-0.02em] sm:text-4xl" dangerouslySetInnerHTML={{ __html: title }} />
          <p className="mt-3 text-lg text-background/75" dangerouslySetInnerHTML={{ __html: text }} />
        </div>
        <Button asChild size="lg" className="h-12 shrink-0 rounded-lg bg-primary px-6 text-base text-primary-foreground hover:bg-primary/90">
          <a href={href}>{label} <ArrowRight aria-hidden /></a>
        </Button>
      </div>
    </section>
  );
}
