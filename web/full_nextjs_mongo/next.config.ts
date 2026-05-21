import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow images from external URLs (like placeholder images)
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },
};

export default nextConfig;
