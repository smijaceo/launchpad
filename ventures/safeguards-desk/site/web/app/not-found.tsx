import { bookingUrl, navPages } from "@/lib/content";
import { SiteHeader } from "@/components/site/site-header";

export default function NotFound() {
  return (
    <>
      <SiteHeader links={navPages()} current="" bookingUrl={bookingUrl} />
      <main id="main" tabIndex={-1} className="mx-auto max-w-3xl px-5 py-24 outline-none sm:px-8">
        <h1 className="text-4xl font-semibold tracking-[-0.03em]">Page not found</h1>
        <p className="mt-4 text-lg text-muted-foreground">
          The page you asked for doesn’t exist. Go to the <a className="text-ink underline" href="/">home page</a>.
        </p>
      </main>
    </>
  );
}
