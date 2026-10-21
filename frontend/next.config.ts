import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  async rewrites() {
    const rawBackend =
      process.env.BACKEND_INTERNAL_URL ||
      process.env.NEXT_PUBLIC_API_URL ||
      "http://127.0.0.1:8000";
    const cleanBackend = rawBackend.replace(/\/api\/?$/, "").replace(/\/+$/, "");
    return [
      {
        source: "/api/:path*",
        destination: `${cleanBackend}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
