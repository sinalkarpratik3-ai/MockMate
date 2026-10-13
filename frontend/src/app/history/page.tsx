"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { Interview } from "@/types";
import { 
  History, 
  ChevronRight, 
  PlusCircle, 
  Loader2, 
  AlertCircle,
  Filter
} from "lucide-react";

export default function HistoryPage() {
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modeFilter, setModeFilter] = useState<"all" | "mcq" | "text">("all");

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiRequest<Interview[]>("/interviews");
      setInterviews(data);
    } catch (err: any) {
      setError(err.message || "Failed to load interview history.");
    } finally {
      setLoading(false);
    }
  };

  const filteredInterviews = interviews.filter((itv) => {
    if (modeFilter === "all") return true;
    return itv.mode === modeFilter;
  });

  return (
    <AppLayout>
      <div className="space-y-6 animate-fade-in pb-16">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <History className="h-6 w-6 text-indigo-600" />
              <span>Interview History</span>
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Complete chronological audit of your technical preparation simulations.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-xs transition-all"
            >
              <PlusCircle className="h-4 w-4" />
              <span>Start New Interview</span>
            </Link>
          </div>
        </div>

        {/* Filter controls */}
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-400" />
          <span className="text-xs font-semibold text-slate-500 mr-2">Filter Mode:</span>
          {(["all", "mcq", "text"] as const).map((m) => (
            <button
              key={m}
              type="button"
              onClick={() => setModeFilter(m)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold capitalize transition-all ${
                modeFilter === m
                  ? "bg-indigo-600 text-white shadow-xs"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
              }`}
            >
              {m === "all" ? "All Modes" : `${m.toUpperCase()} Mode`}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
            <p className="text-xs font-medium">Retrieving historical records...</p>
          </div>
        ) : error ? (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center justify-between">
            <span>{error}</span>
            <button onClick={fetchHistory} className="font-semibold underline">Retry</button>
          </div>
        ) : filteredInterviews.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-md mx-auto shadow-xs">
            <History className="h-10 w-10 text-slate-300 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-900">No interview records found</h3>
            <p className="text-xs text-slate-500 mt-1">
              {modeFilter !== "all" 
                ? `You haven't completed any ${modeFilter.toUpperCase()} interviews yet.`
                : "You haven't completed any interview sessions yet. Start your first session to track progress."}
            </p>
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 mt-5 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold shadow-xs hover:bg-indigo-700 transition-colors"
            >
              <PlusCircle className="h-3.5 w-3.5" />
              <span>Configure Interview</span>
            </Link>
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-600">
                <thead className="bg-slate-50 text-slate-400 font-semibold uppercase text-[10px] border-b border-slate-100">
                  <tr>
                    <th className="py-3.5 px-4">Date</th>
                    <th className="py-3.5 px-4">Job Role</th>
                    <th className="py-3.5 px-4">Difficulty</th>
                    <th className="py-3.5 px-4">Mode</th>
                    <th className="py-3.5 px-4">Questions</th>
                    <th className="py-3.5 px-4">Score</th>
                    <th className="py-3.5 px-4">Status</th>
                    <th className="py-3.5 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredInterviews.map((itv) => {
                    const isCompleted = itv.status === "completed";
                    return (
                      <tr key={itv.id} className="hover:bg-slate-50/70 transition-colors">
                        <td className="py-4 px-4 font-medium text-slate-900">
                          {new Date(itv.created_at).toLocaleDateString()}
                        </td>
                        <td className="py-4 px-4 font-semibold text-slate-800">{itv.job_role}</td>
                        <td className="py-4 px-4">
                          <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium">
                            {itv.difficulty}
                          </span>
                        </td>
                        <td className="py-4 px-4 uppercase font-semibold text-indigo-600">
                          {itv.mode}
                        </td>
                        <td className="py-4 px-4">{itv.num_questions} Qs</td>
                        <td className="py-4 px-4 font-bold text-slate-900">
                          {isCompleted ? `${itv.percentage}%` : "—"}
                        </td>
                        <td className="py-4 px-4">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            isCompleted 
                              ? "bg-emerald-100 text-emerald-800" 
                              : "bg-amber-100 text-amber-800"
                          }`}>
                            {isCompleted ? "Completed" : "In Progress"}
                          </span>
                        </td>
                        <td className="py-4 px-4 text-right">
                          <Link
                            href={isCompleted ? `/interviews/${itv.id}/results` : `/interviews/${itv.id}`}
                            className="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-800 font-semibold"
                          >
                            <span>{isCompleted ? "Review Results" : "Resume"}</span>
                            <ChevronRight className="h-3.5 w-3.5" />
                          </Link>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
