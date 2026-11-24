// Countersign Security seal (brand/logo/icon.svg), drawn in currentColor.
export function LogoMark({ className = "size-7" }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} aria-hidden="true" focusable="false">
      <circle cx="32" cy="29" r="19" fill="none" stroke="currentColor" strokeWidth="4.5" />
      <path d="M22.5 29.5 L29.5 36.5 L42.5 22" fill="none" stroke="var(--primary)" strokeWidth="5.5" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M12 54 C 22 49, 30 57, 40 52 S 52 50, 54 52" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" />
    </svg>
  );
}

export function Wordmark() {
  return (
    <span className="flex items-center gap-2 text-ink">
      <LogoMark />
      <span className="text-[17px] font-semibold tracking-tight text-foreground" translate="no">
        Countersign&nbsp;Security
      </span>
    </span>
  );
}
