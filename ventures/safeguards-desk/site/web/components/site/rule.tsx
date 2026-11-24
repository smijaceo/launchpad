import { SectionHead } from "./section-head";

export function Rule({ title, paras }: { title: string; paras: string[] }) {
  const [first, ...rest] = paras;
  const last = rest.pop();
  return (
    <section aria-labelledby="rule" className="border-b border-border bg-card">
      <div className="mx-auto grid max-w-6xl gap-10 px-5 py-20 sm:px-8 lg:grid-cols-[1fr_1.4fr] lg:py-28">
        <div className="lg:sticky lg:top-28 lg:self-start">
          <SectionHead id="rule" eyebrow="The rule" title={title} />
        </div>
        <div className="flex flex-col gap-6 text-lg leading-relaxed text-foreground/85">
          <p className="font-serif text-2xl leading-snug text-foreground" dangerouslySetInnerHTML={{ __html: first }} />
          {rest.map((p, i) => <p key={i} dangerouslySetInnerHTML={{ __html: p }} />)}
          {last && (
            <p className="border-l-4 border-primary bg-background/60 py-3 pl-5 text-foreground" dangerouslySetInnerHTML={{ __html: last }} />
          )}
        </div>
      </div>
    </section>
  );
}
