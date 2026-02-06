export type City = {
  slug: string;
  name: string;
  highlight: string;
  startingPrice: string;
  phone: string;
  areas: string[];
  rating: string;
};

export const cities: City[] = [
  {
    slug: "nashik",
    name: "Nashik",
    highlight: "Luxury home interiors with vastu-ready planning.",
    startingPrice: "₹4.5L",
    phone: "+91 90000 12345",
    areas: ["Gangapur Road", "College Road", "Cidco", "Indira Nagar"],
    rating: "4.9"
  },
  {
    slug: "pune",
    name: "Pune",
    highlight: "Modern minimal design for premium apartments.",
    startingPrice: "₹5.2L",
    phone: "+91 90000 12346",
    areas: ["Koregaon Park", "Kothrud", "Baner", "Hinjewadi"],
    rating: "4.8"
  },
  {
    slug: "nagpur",
    name: "Nagpur",
    highlight: "Smart storage solutions for growing families.",
    startingPrice: "₹4.1L",
    phone: "+91 90000 12347",
    areas: ["Civil Lines", "Dharampeth", "Manish Nagar", "Trimurti Nagar"],
    rating: "4.8"
  }
];

export const services = [
  "Residential interiors",
  "Commercial design",
  "Modular kitchens",
  "3D visualisation",
  "Turnkey execution"
];
