import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { cities, services } from "../../../lib/cities";

type PageProps = {
  params: {
    city: string;
  };
};

export function generateStaticParams() {
  return cities.map((city) => ({ city: city.slug }));
}

export function generateMetadata({ params }: PageProps): Metadata {
  const city = cities.find((item) => item.slug === params.city);

  if (!city) {
    return {
      title: "Interior Design Studio",
      description: "Premium interior design services."
    };
  }

  return {
    title: `Interior Design in ${city.name} | AuraSpaces`,
    description: `Interior design services in ${city.name} for residential and commercial projects. Packages from ${city.startingPrice}.`,
    openGraph: {
      title: `Interior Design in ${city.name}`,
      description: city.highlight
    }
  };
}

export default function CityPage({ params }: PageProps) {
  const city = cities.find((item) => item.slug === params.city);

  if (!city) {
    notFound();
  }

  const localBusinessSchema = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    name: `AuraSpaces Interior Design - ${city.name}`,
    address: {
      "@type": "PostalAddress",
      addressLocality: city.name,
      addressCountry: "IN"
    },
    telephone: city.phone,
    aggregateRating: {
      "@type": "AggregateRating",
      ratingValue: city.rating,
      reviewCount: 120
    },
    areaServed: city.areas
  };

  return (
    <main>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(localBusinessSchema) }}
      />
      <section className="hero">
        <div>
          <span className="tag">Local interior design</span>
          <h1>Interior design in {city.name}</h1>
          <p>
            Designed for {city.name} homeowners & commercial spaces. Get custom
            layouts, 3D walkthroughs, and turnkey execution with local project
            managers.
          </p>
          <div className="grid" style={{ marginTop: "1.5rem" }}>
            <div className="card">
              <h3>Starting package</h3>
              <p>{city.startingPrice} for 2BHK interiors</p>
            </div>
            <div className="card">
              <h3>Turnaround</h3>
              <p>Design in 7 days · Execution in 45 days</p>
            </div>
          </div>
        </div>
        <form className="hero-card">
          <h2>Plan your {city.name} project</h2>
          <div className="input-group">
            <label htmlFor="name">Name</label>
            <input id="name" placeholder="Your full name" />
          </div>
          <div className="input-group">
            <label htmlFor="phone">Phone</label>
            <input id="phone" placeholder="+91 00000 00000" />
          </div>
          <div className="input-group">
            <label htmlFor="service">Project type</label>
            <select id="service" defaultValue={services[0]}>
              {services.map((service) => (
                <option key={service} value={service}>
                  {service}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className="primary">Request city quote</button>
        </form>
      </section>

      <section className="section">
        <h2>Services in {city.name}</h2>
        <div className="grid">
          {services.map((service) => (
            <div key={service} className="card">
              <h3>{service}</h3>
              <p>
                City-specific material sourcing, smart space planning, and local
                project coordination.
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Local proof</h2>
        <div className="grid">
          {[
            `120+ projects delivered in ${city.name}`,
            `${city.rating}★ average rating on Google`,
            "Dedicated on-site design manager"
          ].map((item) => (
            <div key={item} className="card">
              <h3>{item}</h3>
              <p>
                Verified project documentation and client walkthroughs available
                on request.
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Explore other cities</h2>
        <div className="grid">
          {cities
            .filter((item) => item.slug !== city.slug)
            .map((item) => (
              <Link key={item.slug} href={`/interior-design/${item.slug}`} className="card">
                <h3>Interior design in {item.name}</h3>
                <p>{item.highlight}</p>
              </Link>
            ))}
        </div>
      </section>

      <footer className="footer">
        <strong>AuraSpaces Interior Design Studio</strong>
        <small>
          Reach our {city.name} studio · Call {city.phone} · WhatsApp
          consultations available
        </small>
      </footer>
    </main>
  );
}
