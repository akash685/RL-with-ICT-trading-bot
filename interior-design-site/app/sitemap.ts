import type { MetadataRoute } from "next";
import { cities } from "../lib/cities";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://auraspaces.example";

  const cityRoutes = cities.map((city) => ({
    url: `${baseUrl}/interior-design/${city.slug}`,
    lastModified: new Date(),
    changeFrequency: "weekly" as const,
    priority: 0.8
  }));

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 1
    },
    ...cityRoutes
  ];
}
