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
      setError(err.message || "Failed to load practice history.");
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
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-[#E8DDCA] pb-4">
          <div>
            <h1 className="text-2xl font-bold text-[#252923] tracking-tight flex items-center gap-2">
              <History className="h-6 w-6 text-[#24483F]" />
              <span>Practice History</span>
            </h1>
            <p className="text-xs sm:text-sm text-[#777B74] mt-1">
              Chronological overview of all your practice sessions and performance.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] font-semibold text-xs shadow-xs transition-all"
            >
              <PlusCircle className="h-4 w-4" />
              <span>Start Practising</span>
            </Link>
          </div>
        </div>

        {/* Filter controls */}
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-[#879477]" />
          <span className="text-xs font-semibold text-[#777B74] mr-2">Filter Format:</span>
          {(["all", "mcq", "text"] as const).map((m) => (
            <button
              key={m}
              type="button"
              onClick={() => setModeFilter(m)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                modeFilter === m
                  ? "bg-[#24483F] text-[#F7F3EA] shadow-xs"
                  : "bg-white text-[#252923] border border-[#E8DDCA] hover:bg-[#FAF8F4]"
              }`}
            >
              {m === "all" ? "All Formats" : m === "mcq" ? "Multiple Choice" : "Written"}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-medium">Retrieving session records...</p>
          </div>
        ) : error ? (
          <div className="p-4 rounded-xl bg-[#FDF1F0] border border-[#E8DDCA] text-[#B8473F] text-xs flex items-center justify-between">
            <span>{error}</span>
            <button onClick={fetchHistory} className="font-semibold underline">Retry</button>
          </div>
        ) : filteredInterviews.length === 0 ? (
          <div className="bg-white rounded-2xl border border-[#E8DDCA] p-12 text-center max-w-md mx-auto shadow-xs">
            <History className="h-10 w-10 text-[#879477] mx-auto mb-3" />
            <h3 className="text-base font-bold text-[#252923]">No practice records found</h3>
            <p className="text-xs text-[#777B74] mt-1">
              {modeFilter !== "all" 
                ? `You haven't completed any ${modeFilter === "mcq" ? "Multiple Choice" : "Written"} sessions yet.`
                : "You haven't completed any sessions yet. Start your first session to track progress."}
            </p>
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 mt-5 px-4 py-2 rounded-xl bg-[#24483F] text-[#F7F3EA] text-xs font-semibold shadow-xs hover:bg-[#1A342D] transition-colors"
            >
              <PlusCircle className="h-3.5 w-3.5" />
              <span>Create Practice Test</span>
            </Link>
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-[#E8DDCA] shadow-xs overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-[#252923]">
                <thead className="bg-[#FAF8F4] text-[#879477] font-semibold uppercase text-[10px] border-b border-[#E8DDCA]">
                  <tr>
                    <th className="py-3.5 px-4">Date</th>
                    <th className="py-3.5 px-4">Role</th>
                    <th className="py-3.5 px-4">Difficulty</th>
                    <th className="py-3.5 px-4">Format</th>
                    <th className="py-3.5 px-4">Questions</th>
                    <th className="py-3.5 px-4">Score</th>
                    <th className="py-3.5 px-4">Status</th>
                    <th className="py-3.5 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E8DDCA]">
                  {filteredInterviews.map((itv) => {
                    const isCompleted = itv.status === "completed";
                    return (
                      <tr key={itv.id} className="hover:bg-[#FAF8F4] transition-colors">
                        <td className="py-4 px-4 font-medium text-[#252923]">
                          {new Date(itv.created_at).toLocaleDateString()}
                        </td>
                        <td className="py-4 px-4 font-semibold text-[#252923]">{itv.job_role}</td>
                        <td className="py-4 px-4">
                          <span className="px-2 py-0.5 rounded-full bg-[#EDF3EB] text-[#24483F] font-medium border border-[#DCE6D8]">
                            {itv.difficulty}
                          </span>
                        </td>
                        <td className="py-4 px-4 uppercase font-semibold text-[#24483F]">
                          {itv.mode === "mcq" ? "Multiple Choice" : "Written"}
                        </td>
                        <td className="py-4 px-4">{itv.num_questions} Qs</td>
                        <td className="py-4 px-4 font-bold text-[#252923]">
                          {isCompleted ? `${itv.percentage}%` : "—"}
                        </td>
                        <td className="py-4 px-4">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                            isCompleted 
                              ? "bg-[#EDF3EB] text-[#367451] border-[#DCE6D8]" 
                              : "bg-[#F7ECE7] text-[#C66A4A] border-[#E8DDCA]"
                          }`}>
                            {isCompleted ? "Completed" : "In Progress"}
                          </span>
                        </td>
                        <td className="py-4 px-4 text-right">
                          <Link
                            href={isCompleted ? `/interviews/${itv.id}/results` : `/interviews/${itv.id}`}
                            className="inline-flex items-center gap-1 text-[#24483F] hover:underline font-semibold"
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
