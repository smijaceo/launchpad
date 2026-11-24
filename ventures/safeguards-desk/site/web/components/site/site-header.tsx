"use client";
// Adapted from 21st.dev "Classic Header with Sheet Menu" (ln-dev7/header-17).
import * as React from "react";
import { ArrowRight, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Wordmark } from "./logo";

type Link = { label: string; href: string };

export function SiteHeader({ links, current, bookingUrl }: { links: Link[]; current: string; bookingUrl: string }) {
  const [open, setOpen] = React.useState(false);
  return (
    <div className="sticky top-0 z-40 border-b border-border/80 bg-background/90 backdrop-blur supports-[backdrop-filter]:bg-background/75">
      <header className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-5 py-3 sm:px-8">
        <a href="/" className="rounded-md" aria-label="Countersign Security home">
          <Wordmark />
        </a>
        <nav aria-label="Main" className="hidden items-center gap-0.5 lg:flex">
          {links.filter((l) => l.href !== "/").map((link) => (
            <a
              key={link.href}
              href={link.href}
              aria-current={link.href === current ? "page" : undefined}
              className="rounded-md px-3 py-2 text-sm font-semibold text-muted-foreground transition-colors hover:bg-muted hover:text-foreground aria-[current=page]:text-foreground aria-[current=page]:underline aria-[current=page]:underline-offset-8"
            >
              {link.label}
            </a>
          ))}
        </nav>
        <div className="hidden lg:block">
          <Button asChild size="sm" className="rounded-lg px-4">
            <a href={bookingUrl}>
              Book a Scoping Call <ArrowRight aria-hidden />
            </a>
          </Button>
        </div>
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <button
              type="button"
              aria-label="Open Menu"
              className="grid size-11 place-items-center rounded-full border border-border text-foreground transition-colors hover:bg-muted lg:hidden"
            >
              <Menu className="size-5" aria-hidden />
            </button>
          </SheetTrigger>
          <SheetContent side="right" className="flex w-80 flex-col bg-background p-6">
            <SheetHeader className="mb-4 p-0 text-left">
              <SheetTitle className="sr-only">Menu</SheetTitle>
              <Wordmark />
            </SheetHeader>
            <nav aria-label="Mobile" className="flex flex-col gap-1">
              {links.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  onClick={() => setOpen(false)}
                  aria-current={link.href === current ? "page" : undefined}
                  className="rounded-md px-3 py-3 text-base font-semibold text-foreground transition-colors hover:bg-muted aria-[current=page]:bg-muted"
                >
                  {link.label}
                </a>
              ))}
            </nav>
            <div className="mt-auto border-t border-border pt-6">
              <Button asChild className="w-full rounded-lg" size="lg">
                <a href={bookingUrl}>
                  Book a Scoping Call <ArrowRight aria-hidden />
                </a>
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      </header>
    </div>
  );
}
