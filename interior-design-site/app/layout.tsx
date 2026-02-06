import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AuraSpaces | Interior Design Studio",
  description: "Premium interior design studio delivering modular kitchens, luxury interiors, and turnkey execution across Maharashtra.",
  metadataBase: new URL("https://auraspaces.example")
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
