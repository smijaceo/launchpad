import type { MetadataRoute } from "next";
import { allPages, site } from "@/lib/content";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return allPages().map((p) => ({ url: `${site.base_url}${p.meta.path}` }));
}
