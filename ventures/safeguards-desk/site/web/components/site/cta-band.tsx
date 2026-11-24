import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export function CtaBand({ title, text, href, label }: { title: string; text: string; href: string; label: string }) {
  return (
    <section className="bg-ink text-background">
      <div className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-8 px-5 py-16 sm:px-8 lg:flex-row lg:items-center">
        <div className="max-w-2xl">
          <h2 className="font-serif text-3xl font-semibold tracking-tight sm:text-4xl" dangerouslySetInnerHTML={{ __html: title }} />
          <p className="mt-3 text-lg text-background/80" dangerouslySetInnerHTML={{ __html: text }} />
        </div>
        <Button asChild size="lg" className="h-12 shrink-0 rounded-full bg-background px-7 text-base text-ink hover:bg-background/90">
          <a href={href}>
            {label} <ArrowRight aria-hidden />
          </a>
        </Button>
      </div>
    </section>
  );
}
