export function SectionHead({ eyebrow, title, intro, id, center = false }: {
  eyebrow?: string; title: string; intro?: string; id: string; center?: boolean;
}) {
  return (
    <div className={center ? "mx-auto flex max-w-2xl flex-col items-center gap-3 text-center" : "flex max-w-2xl flex-col gap-3"}>
      {eyebrow && <p className="font-mono text-xs uppercase tracking-[0.08em] text-primary">{eyebrow}</p>}
      <h2 id={id} className="text-3xl font-semibold leading-[1.1] tracking-[-0.02em] sm:text-[2.5rem]" dangerouslySetInnerHTML={{ __html: title }} />
      {intro && <p className="text-lg leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: intro }} />}
    </div>
  );
}
