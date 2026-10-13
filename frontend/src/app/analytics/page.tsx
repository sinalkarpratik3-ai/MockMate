"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { DashboardSummary } from "@/types";
import { 
  BarChart2, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle2, 
  Target, 
  FileText, 
  Award, 
  Loader2, 
  ChevronRight,
  PlusCircle
} from "lucide-react";

export default function AnalyticsPage() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await apiRequest<DashboardSummary>("/dashboard");
      setData(res);
    } catch (err: any) {
      setError(err.message || "Failed to load analytics.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="space-y-8 animate-fade-in pb-16">
        {/* Header */}
        <div className="border-b border-slate-200 pb-4">
          <div className="flex items-center gap-2 mb-1">
            <BarChart2 className="h-5 w-5 text-indigo-600" />
            <span className="text-xs font-bold text-indigo-700 uppercase tracking-widest">Performance Insights</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Progress Analytics & Mastery</h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Track metrics across engineering roles, difficulty tiers, and concept mastery.
          </p>
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
            <p className="text-xs font-medium">Computing analytics aggregates...</p>
          </div>
        ) : error || !data ? (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center justify-between">
            <span>{error || "Could not retrieve analytics."}</span>
            <button onClick={fetchAnalytics} className="font-semibold underline">Retry</button>
          </div>
        ) : (
          <>
            {/* Top Stat Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Total Interviews</span>
                <p className="text-3xl font-extrabold text-slate-900 mt-1">{data.total_interviews}</p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Total Questions</span>
                <p className="text-3xl font-extrabold text-slate-900 mt-1">{data.total_questions_attempted}</p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">MCQ Accuracy</span>
                <p className="text-3xl font-extrabold text-slate-900 mt-1">{data.mcq_accuracy_pct}%</p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Average Text Score</span>
                <p className="text-3xl font-extrabold text-slate-900 mt-1">{data.avg_text_score} / 10</p>
              </div>
            </div>

            {/* Performance Trend Points */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-slate-900">Historical Session Trend</h2>
                  <p className="text-xs text-slate-500">Score percentage progression across recent completed sessions.</p>
                </div>
              </div>

              {data.performance_trends.length === 0 ? (
                <div className="py-12 text-center text-xs text-slate-500">
                  Complete more interviews to build a trend graph.
                </div>
              ) : (
                <div className="space-y-3 pt-2">
                  <div className="flex items-end gap-2 h-40 pt-4 border-b border-slate-100">
                    {data.performance_trends.map((pt, idx) => (
                      <div key={idx} className="flex-1 flex flex-col items-center gap-1 h-full justify-end group">
                        <span className="text-[10px] font-bold text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity">
                          {pt.score_percentage}%
                        </span>
                        <div 
                          className="w-full max-w-[36px] bg-indigo-600 rounded-t-lg transition-all duration-300 group-hover:bg-indigo-700" 
                          style={{ height: `${Math.max(pt.score_percentage, 5)}%` }}
                        />
                      </div>
                    ))}
                  </div>

                  <div className="flex justify-between text-[10px] text-slate-400 px-1">
                    <span>Earlier Sessions</span>
                    <span>Recent Sessions</span>
                  </div>
                </div>
              )}
            </div>

            {/* Two Column: Role Breakdown & Weak Topics */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Role Mastery */}
              <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
                <h2 className="text-base font-bold text-slate-900">Proficiency by Role</h2>

                {data.role_stats.length === 0 ? (
                  <p className="text-xs text-slate-500 py-8 text-center">No role data available yet.</p>
                ) : (
                  <div className="space-y-4 pt-1">
                    {data.role_stats.map((r) => (
                      <div key={r.role}>
                        <div className="flex items-center justify-between text-xs mb-1.5">
                          <span className="font-semibold text-slate-800">{r.role}</span>
                          <span className="text-slate-500">{r.avg_score_pct}% Average</span>
                        </div>
                        <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
                          <div 
                            className="bg-indigo-600 h-3 rounded-full transition-all" 
                            style={{ width: `${Math.min(r.avg_score_pct, 100)}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Difficulty Breakdown */}
              <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
                <h2 className="text-base font-bold text-slate-900">Difficulty Distribution</h2>

                {data.difficulty_stats.length === 0 ? (
                  <p className="text-xs text-slate-500 py-8 text-center">No difficulty statistics recorded.</p>
                ) : (
                  <div className="space-y-4 pt-1">
                    {data.difficulty_stats.map((d) => (
                      <div key={d.difficulty}>
                        <div className="flex items-center justify-between text-xs mb-1.5">
                          <span className="font-semibold text-slate-800">{d.difficulty}</span>
                          <span className="text-slate-500">{d.count} sessions • {d.avg_score_pct}% score</span>
                        </div>
                        <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
                          <div 
                            className="bg-blue-600 h-3 rounded-full transition-all" 
                            style={{ width: `${Math.min(d.avg_score_pct, 100)}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Targeted Weak Topics List */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-rose-500" />
                <h2 className="text-base font-bold text-slate-900">Concepts Requiring Focus (&lt;60% Accuracy)</h2>
              </div>

              {data.weak_topics.length === 0 ? (
                <div className="p-8 text-center">
                  <CheckCircle2 className="h-8 w-8 text-emerald-500 mx-auto mb-2" />
                  <p className="text-sm font-semibold text-slate-800">All Topics Meeting Mastery Thresholds</p>
                  <p className="text-xs text-slate-500 mt-1">Keep taking interviews to identify further areas for improvement.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                  {data.weak_topics.map((wt) => (
                    <div 
                      key={`${wt.role}-${wt.topic}`}
                      className="p-4 rounded-xl border border-rose-200 bg-rose-50/40 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-bold text-xs text-slate-900">{wt.topic}</span>
                          <span className="text-xs font-bold text-rose-600">{wt.accuracy_percentage}%</span>
                        </div>
                        <p className="text-[11px] text-slate-600">{wt.recommendation}</p>
                      </div>

                      <div className="mt-4 pt-2 border-t border-rose-100/80 flex items-center justify-between">
                        <span className="text-[10px] text-slate-400">{wt.attempts} attempts recorded</span>
                        <Link
                          href={`/interviews/new?role=${encodeURIComponent(wt.role)}`}
                          className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 inline-flex items-center gap-1"
                        >
                          <span>Practice Topic</span>
                          <ChevronRight className="h-3 w-3" />
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </AppLayout>
  );
}
