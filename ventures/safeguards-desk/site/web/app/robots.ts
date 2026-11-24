import type { MetadataRoute } from "next";
import { isPreview, site } from "@/lib/content";

export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
  return isPreview
    ? { rules: { userAgent: "*", disallow: "/" } }
    : { rules: { userAgent: "*", allow: "/" }, sitemap: `${site.base_url}/sitemap.xml` };
}
