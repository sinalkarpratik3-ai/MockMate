import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "MockMate — Interview Preparation Platform",
  description: "Practice technical interviews, test your knowledge, review your answers, and build confidence one session at a time.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const rawBackend =
    process.env.BACKEND_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "";

  let runtimeApiUrl = "";
  if (rawBackend && rawBackend.trim().length > 0) {
    let trimmed = rawBackend.trim().replace(/\/+$/, "");
    if (!trimmed.startsWith("http://") && !trimmed.startsWith("https://")) {
      trimmed = `https://${trimmed}`;
    }
    runtimeApiUrl = trimmed.endsWith("/api") ? trimmed : `${trimmed}/api`;
  }

  return (
    <html lang="en" className={`${inter.variable} h-full antialiased`}>
      <head>
        <script
          id="mockmate-runtime-env"
          dangerouslySetInnerHTML={{
            __html: `window.__MOCKMATE_API_URL__ = ${JSON.stringify(runtimeApiUrl)};`,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col font-sans bg-[#F7F3EA] text-[#252923]">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
