"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Problem = {
  id: number;
  title: string;
  difficulty: number;
  problem_type: string;
};

export default function ProblemsPage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProblems() {
      try {
        const data = await apiFetch("/problems?skip=0&limit=20");
        setProblems(data.items);
      } catch (err: any) {
        setError(err.message || "加载失败");
      } finally {
        setLoading(false);
      }
    }

    loadProblems();
  }, []);

  if (loading) return <p>加载中...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <main style={{ padding: 24 }}>
      <h1>📚 题目列表</h1>

      <ul style={{ marginTop: 16 }}>
        {problems.map((p) => (
          <li key={p.id} style={{ marginBottom: 12 }}>
            <Link href={`/problems/${p.id}`}>
              {p.title}
            </Link>
            <span style={{ marginLeft: 8, color: "#666" }}>
              （难度 {p.difficulty}）
            </span>
          </li>
        ))}
      </ul>
    </main>
  );
}
