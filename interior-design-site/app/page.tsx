import Link from "next/link";
import { cities, services } from "../lib/cities";

export default function Home() {
  return (
    <main>
      <section className="hero">
        <div>
          <span className="tag">Interior design studio</span>
          <h1>Interior design that captures attention & converts inquiries.</h1>
          <p>
            AuraSpaces builds premium residential and commercial interiors with a
            conversion-first website experience. Explore curated city pages and
            book a free consultation in minutes.
          </p>
          <div className="grid" style={{ marginTop: "1.5rem" }}>
            <div className="card">
              <h3>3-step process</h3>
              <p>Measure → 3D design → turnkey execution with weekly updates.</p>
            </div>
            <div className="card">
              <h3>Verified reviews</h3>
              <p>4.8★ average Google rating across Maharashtra studios.</p>
            </div>
          </div>
        </div>
        <form className="hero-card">
          <h2>Get a free design consultation</h2>
          <div className="input-group">
            <label htmlFor="name">Name</label>
            <input id="name" placeholder="Your full name" />
          </div>
          <div className="input-group">
            <label htmlFor="phone">Phone</label>
            <input id="phone" placeholder="+91 00000 00000" />
          </div>
          <div className="input-group">
            <label htmlFor="city">City</label>
            <select id="city" defaultValue="nashik">
              {cities.map((city) => (
                <option key={city.slug} value={city.slug}>
                  {city.name}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className="primary">Book free call</button>
        </form>
      </section>

      <section className="section">
        <h2>High-converting design services</h2>
        <div className="grid">
          {services.map((service) => (
            <div key={service} className="card">
              <h3>{service}</h3>
              <p>
                Dedicated project manager, in-house execution, and weekly
                milestone updates.
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Explore city pages</h2>
        <div className="grid">
          {cities.map((city) => (
            <Link key={city.slug} href={`/interior-design/${city.slug}`} className="card">
              <h3>Interior design in {city.name}</h3>
              <p>{city.highlight}</p>
              <strong>Packages from {city.startingPrice}</strong>
              <p style={{ marginTop: "0.5rem" }}>
                Top areas: {city.areas.slice(0, 3).join(", ")}.
              </p>
            </Link>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Why AuraSpaces</h2>
        <div className="grid">
          {[
            "Dedicated CRM for every lead",
            "On-site measurements in 48 hours",
            "Transparent pricing & timelines",
            "High-end material library"
          ].map((reason) => (
            <div key={reason} className="card">
              <h3>{reason}</h3>
              <p>
                We combine local expertise with national-grade design systems to
                deliver predictable outcomes.
              </p>
            </div>
          ))}
        </div>
      </section>

      <footer className="footer">
        <strong>AuraSpaces Interior Design Studio</strong>
        <small>Serving Nashik, Pune, Nagpur · Call +91 90000 12345</small>
      </footer>
    </main>
  );
}
