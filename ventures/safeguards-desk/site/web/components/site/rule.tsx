import { SectionHead } from "./section-head";

export function Rule({ title, paras }: { title: string; paras: string[] }) {
  return (
    <section aria-labelledby="rule" className="border-b border-border bg-muted">
      <div className="mx-auto grid max-w-6xl gap-10 px-5 py-20 sm:px-8 lg:grid-cols-[0.9fr_1.1fr] lg:py-24">
        <SectionHead id="rule" eyebrow="The rule" title={title} />
        <div className="flex flex-col gap-5 text-[17px] leading-relaxed text-foreground/85">
          {paras.map((p, i) => <p key={i} dangerouslySetInnerHTML={{ __html: p }} />)}
          <p className="text-sm text-muted-foreground">General information, not legal advice.</p>
        </div>
      </div>
    </section>
  );
}
