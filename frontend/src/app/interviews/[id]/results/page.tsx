"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { Interview, Answer } from "@/types";
import { 
  CheckCircle2, 
  XCircle, 
  Bookmark, 
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
      setError(err.message || "Failed to load practice results.");
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
        <div className="py-32 flex flex-col items-center justify-center text-[#777B74]">
          <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
          <p className="text-xs font-semibold">Preparing your results summary...</p>
        </div>
      </AppLayout>
    );
  }

  if (error || !interview) {
    return (
      <AppLayout>
        <div className="max-w-xl mx-auto py-16 text-center">
          <AlertCircle className="h-10 w-10 text-[#B8473F] mx-auto mb-3" />
          <h2 className="text-lg font-bold text-[#252923]">Results Notice</h2>
          <p className="text-xs text-[#777B74] mt-1">{error || "Could not retrieve results."}</p>
          <button
            onClick={() => router.push("/dashboard")}
            className="mt-6 px-4 py-2 rounded-xl bg-[#24483F] text-[#F7F3EA] text-xs font-semibold hover:bg-[#1A342D]"
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
        <div className="rounded-3xl p-6 sm:p-8 border border-[#E8DDCA] bg-[#FAF8F4] shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${
                isPass 
                  ? "bg-[#EDF3EB] text-[#367451] border-[#DCE6D8]" 
                  : "bg-[#F7ECE7] text-[#C66A4A] border-[#E8DDCA]"
              }`}>
                {isPass ? "Solid Performance" : "Needs Revision"}
              </span>
              <span className="text-xs text-[#777B74]">
                {interview.job_role} • {interview.difficulty}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-[#252923] tracking-tight">
              Interview Results & Review
            </h1>

            <p className="text-xs sm:text-sm text-[#777B74] mt-1">
              Completed on {new Date(interview.completed_at || interview.created_at).toLocaleDateString()} • {isMCQ ? "Multiple Choice" : "Written Answers"}
            </p>
          </div>

          <div className="flex items-center gap-4 bg-white p-4 rounded-2xl border border-[#E8DDCA] shadow-xs shrink-0">
            <div className="text-center px-2">
              <p className="text-3xl sm:text-4xl font-extrabold text-[#252923]">{percentage}%</p>
              <p className="text-[11px] font-semibold text-[#879477] uppercase mt-0.5">Final Score</p>
            </div>
            <div className="h-10 w-px bg-[#E8DDCA]" />
            <div className="text-center px-2">
              <p className="text-xl sm:text-2xl font-bold text-[#24483F]">
                {interview.total_score} <span className="text-xs font-normal text-[#879477]">/ {interview.max_score}</span>
              </p>
              <p className="text-[11px] font-semibold text-[#879477] uppercase mt-0.5">Points Earned</p>
            </div>
          </div>
        </div>

        {/* Quick Actions Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-2xl bg-white border border-[#E8DDCA] shadow-xs">
          <div className="text-xs font-medium text-[#777B74]">
            Review your question-by-question breakdown and save concepts for later revision.
          </div>

          <div className="flex items-center gap-2.5">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-[#E8DDCA] text-[#252923] hover:bg-[#FAF8F4] text-xs font-semibold transition-colors"
            >
              <LayoutDashboard className="h-3.5 w-3.5" />
              <span>Dashboard</span>
            </Link>

            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] text-xs font-semibold shadow-xs transition-colors"
            >
              <PlusCircle className="h-3.5 w-3.5" />
              <span>Start Another Practice Test</span>
            </Link>
          </div>
        </div>

        {/* Question Breakdown List */}
        <div className="space-y-6">
          <h2 className="text-lg font-bold text-[#252923]">Detailed Answer Review</h2>

          {interview.questions?.map((q, idx) => {
            const ans = answerMap[q.id];
            const isBookmarked = bookmarkedIds.has(q.id);
            const isSaving = savingBookmarkId === q.id;

            return (
              <div 
                key={q.id}
                className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs space-y-5"
              >
                {/* Header: Question Number, Topic, Bookmark */}
                <div className="flex items-center justify-between border-b border-[#E8DDCA] pb-3">
                  <div className="flex items-center gap-2.5">
                    <span className="h-6 w-6 rounded-md bg-[#EDF3EB] text-[#24483F] border border-[#DCE6D8] font-bold text-xs flex items-center justify-center">
                      {idx + 1}
                    </span>
                    <span className="text-xs font-bold text-[#879477] uppercase tracking-wide">
                      {q.topic}
                    </span>
                  </div>

                  <button
                    type="button"
                    onClick={() => handleToggleBookmark(q.id)}
                    disabled={isSaving}
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
                      isBookmarked
                        ? "bg-[#F7ECE7] text-[#C66A4A] border border-[#E8DDCA]"
                        : "bg-[#FAF8F4] text-[#252923] hover:bg-[#EDF3EB] border border-[#E8DDCA]"
                    }`}
                  >
                    <Bookmark className={`h-3.5 w-3.5 ${isBookmarked ? "fill-[#C66A4A] text-[#C66A4A]" : "text-[#879477]"}`} />
                    <span>{isSaving ? "Saving..." : isBookmarked ? "Saved" : "Save Question"}</span>
                  </button>
                </div>

                {/* Question Statement */}
                <p className="text-base font-bold text-[#252923] leading-snug">
                  {q.question_text}
                </p>

                {/* MCQ Mode Breakdown */}
                {isMCQ && (
                  <div className="space-y-4 pt-1">
                    {/* User's selection and correct status */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                      <div className={`p-3.5 rounded-xl border flex items-center justify-between ${
                        ans?.is_correct 
                          ? "bg-[#EDF3EB] border-[#DCE6D8] text-[#252923]" 
                          : "bg-[#FDF1F0] border-[#E8DDCA] text-[#252923]"
                      }`}>
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-wider text-[#879477]">Your Answer</p>
                          <p className="font-bold text-sm mt-0.5">
                            Option {ans?.selected_option || "None"}
                          </p>
                        </div>
                        {ans?.is_correct ? (
                          <div className="flex items-center gap-1 text-[#367451] font-bold text-xs">
                            <CheckCircle2 className="h-4 w-4" />
                            <span>Correct</span>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1 text-[#B8473F] font-bold text-xs">
                            <XCircle className="h-4 w-4" />
                            <span>Incorrect</span>
                          </div>
                        )}
                      </div>

                      <div className="p-3.5 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] text-[#252923]">
                        <p className="text-[10px] font-bold uppercase tracking-wider text-[#879477]">Correct Answer</p>
                        <p className="font-bold text-sm mt-0.5 text-[#24483F]">
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

                          let badgeClass = "border-[#E8DDCA] bg-white text-[#252923]";
                          if (isCorrectOpt) badgeClass = "border-[#DCE6D8] bg-[#EDF3EB] text-[#252923] font-semibold";
                          else if (isUserOpt && !isCorrectOpt) badgeClass = "border-[#E8DDCA] bg-[#FDF1F0] text-[#252923] font-semibold";

                          return (
                            <div key={opt.key} className={`p-3 rounded-xl border text-xs flex items-center gap-3 ${badgeClass}`}>
                              <span className="h-5 w-5 rounded-md flex items-center justify-center font-bold text-[11px] bg-white border border-[#E8DDCA] shrink-0">
                                {opt.key}
                              </span>
                              <span className="flex-1">{opt.text}</span>
                              {isCorrectOpt && (
                                <span className="text-[10px] bg-[#367451] text-white px-2 py-0.5 rounded-full font-bold shrink-0">
                                  Correct
                                </span>
                              )}
                              {isUserOpt && !isCorrectOpt && (
                                <span className="text-[10px] bg-[#B8473F] text-white px-2 py-0.5 rounded-full font-bold shrink-0">
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
                      <div className="p-4 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] text-xs text-[#252923] leading-relaxed">
                        <span className="font-bold text-[#24483F] block mb-1">Explanation:</span>
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
                      <span className="text-[11px] font-bold uppercase text-[#879477] tracking-wider">Your Submitted Answer</span>
                      <div className="mt-1 p-4 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] text-xs text-[#252923] leading-relaxed whitespace-pre-line font-mono">
                        {ans?.text_answer || "No response provided."}
                      </div>
                    </div>

                    {/* Score and feedback */}
                    <div className="p-4 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] space-y-3">
                      <div className="flex items-center justify-between border-b border-[#E8DDCA] pb-2">
                        <span className="text-xs font-bold text-[#24483F]">Answer Review</span>
                        <span className="text-sm font-extrabold text-[#24483F]">
                          Score: {ans?.score || 0} / 10
                        </span>
                      </div>
                      <p className="text-xs text-[#252923] leading-relaxed font-medium">
                        {ans?.feedback}
                      </p>

                      {/* Strengths & Missing Concepts */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                        {ans?.strengths && ans.strengths.length > 0 && (
                          <div className="p-3 rounded-lg bg-white border border-[#E8DDCA]">
                            <span className="font-bold text-[11px] uppercase text-[#367451] block mb-1">What You Did Well</span>
                            <ul className="space-y-1">
                              {ans.strengths.map((s, i) => (
                                <li key={i} className="flex items-start gap-1.5 text-[#252923]">
                                  <Check className="h-3.5 w-3.5 text-[#367451] shrink-0 mt-0.5" />
                                  <span>{s}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {ans?.missing_concepts && ans.missing_concepts.length > 0 && (
                          <div className="p-3 rounded-lg bg-white border border-[#E8DDCA]">
                            <span className="font-bold text-[11px] uppercase text-[#C66A4A] block mb-1">Key Concepts to Review</span>
                            <ul className="space-y-1">
                              {ans.missing_concepts.map((m, i) => (
                                <li key={i} className="flex items-start gap-1.5 text-[#252923]">
                                  <AlertCircle className="h-3.5 w-3.5 text-[#C66A4A] shrink-0 mt-0.5" />
                                  <span>{m}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Sample Answer */}
                    {q.model_answer && (
                      <div>
                        <span className="text-[11px] font-bold uppercase text-[#252923] tracking-wider flex items-center gap-1.5 mb-1.5">
                          <BookOpen className="h-3.5 w-3.5 text-[#24483F]" />
                          Sample Answer
                        </span>
                        <div className="p-4 rounded-xl bg-white border border-[#E8DDCA] text-xs text-[#252923] leading-relaxed whitespace-pre-line font-sans">
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
          <div className="py-32 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-semibold">Preparing your results summary...</p>
          </div>
        </AppLayout>
      }
    >
      <InterviewResultsContent />
    </Suspense>
  );
}
