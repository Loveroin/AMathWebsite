import type { ReactNode } from "react";

export default function ProblemsLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <section style={{ maxWidth: 800, margin: "0 auto" }}>
      {children}
    </section>
  );
}
