"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { DashboardSummary } from "@/types";
import { 
  BarChart2, 
  AlertTriangle, 
  CheckCircle2, 
  Loader2, 
  ChevronRight
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
      setError(err.message || "Failed to load progress metrics.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="space-y-8 animate-fade-in pb-16">
        {/* Header */}
        <div className="border-b border-[#E8DDCA] pb-4">
          <div className="flex items-center gap-2 mb-1">
            <BarChart2 className="h-5 w-5 text-[#24483F]" />
            <span className="text-xs font-bold text-[#879477] uppercase tracking-widest">Performance Insights</span>
          </div>
          <h1 className="text-2xl font-bold text-[#252923] tracking-tight">Your Progress</h1>
          <p className="text-xs sm:text-sm text-[#777B74] mt-1">
            Track metrics across engineering roles, difficulty levels, and concept mastery.
          </p>
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-medium">Computing your progress metrics...</p>
          </div>
        ) : error || !data ? (
          <div className="p-4 rounded-xl bg-[#FDF1F0] border border-[#E8DDCA] text-[#B8473F] text-xs flex items-center justify-between">
            <span>{error || "Could not retrieve progress metrics."}</span>
            <button onClick={fetchAnalytics} className="font-semibold underline">Retry</button>
          </div>
        ) : (
          <>
            {/* Top Stat Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-5 rounded-2xl bg-white border border-[#E8DDCA] shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#879477]">Completed Sessions</span>
                <p className="text-3xl font-extrabold text-[#252923] mt-1">{data.total_interviews}</p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-[#E8DDCA] shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#879477]">Questions Practised</span>
                <p className="text-3xl font-extrabold text-[#252923] mt-1">{data.total_questions_attempted}</p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-[#E8DDCA] shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#879477]">MCQ Accuracy</span>
                <p className="text-3xl font-extrabold text-[#252923] mt-1">{data.mcq_accuracy_pct}%</p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-[#E8DDCA] shadow-xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#879477]">Average Written Score</span>
                <p className="text-3xl font-extrabold text-[#252923] mt-1">{data.avg_text_score} / 10</p>
              </div>
            </div>

            {/* Performance Trend Points */}
            <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-base font-bold text-[#252923]">Performance Trend</h2>
                  <p className="text-xs text-[#777B74]">Score percentage progression across recent completed sessions.</p>
                </div>
              </div>

              {data.performance_trends.length === 0 ? (
                <div className="py-12 text-center text-xs text-[#777B74]">
                  Complete more sessions to build a performance trend graph.
                </div>
              ) : (
                <div className="space-y-3 pt-2">
                  <div className="flex items-end gap-2 h-40 pt-4 border-b border-[#E8DDCA]">
                    {data.performance_trends.map((pt, idx) => (
                      <div key={idx} className="flex-1 flex flex-col items-center gap-1 h-full justify-end group relative">
                        <div className="absolute -top-12 z-20 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity bg-[#252923] text-white text-[10px] px-2.5 py-1 rounded-lg shadow-md whitespace-nowrap text-center border border-[#3D443A]">
                          <p className="font-bold">{pt.score_percentage}% • {pt.role}</p>
                          <p className="text-[9px] text-[#DCE6D8]">{pt.date} ({pt.mode === "mcq" ? "Multiple Choice" : "Written"})</p>
                        </div>
                        <span className="text-[10px] font-bold text-[#252923] opacity-0 group-hover:opacity-100 transition-opacity">
                          {pt.score_percentage}%
                        </span>
                        <div 
                          className="w-full max-w-[36px] bg-[#24483F] rounded-t-lg transition-all duration-300 group-hover:bg-[#1A342D] cursor-pointer" 
                          style={{ height: `${Math.max(pt.score_percentage, 5)}%` }}
                        />
                      </div>
                    ))}
                  </div>

                  <div className="flex justify-between text-[10px] text-[#879477] px-1">
                    <span>Earlier Sessions</span>
                    <span>Recent Sessions</span>
                  </div>
                </div>
              )}
            </div>

            {/* Two Column: Role Breakdown & Difficulty Distribution */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Role Mastery */}
              <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs space-y-4">
                <h2 className="text-base font-bold text-[#252923]">Proficiency by Role</h2>

                {data.role_stats.length === 0 ? (
                  <p className="text-xs text-[#777B74] py-8 text-center">No role data available yet.</p>
                ) : (
                  <div className="space-y-4 pt-1">
                    {data.role_stats.map((r) => (
                      <div key={r.role}>
                        <div className="flex items-center justify-between text-xs mb-1.5">
                          <span className="font-semibold text-[#252923]">{r.role}</span>
                          <span className="text-[#777B74]">{r.avg_score_pct}% Average</span>
                        </div>
                        <div className="w-full bg-[#FAF8F4] border border-[#E8DDCA] rounded-full h-3 overflow-hidden">
                          <div 
                            className="bg-[#24483F] h-3 rounded-full transition-all" 
                            style={{ width: `${Math.min(r.avg_score_pct, 100)}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Difficulty Breakdown */}
              <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs space-y-4">
                <h2 className="text-base font-bold text-[#252923]">Difficulty Distribution</h2>

                {data.difficulty_stats.length === 0 ? (
                  <p className="text-xs text-[#777B74] py-8 text-center">No difficulty statistics recorded.</p>
                ) : (
                  <div className="space-y-4 pt-1">
                    {data.difficulty_stats.map((d) => (
                      <div key={d.difficulty}>
                        <div className="flex items-center justify-between text-xs mb-1.5">
                          <span className="font-semibold text-[#252923]">{d.difficulty}</span>
                          <span className="text-[#777B74]">{d.count} sessions • {d.avg_score_pct}% score</span>
                        </div>
                        <div className="w-full bg-[#FAF8F4] border border-[#E8DDCA] rounded-full h-3 overflow-hidden">
                          <div 
                            className="bg-[#879477] h-3 rounded-full transition-all" 
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
            <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs space-y-4">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-[#C66A4A]" />
                <h2 className="text-base font-bold text-[#252923]">Topics to Revisit (&lt;60% Accuracy)</h2>
              </div>

              {data.weak_topics.length === 0 ? (
                <div className="p-8 text-center">
                  <CheckCircle2 className="h-8 w-8 text-[#367451] mx-auto mb-2" />
                  <p className="text-sm font-semibold text-[#252923]">All Topics Meeting Mastery Thresholds</p>
                  <p className="text-xs text-[#777B74] mt-1">Keep practising to identify further areas for improvement.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                  {data.weak_topics.map((wt) => (
                    <div 
                      key={`${wt.role}-${wt.topic}`} 
                      className="p-4 rounded-xl border border-[#E8DDCA] bg-[#FAF8F4] flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-bold text-xs text-[#252923]">{wt.topic}</span>
                          <span className="text-xs font-bold text-[#C66A4A]">{wt.accuracy_percentage}%</span>
                        </div>
                        <p className="text-[11px] text-[#777B74]">{wt.recommendation}</p>
                      </div>

                      <div className="mt-4 pt-2 border-t border-[#E8DDCA] flex items-center justify-between">
                        <span className="text-[10px] text-[#879477]">{wt.attempts} attempts recorded</span>
                        <Link
                          href={`/interviews/new?role=${encodeURIComponent(wt.role)}`}
                          className="text-xs font-semibold text-[#24483F] hover:underline inline-flex items-center gap-1"
                        >
                          <span>Practise Topic</span>
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
