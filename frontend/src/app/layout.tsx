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
  const runtimeApiUrl =
    process.env.NEXT_PUBLIC_API_URL ||
    process.env.BACKEND_URL ||
    "";

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
