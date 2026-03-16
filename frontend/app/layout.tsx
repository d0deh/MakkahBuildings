import type { Metadata } from "next";
import { Cairo } from "next/font/google";
import "./globals.css";

const cairo = Cairo({
  subsets: ["arabic", "latin"],
  variable: "--font-cairo",
});

export const metadata: Metadata = {
  title: "مولد التقارير العمرانية",
  description: "تحليل بيانات المسح العمراني وإنشاء التقارير تلقائياً",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className={`${cairo.variable} font-cairo antialiased bg-background`}>
        {children}
      </body>
    </html>
  );
}
