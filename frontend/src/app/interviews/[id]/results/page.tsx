"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { Interview, Question, Answer } from "@/types";
import { 
  Award, 
  CheckCircle2, 
  XCircle, 
  Bookmark, 
  ArrowRight, 
  PlusCircle, 
  LayoutDashboard, 
  BookOpen, 
  AlertCircle, 
  Loader2,
  Check
} from "lucide-react";

function InterviewResultsContent() {
  const params = useParams();
  const router = useRouter();
  const interviewId = params.id as string;

  const [interview, setInterview] = useState<Interview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [bookmarkedIds, setBookmarkedIds] = useState<Set<number>>(new Set());
  const [savingBookmarkId, setSavingBookmarkId] = useState<number | null>(null);

  useEffect(() => {
    fetchResults();
    fetchUserBookmarks();
  }, [interviewId]);

  const fetchResults = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiRequest<Interview>(`/interviews/${interviewId}/results`);
      setInterview(data);
    } catch (err: any) {
      setError(err.message || "Failed to load interview results.");
    } finally {
      setLoading(false);
    }
  };

  const fetchUserBookmarks = async () => {
    try {
      const bms = await apiRequest<any[]>("/bookmarks");
      const ids = new Set<number>(bms.map((b) => b.question_id));
      setBookmarkedIds(ids);
    } catch (err) {
      console.warn("Could not fetch existing bookmarks:", err);
    }
  };

  const handleToggleBookmark = async (questionId: number) => {
    setSavingBookmarkId(questionId);
    const isBookmarked = bookmarkedIds.has(questionId);

    try {
      if (isBookmarked) {
        await apiRequest(`/bookmarks/${questionId}`, { method: "DELETE" });
        setBookmarkedIds((prev) => {
          const next = new Set(prev);
          next.delete(questionId);
          return next;
        });
      } else {
        await apiRequest(`/bookmarks/${questionId}`, { method: "POST" });
        setBookmarkedIds((prev) => new Set(prev).add(questionId));
      }
    } catch (err: any) {
      alert(err.message || "Bookmark action failed.");
    } finally {
      setSavingBookmarkId(null);
    }
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="py-32 flex flex-col items-center justify-center text-slate-500">
          <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
          <p className="text-xs font-semibold">Generating scorecard and analytics...</p>
        </div>
      </AppLayout>
    );
  }

  if (error || !interview) {
    return (
      <AppLayout>
        <div className="max-w-xl mx-auto py-16 text-center">
          <AlertCircle className="h-10 w-10 text-rose-500 mx-auto mb-3" />
          <h2 className="text-lg font-bold text-slate-900">Scorecard Error</h2>
          <p className="text-xs text-slate-600 mt-1">{error || "Could not retrieve score."}</p>
          <button
            onClick={() => router.push("/dashboard")}
            className="mt-6 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold"
          >
            Return to Dashboard
          </button>
        </div>
      </AppLayout>
    );
  }

  const isMCQ = interview.mode === "mcq";
  const percentage = interview.percentage || 0;
  const isPass = percentage >= 60;

  // Map answers by question_id
  const answerMap: Record<number, Answer> = {};
  interview.answers?.forEach((ans) => {
    answerMap[ans.question_id] = ans;
  });

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-16">
        {/* Scorecard Hero Banner */}
        <div className={`rounded-3xl p-6 sm:p-8 border shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6 ${
          isPass 
            ? "bg-gradient-to-br from-emerald-500/10 via-emerald-500/5 to-white border-emerald-200" 
            : "bg-gradient-to-br from-amber-500/10 via-amber-500/5 to-white border-amber-200"
        }`}>
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full ${
                isPass ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"
              }`}>
                {isPass ? "Strong Performance" : "Needs Revision"}
              </span>
              <span className="text-xs text-slate-500">
                {interview.job_role} • {interview.difficulty}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Interview Evaluation Scorecard
            </h1>

            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Completed on {new Date(interview.completed_at || interview.created_at).toLocaleDateString()} • {interview.mode.toUpperCase()} Mode
            </p>
          </div>

          <div className="flex items-center gap-4 bg-white/90 backdrop-blur-xs p-4 rounded-2xl border border-slate-200/80 shadow-xs shrink-0">
            <div className="text-center px-2">
              <p className="text-3xl sm:text-4xl font-extrabold text-slate-900">{percentage}%</p>
              <p className="text-[11px] font-semibold text-slate-400 uppercase mt-0.5">Final Score</p>
            </div>
            <div className="h-10 w-px bg-slate-200" />
            <div className="text-center px-2">
              <p className="text-xl sm:text-2xl font-bold text-indigo-600">
                {interview.total_score} <span className="text-xs font-normal text-slate-400">/ {interview.max_score}</span>
              </p>
              <p className="text-[11px] font-semibold text-slate-400 uppercase mt-0.5">Marks Earned</p>
            </div>
          </div>
        </div>

        {/* Quick Actions Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-2xl bg-white border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-600">
            Review your question-by-question breakdown and bookmark essential concepts.
          </div>

          <div className="flex items-center gap-2.5">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-semibold transition-colors"
            >
              <LayoutDashboard className="h-3.5 w-3.5" />
              <span>Dashboard</span>
            </Link>

            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-xs transition-colors"
            >
              <PlusCircle className="h-3.5 w-3.5" />
              <span>New Interview</span>
            </Link>
          </div>
        </div>

        {/* Question Breakdown List */}
        <div className="space-y-6">
          <h2 className="text-lg font-bold text-slate-900">Detailed Answer Breakdown</h2>

          {interview.questions?.map((q, idx) => {
            const ans = answerMap[q.id];
            const isBookmarked = bookmarkedIds.has(q.id);
            const isSaving = savingBookmarkId === q.id;

            return (
              <div 
                key={q.id}
                className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-5"
              >
                {/* Header: Question Number, Topic, Bookmark */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div className="flex items-center gap-2.5">
                    <span className="h-6 w-6 rounded-md bg-slate-100 text-slate-800 font-bold text-xs flex items-center justify-center">
                      {idx + 1}
                    </span>
                    <span className="text-xs font-bold text-indigo-600 uppercase tracking-wide">
                      {q.topic}
                    </span>
                  </div>

                  <button
                    type="button"
                    onClick={() => handleToggleBookmark(q.id)}
                    disabled={isSaving}
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
                      isBookmarked
                        ? "bg-amber-50 text-amber-800 border border-amber-200"
                        : "bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200"
                    }`}
                  >
                    <Bookmark className={`h-3.5 w-3.5 ${isBookmarked ? "fill-amber-600 text-amber-600" : ""}`} />
                    <span>{isSaving ? "Saving..." : isBookmarked ? "Bookmarked" : "Bookmark Question"}</span>
                  </button>
                </div>

                {/* Question Statement */}
                <p className="text-base font-bold text-slate-900 leading-snug">
                  {q.question_text}
                </p>

                {/* MCQ Mode Breakdown */}
                {isMCQ && (
                  <div className="space-y-4 pt-1">
                    {/* User's selection and correct status */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                      <div className={`p-3.5 rounded-xl border flex items-center justify-between ${
                        ans?.is_correct 
                          ? "bg-emerald-50/70 border-emerald-200 text-emerald-900" 
                          : "bg-rose-50/70 border-rose-200 text-rose-900"
                      }`}>
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Your Answer</p>
                          <p className="font-bold text-sm mt-0.5">
                            Option {ans?.selected_option || "None"}
                          </p>
                        </div>
                        {ans?.is_correct ? (
                          <div className="flex items-center gap-1 text-emerald-700 font-bold text-xs">
                            <CheckCircle2 className="h-4 w-4" />
                            <span>Correct</span>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1 text-rose-700 font-bold text-xs">
                            <XCircle className="h-4 w-4" />
                            <span>Incorrect</span>
                          </div>
                        )}
                      </div>

                      <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900">
                        <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Correct Answer</p>
                        <p className="font-bold text-sm mt-0.5 text-indigo-700">
                          Option {q.correct_option}
                        </p>
                      </div>
                    </div>

                    {/* Options list showing right and wrong */}
                    {q.options && (
                      <div className="space-y-2 pt-1">
                        {q.options.map((opt) => {
                          const isCorrectOpt = opt.key === q.correct_option;
                          const isUserOpt = opt.key === ans?.selected_option;

                          let badgeClass = "border-slate-200 bg-white text-slate-700";
                          if (isCorrectOpt) badgeClass = "border-emerald-300 bg-emerald-50/60 text-emerald-900 font-semibold";
                          else if (isUserOpt && !isCorrectOpt) badgeClass = "border-rose-300 bg-rose-50/60 text-rose-900 font-semibold";

                          return (
                            <div key={opt.key} className={`p-3 rounded-xl border text-xs flex items-center gap-3 ${badgeClass}`}>
                              <span className="h-5 w-5 rounded-md flex items-center justify-center font-bold text-[11px] bg-white border border-slate-200 shrink-0">
                                {opt.key}
                              </span>
                              <span className="flex-1">{opt.text}</span>
                              {isCorrectOpt && (
                                <span className="text-[10px] bg-emerald-600 text-white px-2 py-0.5 rounded-full font-bold shrink-0">
                                  Correct
                                </span>
                              )}
                              {isUserOpt && !isCorrectOpt && (
                                <span className="text-[10px] bg-rose-600 text-white px-2 py-0.5 rounded-full font-bold shrink-0">
                                  Your Choice
                                </span>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {/* Explanation */}
                    {q.explanation && (
                      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 text-xs text-slate-700 leading-relaxed">
                        <span className="font-bold text-slate-900 block mb-1">Explanation:</span>
                        {q.explanation}
                      </div>
                    )}
                  </div>
                )}

                {/* Text Mode Breakdown */}
                {!isMCQ && (
                  <div className="space-y-4 pt-1">
                    {/* Candidate's submitted text */}
                    <div>
                      <span className="text-[11px] font-bold uppercase text-slate-500 tracking-wider">Your Submitted Answer</span>
                      <div className="mt-1 p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 leading-relaxed whitespace-pre-line font-mono">
                        {ans?.text_answer || "No response provided."}
                      </div>
                    </div>

                    {/* Score and feedback */}
                    <div className="p-4 rounded-xl bg-indigo-50/40 border border-indigo-100 space-y-3">
                      <div className="flex items-center justify-between border-b border-indigo-100/80 pb-2">
                        <span className="text-xs font-bold text-indigo-700">AI Evaluation</span>
                        <span className="text-sm font-extrabold text-indigo-700">
                          Score: {ans?.score || 0} / 10
                        </span>
                      </div>
                      <p className="text-xs text-slate-700 leading-relaxed font-medium">
                        {ans?.feedback}
                      </p>

                      {/* Strengths & Missing Concepts */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                        {ans?.strengths && ans.strengths.length > 0 && (
                          <div className="p-3 rounded-lg bg-white border border-slate-200">
                            <span className="font-bold text-[11px] uppercase text-emerald-700 block mb-1">Strengths</span>
                            <ul className="space-y-1">
                              {ans.strengths.map((s, i) => (
                                <li key={i} className="flex items-start gap-1.5 text-slate-700">
                                  <Check className="h-3.5 w-3.5 text-emerald-600 shrink-0 mt-0.5" />
                                  <span>{s}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {ans?.missing_concepts && ans.missing_concepts.length > 0 && (
                          <div className="p-3 rounded-lg bg-white border border-slate-200">
                            <span className="font-bold text-[11px] uppercase text-amber-700 block mb-1">Missing Concepts</span>
                            <ul className="space-y-1">
                              {ans.missing_concepts.map((m, i) => (
                                <li key={i} className="flex items-start gap-1.5 text-slate-700">
                                  <AlertCircle className="h-3.5 w-3.5 text-amber-600 shrink-0 mt-0.5" />
                                  <span>{m}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Model Answer */}
                    {q.model_answer && (
                      <div>
                        <span className="text-[11px] font-bold uppercase text-slate-700 tracking-wider flex items-center gap-1.5 mb-1.5">
                          <BookOpen className="h-3.5 w-3.5 text-indigo-600" />
                          Ideal Engineering Model Answer
                        </span>
                        <div className="p-4 rounded-xl bg-white border border-slate-200 text-xs text-slate-800 leading-relaxed whitespace-pre-line font-sans">
                          {q.model_answer}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </AppLayout>
  );
}

export default function InterviewResultsPage() {
  return (
    <Suspense
      fallback={
        <AppLayout>
          <div className="py-32 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
            <p className="text-xs font-semibold">Generating scorecard and analytics...</p>
          </div>
        </AppLayout>
      }
    >
      <InterviewResultsContent />
    </Suspense>
  );
}
