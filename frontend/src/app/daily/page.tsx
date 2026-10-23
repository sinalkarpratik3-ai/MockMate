"use client";

import React, { useState, useEffect, useCallback } from "react";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { DailyQuestion } from "@/types";
import { 
  Calendar, 
  CheckCircle2, 
  XCircle, 
  Send, 
  Loader2, 
  Award,
  BookOpen,
  Bookmark
} from "lucide-react";

export default function DailyQuestionPage() {
  const [data, setData] = useState<DailyQuestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedOption, setSelectedOption] = useState<string>("");
  const [textAnswer, setTextAnswer] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [savingBookmark, setSavingBookmark] = useState(false);

  const fetchDailyQuestion = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await apiRequest<DailyQuestion>("/daily");
      setData(res);
      setIsBookmarked(Boolean(res.is_bookmarked));
      if (res.user_attempt) {
        if (res.question_type === "mcq") {
          setSelectedOption(res.user_attempt.submitted_answer);
        } else {
          setTextAnswer(res.user_attempt.submitted_answer);
        }
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load today's question.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let ignore = false;
    apiRequest<DailyQuestion>("/daily")
      .then((res) => {
        if (!ignore) {
          setData(res);
          setIsBookmarked(Boolean(res.is_bookmarked));
          if (res.user_attempt) {
            if (res.question_type === "mcq") {
              setSelectedOption(res.user_attempt.submitted_answer);
            } else {
              setTextAnswer(res.user_attempt.submitted_answer);
            }
          }
        }
      })
      .catch((err: unknown) => {
        if (!ignore) {
          const msg = err instanceof Error ? err.message : "Failed to load today's question.";
          setError(msg);
        }
      })
      .finally(() => {
        if (!ignore) {
          setLoading(false);
        }
      });
    return () => {
      ignore = true;
    };
  }, []);

  const handleToggleBookmark = async () => {
    if (!data?.question_id) return;
    setSavingBookmark(true);
    try {
      if (isBookmarked) {
        await apiRequest(`/bookmarks/${data.question_id}`, { method: "DELETE" });
        setIsBookmarked(false);
      } else {
        await apiRequest(`/bookmarks/${data.question_id}`, { method: "POST" });
        setIsBookmarked(true);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to toggle bookmark.";
      alert(msg);
    } finally {
      setSavingBookmark(false);
    }
  };

  const handleSubmit = async () => {
    if (!data) return;
    const answerToSubmit = data.question_type === "mcq" ? selectedOption : textAnswer;

    if (!answerToSubmit.trim()) {
      alert("Please select or write an answer before submitting.");
      return;
    }

    setSubmitting(true);
    try {
      const res = await apiRequest<NonNullable<DailyQuestion["user_attempt"]>>("/daily/attempt", {
        method: "POST",
        body: JSON.stringify({ submitted_answer: answerToSubmit }),
      });

      setData((prev) => prev ? {
        ...prev,
        has_attempted: true,
        user_attempt: res,
      } : null);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Submission failed.";
      alert(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AppLayout>
      <div className="max-w-3xl mx-auto space-y-6 animate-fade-in pb-16">
        {/* Header */}
        <div className="border-b border-[#E8DDCA] pb-4">
          <div className="flex items-center gap-2 mb-1">
            <Calendar className="h-5 w-5 text-[#C66A4A]" />
            <span className="text-xs font-bold text-[#C66A4A] uppercase tracking-widest">Daily Practice Habit</span>
          </div>
          <h1 className="text-2xl font-bold text-[#252923] tracking-tight">Question of the Day</h1>
          <p className="text-xs sm:text-sm text-[#777B74] mt-1">
            Build consistent technical intuition. Every day features a distinct question to keep problem-solving fresh.
          </p>
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-medium">Fetching today&apos;s challenge...</p>
          </div>
        ) : error || !data ? (
          <div className="p-4 rounded-xl bg-[#FDF1F0] border border-[#E8DDCA] text-[#B8473F] text-xs flex items-center justify-between">
            <span>{error || "Could not retrieve question."}</span>
            <button onClick={fetchDailyQuestion} className="font-semibold underline">Retry</button>
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 sm:p-8 shadow-xs space-y-6">
            {/* Meta Tags */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#E8DDCA] pb-4">
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-[#FAF8F4] text-[#252923] border border-[#E8DDCA]">
                  {new Date(data.date).toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" })}
                </span>
                <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-[#EDF3EB] text-[#24483F] border border-[#DCE6D8]">
                  {data.role}
                </span>
                <span className="text-xs font-bold text-[#879477]">
                  Topic: {data.topic}
                </span>
              </div>

              <div className="flex items-center gap-2">
                {data.question_id && (
                  <button
                    type="button"
                    onClick={handleToggleBookmark}
                    disabled={savingBookmark}
                    className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
                      isBookmarked
                        ? "bg-[#F7ECE7] text-[#C66A4A] border border-[#E8DDCA]"
                        : "bg-[#FAF8F4] text-[#252923] hover:bg-[#EDF3EB] border border-[#E8DDCA]"
                    }`}
                    title="Bookmark today's question for revision"
                  >
                    <Bookmark className={`h-3.5 w-3.5 ${isBookmarked ? "fill-[#C66A4A] text-[#C66A4A]" : "text-[#879477]"}`} />
                    <span>{savingBookmark ? "Saving..." : isBookmarked ? "Saved" : "Save Question"}</span>
                  </button>
                )}

                {data.has_attempted && (
                  <span className="text-xs font-bold text-[#367451] bg-[#EDF3EB] border border-[#DCE6D8] px-2.5 py-1 rounded-full flex items-center gap-1">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Completed Today
                  </span>
                )}
              </div>
            </div>

            {/* Question Statement */}
            <h2 className="text-lg font-bold text-[#252923] leading-snug">
              {data.question_text}
            </h2>

            {/* MCQ Options */}
            {data.question_type === "mcq" && data.options && (
              <div className="space-y-3 pt-2">
                {data.options.map((opt) => {
                  const isSelected = selectedOption === opt.key;
                  const isDisabled = data.has_attempted;

                  return (
                    <button
                      key={opt.key}
                      type="button"
                      disabled={isDisabled}
                      onClick={() => setSelectedOption(opt.key)}
                      className={`w-full p-4 rounded-xl border text-left transition-all flex items-center gap-3.5 ${
                        isSelected
                          ? "border-[#24483F] bg-[#EDF3EB] shadow-xs ring-1 ring-[#24483F]"
                          : "border-[#E8DDCA] bg-white hover:border-[#DCE6D8] hover:bg-[#FAF8F4]"
                      } ${isDisabled ? "cursor-default" : ""}`}
                    >
                      <div className={`h-7 w-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                        isSelected ? "bg-[#24483F] text-[#F7F3EA]" : "bg-[#FAF8F4] text-[#252923] border border-[#E8DDCA]"
                      }`}>
                        {opt.key}
                      </div>
                      <span className="text-xs sm:text-sm font-medium text-[#252923] leading-relaxed">
                        {opt.text}
                      </span>
                    </button>
                  );
                })}
              </div>
            )}

            {/* Text Input Mode */}
            {data.question_type === "text" && (
              <div className="space-y-3 pt-2">
                <textarea
                  rows={6}
                  value={textAnswer}
                  onChange={(e) => setTextAnswer(e.target.value)}
                  disabled={data.has_attempted}
                  placeholder="Explain the mechanism, trade-offs, and examples in your own words..."
                  className="w-full p-4 rounded-xl border border-[#E8DDCA] text-sm text-[#252923] placeholder:text-[#879477] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F] font-mono leading-relaxed bg-[#FAF8F4] focus:bg-white"
                />
              </div>
            )}

            {/* Submit Button (if not attempted) */}
            {!data.has_attempted && (
              <div className="pt-2">
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={submitting}
                  className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] font-semibold text-sm shadow-sm transition-all disabled:opacity-60"
                >
                  {submitting ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Saving your answer...</span>
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4" />
                      <span>Submit Today&apos;s Answer</span>
                    </>
                  )}
                </button>
              </div>
            )}

            {/* Results / Feedback if attempted */}
            {data.has_attempted && data.user_attempt && (
              <div className="mt-6 p-5 rounded-2xl bg-[#FAF8F4] border border-[#E8DDCA] space-y-4 animate-in fade-in">
                <div className="flex items-center justify-between border-b border-[#E8DDCA] pb-3">
                  <div className="flex items-center gap-2">
                    <Award className="h-5 w-5 text-[#24483F]" />
                    <span className="font-bold text-sm text-[#252923]">Your Daily Result</span>
                  </div>
                  <div>
                    {data.user_attempt.is_correct ? (
                      <span className="text-xs font-bold text-[#367451] bg-[#EDF3EB] border border-[#DCE6D8] px-2.5 py-0.5 rounded-full flex items-center gap-1">
                        <CheckCircle2 className="h-3.5 w-3.5" />
                        Correct
                      </span>
                    ) : (
                      <span className="text-xs font-bold text-[#B8473F] bg-[#FDF1F0] border border-[#E8DDCA] px-2.5 py-0.5 rounded-full flex items-center gap-1">
                        <XCircle className="h-3.5 w-3.5" />
                        Incorrect
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-xs text-[#252923] leading-relaxed">
                  {data.user_attempt.feedback}
                </p>

                {data.user_attempt.explanation && (
                  <div className="p-3.5 rounded-xl bg-white border border-[#E8DDCA] text-xs text-[#252923]">
                    <strong className="text-[#24483F] block mb-1">
                      Correct Answer: Option {data.user_attempt.correct_option}
                    </strong>
                    <p className="text-[#777B74]">{data.user_attempt.explanation}</p>
                  </div>
                )}

                {data.user_attempt.model_answer && (
                  <div className="p-3.5 rounded-xl bg-white border border-[#E8DDCA] text-xs text-[#252923]">
                    <strong className="text-[#24483F] block mb-1 flex items-center gap-1.5">
                      <BookOpen className="h-3.5 w-3.5 text-[#24483F]" />
                      Sample Answer:
                    </strong>
                    <p className="whitespace-pre-line text-[#777B74]">{data.user_attempt.model_answer}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </AppLayout>
  );
}
