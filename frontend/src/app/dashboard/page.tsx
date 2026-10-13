"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { useAuth } from "@/context/AuthContext";
import { apiRequest } from "@/lib/api";
import { DashboardSummary } from "@/types";
import { 
  CheckCircle, 
  HelpCircle, 
  Target, 
  FileText, 
  PlusCircle, 
  Calendar, 
  Bookmark, 
  ArrowRight, 
  AlertTriangle, 
  TrendingUp, 
  Loader2,
  ChevronRight,
  Sparkles,
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
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Welcome back, {user?.full_name || user?.email.split("@")[0]}
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Here is your verified technical interview preparation trajectory.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs sm:text-sm shadow-sm shadow-indigo-600/20 transition-all"
            >
              <PlusCircle className="h-4 w-4" />
              <span>Start New Interview</span>
            </Link>
          </div>
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
            <p className="text-xs font-medium">Aggregating database statistics...</p>
          </div>
        ) : error ? (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center justify-between">
            <span>{error}</span>
            <button
              onClick={fetchDashboard}
              className="font-semibold underline hover:text-rose-800"
            >
              Retry
            </button>
          </div>
        ) : data ? (
          <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
              {/* Total Interviews */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Completed Interviews</p>
                  <p className="text-3xl font-extrabold text-slate-900 mt-1">{data.total_interviews}</p>
                  <p className="text-[11px] text-slate-400 mt-1">Full sessions completed</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
                  <Award className="h-6 w-6" />
                </div>
              </div>

              {/* Questions Attempted */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Questions Solved</p>
                  <p className="text-3xl font-extrabold text-slate-900 mt-1">{data.total_questions_attempted}</p>
                  <p className="text-[11px] text-slate-400 mt-1">Across all roles</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600">
                  <CheckCircle className="h-6 w-6" />
                </div>
              </div>

              {/* MCQ Accuracy */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">MCQ Accuracy</p>
                  <p className="text-3xl font-extrabold text-slate-900 mt-1">
                    {data.mcq_accuracy_pct}%
                  </p>
                  <p className="text-[11px] text-slate-400 mt-1">Deterministic score</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600">
                  <Target className="h-6 w-6" />
                </div>
              </div>

              {/* Average Text Score */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Text Score</p>
                  <p className="text-3xl font-extrabold text-slate-900 mt-1">
                    {data.avg_text_score} <span className="text-sm font-normal text-slate-400">/ 10</span>
                  </p>
                  <p className="text-[11px] text-slate-400 mt-1">AI Rubric evaluation</p>
                </div>
                <div className="h-12 w-12 rounded-xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600">
                  <FileText className="h-6 w-6" />
                </div>
              </div>
            </div>

            {/* Daily Question Callout */}
            <div className="bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-indigo-500/10 border border-amber-200/80 rounded-2xl p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="flex items-start sm:items-center gap-3.5">
                <div className="h-10 w-10 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0 shadow-sm shadow-amber-500/20">
                  <Calendar className="h-5 w-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-amber-800">Question of the Day</span>
                    {data.has_attempted_daily ? (
                      <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full">
                        Completed
                      </span>
                    ) : (
                      <span className="text-[10px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded-full">
                        Pending
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-600 mt-0.5">
                    {data.has_attempted_daily 
                      ? "Great job! You have completed today's technical challenge." 
                      : "Strengthen your daily habit with today's featured technical question."}
                  </p>
                </div>
              </div>

              <Link
                href="/daily"
                className="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-800 hover:text-indigo-600 hover:border-indigo-200 text-xs font-semibold shadow-xs transition-colors shrink-0"
              >
                <span>{data.has_attempted_daily ? "Review Daily Answer" : "Solve Daily Challenge"}</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>

            {/* Two Column Section: Weak Topics & Role Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Weak Topics */}
              <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5 text-rose-500" />
                    <h2 className="text-base font-bold text-slate-900">Weak Topics Identified</h2>
                  </div>
                  <span className="text-xs text-slate-400">Score &lt; 60%</span>
                </div>

                {data.weak_topics.length === 0 ? (
                  <div className="py-10 text-center my-auto">
                    <CheckCircle className="h-8 w-8 text-emerald-500 mx-auto mb-2 opacity-80" />
                    <p className="text-sm font-semibold text-slate-800">No Consistently Weak Topics</p>
                    <p className="text-xs text-slate-500 mt-1 max-w-xs mx-auto">
                      All attempted topics have maintained &gt;=60% performance. Keep challenging yourself!
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3 flex-1">
                    {data.weak_topics.map((wt) => (
                      <div 
                        key={`${wt.role}-${wt.topic}`} 
                        className="p-3.5 rounded-xl border border-rose-100 bg-rose-50/40 flex items-center justify-between gap-3"
                      >
                        <div className="min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-xs text-slate-900 truncate">{wt.topic}</span>
                            <span className="text-[10px] bg-slate-200/80 text-slate-700 px-1.5 py-0.5 rounded font-medium">
                              {wt.role}
                            </span>
                          </div>
                          <p className="text-[11px] text-slate-500 mt-0.5">
                            Accuracy: <span className="font-bold text-rose-600">{wt.accuracy_percentage}%</span> ({wt.attempts} attempts)
                          </p>
                        </div>

                        <Link
                          href={`/interviews/new?role=${encodeURIComponent(wt.role)}`}
                          className="shrink-0 text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 bg-white border border-slate-200 px-2.5 py-1 rounded-lg transition-colors"
                        >
                          Practice
                        </Link>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Role Performance */}
              <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-indigo-600" />
                    <h2 className="text-base font-bold text-slate-900">Performance by Job Role</h2>
                  </div>
                  <Link href="/analytics" className="text-xs font-semibold text-indigo-600 hover:underline">
                    View Analytics
                  </Link>
                </div>

                {data.role_stats.length === 0 ? (
                  <div className="py-10 text-center my-auto">
                    <p className="text-sm font-semibold text-slate-800">No Role Data Yet</p>
                    <p className="text-xs text-slate-500 mt-1">Complete your first interview to see role proficiency breakdown.</p>
                  </div>
                ) : (
                  <div className="space-y-4 flex-1">
                    {data.role_stats.map((rs) => (
                      <div key={rs.role}>
                        <div className="flex items-center justify-between text-xs mb-1.5">
                          <span className="font-semibold text-slate-800">{rs.role}</span>
                          <span className="text-slate-500">{rs.interviews_count} interviews • <strong className="text-indigo-600">{rs.avg_score_pct}%</strong> avg</span>
                        </div>
                        <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                          <div 
                            className="bg-indigo-600 h-2.5 rounded-full transition-all duration-500" 
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
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-base font-bold text-slate-900">Recent Completed Interviews</h2>
                <Link href="/history" className="text-xs font-semibold text-indigo-600 hover:underline">
                  All History
                </Link>
              </div>

              {data.recent_interviews.length === 0 ? (
                <div className="py-12 text-center">
                  <p className="text-sm font-semibold text-slate-800">No interviews completed yet</p>
                  <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                    Configure your first simulation to start recording scores and personalized feedback.
                  </p>
                  <Link
                    href="/interviews/new"
                    className="inline-flex items-center gap-1.5 mt-4 px-4 py-2 rounded-xl bg-indigo-600 text-white font-semibold text-xs shadow-sm hover:bg-indigo-700 transition-colors"
                  >
                    <PlusCircle className="h-3.5 w-3.5" />
                    <span>Start First Interview</span>
                  </Link>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-600">
                    <thead className="bg-slate-50 text-slate-400 font-semibold uppercase text-[10px] border-b border-slate-100">
                      <tr>
                        <th className="py-3 px-4">Date</th>
                        <th className="py-3 px-4">Job Role</th>
                        <th className="py-3 px-4">Difficulty</th>
                        <th className="py-3 px-4">Mode</th>
                        <th className="py-3 px-4">Score</th>
                        <th className="py-3 px-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {data.recent_interviews.map((itv) => (
                        <tr key={itv.id} className="hover:bg-slate-50/60 transition-colors">
                          <td className="py-3.5 px-4 font-medium text-slate-900">
                            {new Date(itv.created_at).toLocaleDateString()}
                          </td>
                          <td className="py-3.5 px-4 font-semibold text-slate-800">{itv.job_role}</td>
                          <td className="py-3.5 px-4">
                            <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium">
                              {itv.difficulty}
                            </span>
                          </td>
                          <td className="py-3.5 px-4 uppercase font-semibold text-indigo-600">{itv.mode}</td>
                          <td className="py-3.5 px-4 font-bold text-slate-900">
                            {itv.percentage}%
                          </td>
                          <td className="py-3.5 px-4 text-right">
                            <Link
                              href={`/interviews/${itv.id}/results`}
                              className="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-800 font-semibold"
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
