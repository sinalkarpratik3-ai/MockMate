"use client";

import React, { useState, useEffect } from "react";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { DailyQuestion } from "@/types";
import { 
  Calendar, 
  CheckCircle2, 
  XCircle, 
  Send, 
  Loader2, 
  AlertCircle, 
  Award,
  Sparkles,
  BookOpen
} from "lucide-react";

export default function DailyQuestionPage() {
  const [data, setData] = useState<DailyQuestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedOption, setSelectedOption] = useState<string>("");
  const [textAnswer, setTextAnswer] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchDailyQuestion();
  }, []);

  const fetchDailyQuestion = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await apiRequest<DailyQuestion>("/daily");
      setData(res);
      if (res.user_attempt) {
        if (res.question_type === "mcq") {
          setSelectedOption(res.user_attempt.submitted_answer);
        } else {
          setTextAnswer(res.user_attempt.submitted_answer);
        }
      }
    } catch (err: any) {
      setError(err.message || "Failed to load today's question.");
    } finally {
      setLoading(false);
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
      const res = await apiRequest<any>("/daily/attempt", {
        method: "POST",
        body: JSON.stringify({ submitted_answer: answerToSubmit }),
      });

      setData((prev) => prev ? {
        ...prev,
        has_attempted: true,
        user_attempt: res,
      } : null);
    } catch (err: any) {
      alert(err.message || "Submission failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AppLayout>
      <div className="max-w-3xl mx-auto space-y-6 animate-fade-in pb-16">
        {/* Header */}
        <div className="border-b border-slate-200 pb-4">
          <div className="flex items-center gap-2 mb-1">
            <Calendar className="h-5 w-5 text-amber-500" />
            <span className="text-xs font-bold text-amber-700 uppercase tracking-widest">Daily Technical Challenge</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Question of the Day</h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Build consistent technical intuition. Every day features a distinct question locked to one verified attempt.
          </p>
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="h-8 w-8 animate-spin text-amber-500 mb-3" />
            <p className="text-xs font-medium">Fetching today&apos;s challenge...</p>
          </div>
        ) : error || !data ? (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center justify-between">
            <span>{error || "Could not retrieve question."}</span>
            <button onClick={fetchDailyQuestion} className="font-semibold underline">Retry</button>
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs space-y-6">
            {/* Meta Tags */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200/60">
                  {new Date(data.date).toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" })}
                </span>
                <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700">
                  {data.role}
                </span>
                <span className="text-xs font-bold text-slate-600">
                  Topic: {data.topic}
                </span>
              </div>

              {data.has_attempted && (
                <span className="text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full flex items-center gap-1">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  Completed Today
                </span>
              )}
            </div>

            {/* Question Statement */}
            <h2 className="text-lg font-bold text-slate-900 leading-snug">
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
                          ? "border-amber-500 bg-amber-50/70 shadow-xs ring-1 ring-amber-400"
                          : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50"
                      } ${isDisabled ? "cursor-default" : ""}`}
                    >
                      <div className={`h-7 w-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                        isSelected ? "bg-amber-500 text-white" : "bg-slate-100 text-slate-700"
                      }`}>
                        {opt.key}
                      </div>
                      <span className="text-xs sm:text-sm font-medium text-slate-800 leading-relaxed">
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
                  placeholder="Explain the mechanism, trade-offs, and examples..."
                  className="w-full p-4 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 font-mono leading-relaxed"
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
                  className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm shadow-md shadow-amber-500/20 transition-all disabled:opacity-60"
                >
                  {submitting ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Recording Submission...</span>
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
              <div className="mt-6 p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-4 animate-in fade-in">
                <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                  <div className="flex items-center gap-2">
                    <Award className="h-5 w-5 text-amber-500" />
                    <span className="font-bold text-sm text-slate-900">Your Daily Result</span>
                  </div>
                  <div>
                    {data.user_attempt.is_correct ? (
                      <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                        <CheckCircle2 className="h-3.5 w-3.5" />
                        Correct
                      </span>
                    ) : (
                      <span className="text-xs font-bold text-rose-700 bg-rose-100 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                        <XCircle className="h-3.5 w-3.5" />
                        Incorrect
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-xs text-slate-700 leading-relaxed">
                  {data.user_attempt.feedback}
                </p>

                {data.user_attempt.explanation && (
                  <div className="p-3.5 rounded-xl bg-white border border-slate-200 text-xs text-slate-700">
                    <strong className="text-slate-900 block mb-1">
                      Correct Answer: Option {data.user_attempt.correct_option}
                    </strong>
                    <p>{data.user_attempt.explanation}</p>
                  </div>
                )}

                {data.user_attempt.model_answer && (
                  <div className="p-3.5 rounded-xl bg-white border border-slate-200 text-xs text-slate-800">
                    <strong className="text-slate-900 block mb-1">Engineering Model Answer:</strong>
                    <p className="whitespace-pre-line">{data.user_attempt.model_answer}</p>
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
