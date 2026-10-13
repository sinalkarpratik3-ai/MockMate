"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { useAuth } from "@/context/AuthContext";
import { apiRequest } from "@/lib/api";
import { DashboardSummary } from "@/types";
import { 
  CheckCircle, 
  Target, 
  FileText, 
  PlusCircle, 
  Calendar, 
  ArrowRight, 
  AlertTriangle, 
  TrendingUp, 
  Loader2,
  ChevronRight,
  Award
} from "lucide-react";

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const summary = await apiRequest<DashboardSummary>("/dashboard");
      setData(summary);
    } catch (err: any) {
      setError(err.message || "Failed to load dashboard metrics.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="space-y-8 animate-fade-in">
        {/* Header greeting & quick action */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-[#E8DDCA]">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-[#252923] tracking-tight">
              Welcome back, {user?.full_name || user?.email.split("@")[0]}
            </h1>
            <p className="text-xs sm:text-sm text-[#777B74] mt-1">
              Here is your current interview preparation progress and practice summary.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] font-semibold text-xs sm:text-sm shadow-sm transition-all"
            >
              <PlusCircle className="h-4 w-4" />
              <span>Start Practising</span>
            </Link>
          </div>
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-medium">Loading your practice summary...</p>
          </div>
        ) : error ? (
          <div className="p-4 rounded-xl bg-[#FDF1F0] border border-[#E8DDCA] text-[#B8473F] text-xs flex items-center justify-between">
            <span>{error}</span>
            <button
              onClick={fetchDashboard}
              className="font-semibold underline hover:text-[#94362E]"
            >
              Retry
            </button>
          </div>
        ) : data ? (
          <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
              {/* Total Interviews */}
              <div className="bg-white p-5 rounded-2xl border border-[#E8DDCA] shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-[#879477] uppercase tracking-wider">Completed Sessions</p>
                  <p className="text-3xl font-extrabold text-[#252923] mt-1">{data.total_interviews}</p>
                  <p className="text-[11px] text-[#777B74] mt-1">Full sessions completed</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-[#EDF3EB] border border-[#DCE6D8] flex items-center justify-center text-[#24483F]">
                  <Award className="h-6 w-6" />
                </div>
              </div>

              {/* Questions Attempted */}
              <div className="bg-white p-5 rounded-2xl border border-[#E8DDCA] shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-[#879477] uppercase tracking-wider">Questions Practised</p>
                  <p className="text-3xl font-extrabold text-[#252923] mt-1">{data.total_questions_attempted}</p>
                  <p className="text-[11px] text-[#777B74] mt-1">Across all tracks</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-[#EDF3EB] border border-[#DCE6D8] flex items-center justify-center text-[#367451]">
                  <CheckCircle className="h-6 w-6" />
                </div>
              </div>

              {/* MCQ Accuracy */}
              <div className="bg-white p-5 rounded-2xl border border-[#E8DDCA] shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-[#879477] uppercase tracking-wider">MCQ Accuracy</p>
                  <p className="text-3xl font-extrabold text-[#252923] mt-1">
                    {data.mcq_accuracy_pct}%
                  </p>
                  <p className="text-[11px] text-[#777B74] mt-1">Multiple choice average</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-[#EDF3EB] border border-[#DCE6D8] flex items-center justify-center text-[#24483F]">
                  <Target className="h-6 w-6" />
                </div>
              </div>

              {/* Average Text Score */}
              <div className="bg-white p-5 rounded-2xl border border-[#E8DDCA] shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-[#879477] uppercase tracking-wider">Average Written Score</p>
                  <p className="text-3xl font-extrabold text-[#252923] mt-1">
                    {data.avg_text_score} <span className="text-sm font-normal text-[#879477]">/ 10</span>
                  </p>
                  <p className="text-[11px] text-[#777B74] mt-1">Written answer review</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-[#F7ECE7] border border-[#E8DDCA] flex items-center justify-center text-[#C66A4A]">
                  <FileText className="h-6 w-6" />
                </div>
              </div>
            </div>

            {/* Daily Question Callout */}
            <div className="bg-[#FAF8F4] border border-[#E8DDCA] rounded-2xl p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="flex items-start sm:items-center gap-3.5">
                <div className="h-10 w-10 rounded-xl bg-[#C66A4A] text-[#F7F3EA] flex items-center justify-center shrink-0 shadow-sm">
                  <Calendar className="h-5 w-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-[#252923]">Question of the Day</span>
                    {data.has_attempted_daily ? (
                      <span className="text-[10px] bg-[#EDF3EB] text-[#24483F] font-bold px-2 py-0.5 rounded-full border border-[#DCE6D8]">
                        Completed Today
                      </span>
                    ) : (
                      <span className="text-[10px] bg-[#F7ECE7] text-[#C66A4A] font-bold px-2 py-0.5 rounded-full border border-[#E8DDCA]">
                        Pending
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-[#777B74] mt-0.5">
                    {data.has_attempted_daily 
                      ? "Great work! You have completed today's technical practice question." 
                      : "Build a consistent habit with today's featured question."}
                  </p>
                </div>
              </div>

              <Link
                href="/daily"
                className="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-xl bg-white border border-[#E8DDCA] text-[#252923] hover:text-[#24483F] hover:border-[#DCE6D8] text-xs font-semibold shadow-xs transition-colors shrink-0"
              >
                <span>{data.has_attempted_daily ? "Review Daily Answer" : "Solve Daily Challenge"}</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>

            {/* Two Column Section: Weak Topics & Role Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Weak Topics */}
              <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5 text-[#C66A4A]" />
                    <h2 className="text-base font-bold text-[#252923]">Topics to Revisit</h2>
                  </div>
                  <span className="text-xs text-[#879477]">Accuracy &lt; 60%</span>
                </div>

                {data.weak_topics.length === 0 ? (
                  <div className="py-10 text-center my-auto">
                    <CheckCircle className="h-8 w-8 text-[#367451] mx-auto mb-2 opacity-80" />
                    <p className="text-sm font-semibold text-[#252923]">No Weak Topics Identified</p>
                    <p className="text-xs text-[#777B74] mt-1 max-w-xs mx-auto">
                      All attempted topics currently maintain 60% or higher accuracy. Keep challenging yourself!
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3 flex-1">
                    {data.weak_topics.map((wt) => (
                      <div 
                        key={`${wt.role}-${wt.topic}`} 
                        className="p-3.5 rounded-xl border border-[#E8DDCA] bg-[#FAF8F4] flex items-center justify-between gap-3"
                      >
                        <div className="min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-xs text-[#252923] truncate">{wt.topic}</span>
                            <span className="text-[10px] bg-[#EDF3EB] text-[#24483F] px-1.5 py-0.5 rounded font-medium border border-[#DCE6D8]">
                              {wt.role}
                            </span>
                          </div>
                          <p className="text-[11px] text-[#777B74] mt-0.5">
                            Accuracy: <span className="font-bold text-[#C66A4A]">{wt.accuracy_percentage}%</span> ({wt.attempts} attempts)
                          </p>
                        </div>

                        <Link
                          href={`/interviews/new?role=${encodeURIComponent(wt.role)}`}
                          className="shrink-0 text-[11px] font-semibold text-[#24483F] hover:text-[#1A342D] bg-[#EDF3EB] border border-[#DCE6D8] px-2.5 py-1 rounded-lg transition-colors"
                        >
                          Practise
                        </Link>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Role Performance */}
              <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-[#24483F]" />
                    <h2 className="text-base font-bold text-[#252923]">Performance by Role</h2>
                  </div>
                  <Link href="/analytics" className="text-xs font-semibold text-[#24483F] hover:underline">
                    View Progress
                  </Link>
                </div>

                {data.role_stats.length === 0 ? (
                  <div className="py-10 text-center my-auto">
                    <p className="text-sm font-semibold text-[#252923]">No Role Data Yet</p>
                    <p className="text-xs text-[#777B74] mt-1">Complete your first practice session to see performance breakdown.</p>
                  </div>
                ) : (
                  <div className="space-y-4 flex-1">
                    {data.role_stats.map((rs) => (
                      <div key={rs.role}>
                        <div className="flex items-center justify-between text-xs mb-1.5">
                          <span className="font-semibold text-[#252923]">{rs.role}</span>
                          <span className="text-[#777B74]">{rs.interviews_count} sessions • <strong className="text-[#24483F]">{rs.avg_score_pct}%</strong> avg</span>
                        </div>
                        <div className="w-full bg-[#FAF8F4] border border-[#E8DDCA] rounded-full h-2.5 overflow-hidden">
                          <div 
                            className="bg-[#24483F] h-2.5 rounded-full transition-all duration-500" 
                            style={{ width: `${Math.min(rs.avg_score_pct, 100)}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Recent Activity Section */}
            <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-base font-bold text-[#252923]">Recent Practice Sessions</h2>
                <Link href="/history" className="text-xs font-semibold text-[#24483F] hover:underline">
                  Full History
                </Link>
              </div>

              {data.recent_interviews.length === 0 ? (
                <div className="py-12 text-center">
                  <p className="text-sm font-semibold text-[#252923]">Your progress starts with your first practice session.</p>
                  <p className="text-xs text-[#777B74] mt-1 max-w-sm mx-auto">
                    Choose your target role and format to begin practising and recording feedback.
                  </p>
                  <Link
                    href="/interviews/new"
                    className="inline-flex items-center gap-1.5 mt-4 px-4 py-2 rounded-xl bg-[#24483F] text-[#F7F3EA] font-semibold text-xs shadow-sm hover:bg-[#1A342D] transition-colors"
                  >
                    <PlusCircle className="h-3.5 w-3.5" />
                    <span>Start Practising</span>
                  </Link>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-[#252923]">
                    <thead className="bg-[#FAF8F4] text-[#879477] font-semibold uppercase text-[10px] border-b border-[#E8DDCA]">
                      <tr>
                        <th className="py-3 px-4">Date</th>
                        <th className="py-3 px-4">Role</th>
                        <th className="py-3 px-4">Difficulty</th>
                        <th className="py-3 px-4">Format</th>
                        <th className="py-3 px-4">Score</th>
                        <th className="py-3 px-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E8DDCA]">
                      {data.recent_interviews.map((itv) => (
                        <tr key={itv.id} className="hover:bg-[#FAF8F4] transition-colors">
                          <td className="py-3.5 px-4 font-medium text-[#252923]">
                            {new Date(itv.created_at).toLocaleDateString()}
                          </td>
                          <td className="py-3.5 px-4 font-semibold text-[#252923]">{itv.job_role}</td>
                          <td className="py-3.5 px-4">
                            <span className="px-2 py-0.5 rounded-full bg-[#EDF3EB] text-[#24483F] font-medium border border-[#DCE6D8]">
                              {itv.difficulty}
                            </span>
                          </td>
                          <td className="py-3.5 px-4 uppercase font-semibold text-[#24483F]">
                            {itv.mode === "mcq" ? "Multiple Choice" : "Written"}
                          </td>
                          <td className="py-3.5 px-4 font-bold text-[#252923]">
                            {itv.percentage}%
                          </td>
                          <td className="py-3.5 px-4 text-right">
                            <Link
                              href={`/interviews/${itv.id}/results`}
                              className="inline-flex items-center gap-1 text-[#24483F] hover:underline font-semibold"
                            >
                              <span>Review</span>
                              <ChevronRight className="h-3.5 w-3.5" />
                            </Link>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        ) : null}
      </div>
    </AppLayout>
  );
}
