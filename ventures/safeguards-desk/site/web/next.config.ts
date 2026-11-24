import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  basePath: process.env.SITE_BASE_PATH || "",
  experimental: {
    optimizePackageImports: ["radix-ui", "@base-ui/react", "@tabler/icons-react", "@remixicon/react", "lucide-react"],
  },
};

export default nextConfig;
