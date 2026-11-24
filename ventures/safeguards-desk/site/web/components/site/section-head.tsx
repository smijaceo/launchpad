export function SectionHead({ eyebrow, title, intro, id }: { eyebrow?: string; title: string; intro?: string; id: string }) {
  return (
    <div className="flex max-w-2xl flex-col gap-4">
      {eyebrow && <p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">{eyebrow}</p>}
      <h2 id={id} className="font-serif text-3xl font-semibold leading-[1.1] tracking-tight sm:text-[2.6rem]" dangerouslySetInnerHTML={{ __html: title }} />
      {intro && <p className="text-lg leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: intro }} />}
    </div>
  );
}
