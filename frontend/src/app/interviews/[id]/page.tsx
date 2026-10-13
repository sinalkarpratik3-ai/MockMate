"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useParams, useRouter } from "next/navigation";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { Interview, Question, Answer } from "@/types";
import { 
  CheckCircle2, 
  ArrowRight, 
  ArrowLeft, 
  Loader2, 
  Send, 
  Sparkles, 
  Target, 
  AlertCircle, 
  HelpCircle,
  Award,
  BookOpen,
  Check,
  ChevronRight
} from "lucide-react";

function InterviewWorkspaceContent() {
  const params = useParams();
  const router = useRouter();
  const interviewId = params.id as string;

  const [interview, setInterview] = useState<Interview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [currentIndex, setCurrentIndex] = useState(0);

  // Mode A: MCQ state
  const [selectedOptions, setSelectedOptions] = useState<Record<number, string>>({});
  const [submittingInterview, setSubmittingInterview] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  // Mode B: Text state
  const [textAnswers, setTextAnswers] = useState<Record<number, string>>({});
  const [evaluatingQuestion, setEvaluatingQuestion] = useState(false);
  const [evaluatedAnswers, setEvaluatedAnswers] = useState<Record<number, Answer>>({});

  useEffect(() => {
    fetchInterview();
  }, [interviewId]);

  const fetchInterview = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiRequest<Interview>(`/interviews/${interviewId}`);
      
      if (data.status === "completed") {
        router.push(`/interviews/${interviewId}/results`);
        return;
      }

      setInterview(data);

      // Hydrate existing answers if resumed
      if (data.answers && data.answers.length > 0) {
        const mcqMap: Record<number, string> = {};
        const textMap: Record<number, string> = {};
        const evalMap: Record<number, Answer> = {};

        data.answers.forEach((ans) => {
          if (ans.selected_option) {
            mcqMap[ans.question_id] = ans.selected_option;
          }
          if (ans.text_answer) {
            textMap[ans.question_id] = ans.text_answer;
          }
          evalMap[ans.question_id] = ans;
        });

        setSelectedOptions(mcqMap);
        setTextAnswers(textMap);
        setEvaluatedAnswers(evalMap);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load interview session.");
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion: Question | undefined = interview?.questions?.[currentIndex];
  const totalQuestions = interview?.questions?.length || 0;

  // Handle MCQ Option Selection
  const handleSelectMCQ = (optionKey: string) => {
    if (!currentQuestion) return;
    setSelectedOptions((prev) => ({
      ...prev,
      [currentQuestion.id]: optionKey,
    }));
  };

  // Submit single Text Answer for AI evaluation
  const handleSubmitTextAnswer = async () => {
    if (!currentQuestion) return;
    const answerText = textAnswers[currentQuestion.id] || "";
    if (!answerText.trim()) {
      alert("Please write your answer before submitting.");
      return;
    }

    setEvaluatingQuestion(true);
    try {
      const res = await apiRequest<Answer>(`/interviews/${interviewId}/submit-answer`, {
        method: "POST",
        body: JSON.stringify({
          question_id: currentQuestion.id,
          text_answer: answerText,
        }),
      });

      setEvaluatedAnswers((prev) => ({
        ...prev,
        [currentQuestion.id]: res,
      }));
    } catch (err: any) {
      alert(err.message || "Evaluation failed. Please try again.");
    } finally {
      setEvaluatingQuestion(false);
    }
  };

  // Final submission of interview
  const handleFinalSubmit = async () => {
    if (!interview) return;
    setSubmittingInterview(true);
    setShowConfirmModal(false);

    try {
      if (interview.mode === "mcq") {
        // Submit all selected MCQ answers in batch
        const batch = Object.entries(selectedOptions).map(([qId, opt]) => ({
          question_id: parseInt(qId),
          selected_option: opt,
        }));

        await apiRequest(`/interviews/${interviewId}/submit-batch`, {
          method: "POST",
          body: JSON.stringify({ answers: batch }),
        });
      } else {
        // Finalize text interview
        await apiRequest(`/interviews/${interviewId}/complete`, {
          method: "POST",
        });
      }

      router.push(`/interviews/${interviewId}/results`);
    } catch (err: any) {
      alert(err.message || "Failed to complete interview.");
      setSubmittingInterview(false);
    }
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="py-32 flex flex-col items-center justify-center text-slate-500">
          <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
          <p className="text-xs font-semibold">Loading interview session...</p>
        </div>
      </AppLayout>
    );
  }

  if (error || !interview || !currentQuestion) {
    return (
      <AppLayout>
        <div className="max-w-xl mx-auto py-16 text-center">
          <AlertCircle className="h-10 w-10 text-rose-500 mx-auto mb-3" />
          <h2 className="text-lg font-bold text-slate-900">Session Error</h2>
          <p className="text-xs text-slate-600 mt-1">{error || "Could not load questions."}</p>
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
  const currentTextAnswer = textAnswers[currentQuestion.id] || "";
  const currentEvaluation = evaluatedAnswers[currentQuestion.id];
  const answeredCount = isMCQ 
    ? Object.keys(selectedOptions).length 
    : Object.keys(evaluatedAnswers).length;

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-6 animate-fade-in pb-16">
        {/* Top Header Bar */}
        <div className="bg-white rounded-2xl border border-slate-200 p-4 sm:p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700">
                {interview.job_role}
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                {interview.difficulty}
              </span>
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                isMCQ ? "bg-blue-50 text-blue-700" : "bg-purple-50 text-purple-700"
              }`}>
                {interview.mode.toUpperCase()} Mode
              </span>
            </div>
            <h1 className="text-base sm:text-lg font-bold text-slate-900">
              Question {currentIndex + 1} of {totalQuestions}
            </h1>
          </div>

          <div className="flex items-center gap-4">
            {/* Progress Counter */}
            <div className="text-right">
              <p className="text-xs font-semibold text-slate-700">
                {answeredCount} of {totalQuestions} Answered
              </p>
              <div className="w-32 bg-slate-100 rounded-full h-2 mt-1 overflow-hidden">
                <div
                  className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(answeredCount / totalQuestions) * 100}%` }}
                />
              </div>
            </div>

            <button
              type="button"
              onClick={() => setShowConfirmModal(true)}
              disabled={submittingInterview}
              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs shadow-xs transition-all disabled:opacity-60"
            >
              Finish & Submit
            </button>
          </div>
        </div>

        {/* Question Palette (Quick Jump) */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {interview.questions?.map((q, idx) => {
            const isAnswered = isMCQ 
              ? selectedOptions[q.id] !== undefined 
              : evaluatedAnswers[q.id] !== undefined;
            const isCurrent = idx === currentIndex;

            return (
              <button
                key={q.id}
                onClick={() => setCurrentIndex(idx)}
                className={`h-8 min-w-[32px] px-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1 ${
                  isCurrent
                    ? "bg-indigo-600 text-white shadow-xs"
                    : isAnswered
                    ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                    : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
                }`}
              >
                <span>{idx + 1}</span>
                {isAnswered && !isCurrent && <Check className="h-3 w-3 text-emerald-600" />}
              </button>
            );
          })}
        </div>

        {/* Main Question Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs space-y-6">
          {/* Question Metadata */}
          <div className="flex items-center justify-between text-xs text-slate-500 border-b border-slate-100 pb-3">
            <span className="font-semibold text-indigo-600">Topic: {currentQuestion.topic}</span>
            <span>Question ID #{currentQuestion.id}</span>
          </div>

          {/* Question Statement */}
          <div className="text-base sm:text-lg font-bold text-slate-900 leading-snug">
            {currentQuestion.question_text}
          </div>

          {/* Mode A: MCQ Options Rendering */}
          {isMCQ && currentQuestion.options && (
            <div className="space-y-3 pt-2">
              {currentQuestion.options.map((opt) => {
                const isSelected = selectedOptions[currentQuestion.id] === opt.key;
                return (
                  <button
                    key={opt.key}
                    type="button"
                    onClick={() => handleSelectMCQ(opt.key)}
                    className={`w-full p-4 rounded-xl border text-left transition-all flex items-center gap-3.5 ${
                      isSelected
                        ? "border-indigo-600 bg-indigo-50/70 shadow-xs ring-1 ring-indigo-500"
                        : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50"
                    }`}
                  >
                    <div className={`h-7 w-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                      isSelected ? "bg-indigo-600 text-white" : "bg-slate-100 text-slate-700"
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

          {/* Mode B: Text Editor & Feedback */}
          {!isMCQ && (
            <div className="space-y-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Your Technical Answer
                </label>
                <textarea
                  rows={6}
                  value={currentTextAnswer}
                  onChange={(e) => setTextAnswers({ ...textAnswers, [currentQuestion.id]: e.target.value })}
                  placeholder="Explain the mechanism, trade-offs, architecture, and real-world examples..."
                  disabled={evaluatingQuestion}
                  className="w-full p-4 rounded-xl border border-slate-200 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all font-mono leading-relaxed"
                />
                <div className="flex justify-between items-center text-[11px] text-slate-400 mt-1">
                  <span>Aim for technical depth, mechanism, and practical trade-offs.</span>
                  <span>{currentTextAnswer.length} characters</span>
                </div>
              </div>

              {/* Submit text answer button */}
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={handleSubmitTextAnswer}
                  disabled={evaluatingQuestion || !currentTextAnswer.trim()}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-sm transition-all disabled:opacity-50"
                >
                  {evaluatingQuestion ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Evaluating with Gemini AI...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="h-4 w-4" />
                      <span>{currentEvaluation ? "Re-evaluate Answer" : "Submit for AI Evaluation"}</span>
                    </>
                  )}
                </button>
              </div>

              {/* Instant Evaluation Card */}
              {currentEvaluation && (
                <div className="mt-6 p-5 rounded-2xl bg-indigo-50/50 border border-indigo-100 space-y-4 animate-in fade-in duration-200">
                  <div className="flex items-center justify-between border-b border-indigo-100 pb-3">
                    <div className="flex items-center gap-2">
                      <Award className="h-5 w-5 text-indigo-600" />
                      <span className="font-bold text-sm text-slate-900">AI Evaluation Feedback</span>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-semibold text-slate-500">Score: </span>
                      <span className="text-base font-extrabold text-indigo-600">
                        {currentEvaluation.score} / 10
                      </span>
                    </div>
                  </div>

                  {/* Feedback paragraph */}
                  <p className="text-xs text-slate-700 leading-relaxed font-medium">
                    {currentEvaluation.feedback}
                  </p>

                  {/* Strengths */}
                  {currentEvaluation.strengths && currentEvaluation.strengths.length > 0 && (
                    <div>
                      <span className="text-[11px] font-bold uppercase text-emerald-700 tracking-wider">Strengths</span>
                      <ul className="mt-1 space-y-1 text-xs text-slate-700">
                        {currentEvaluation.strengths.map((s, idx) => (
                          <li key={idx} className="flex items-start gap-1.5">
                            <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600 shrink-0 mt-0.5" />
                            <span>{s}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Missing Concepts */}
                  {currentEvaluation.missing_concepts && currentEvaluation.missing_concepts.length > 0 && (
                    <div>
                      <span className="text-[11px] font-bold uppercase text-amber-700 tracking-wider">Missing Concepts</span>
                      <ul className="mt-1 space-y-1 text-xs text-slate-700">
                        {currentEvaluation.missing_concepts.map((m, idx) => (
                          <li key={idx} className="flex items-start gap-1.5">
                            <AlertCircle className="h-3.5 w-3.5 text-amber-600 shrink-0 mt-0.5" />
                            <span>{m}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Improvement Tips */}
                  {currentEvaluation.improvement_tips && currentEvaluation.improvement_tips.length > 0 && (
                    <div>
                      <span className="text-[11px] font-bold uppercase text-indigo-700 tracking-wider">Improvement Advice</span>
                      <ul className="mt-1 space-y-1 text-xs text-slate-700">
                        {currentEvaluation.improvement_tips.map((tip, idx) => (
                          <li key={idx} className="flex items-start gap-1.5">
                            <ArrowRight className="h-3.5 w-3.5 text-indigo-600 shrink-0 mt-0.5" />
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Model Answer Preview */}
                  {currentEvaluation.model_answer && (
                    <div className="pt-2 border-t border-indigo-100">
                      <span className="text-[11px] font-bold uppercase text-slate-700 tracking-wider flex items-center gap-1.5 mb-1.5">
                        <BookOpen className="h-3.5 w-3.5 text-indigo-600" />
                        Ideal Model Answer
                      </span>
                      <div className="p-3.5 rounded-xl bg-white border border-slate-200 text-xs text-slate-800 leading-relaxed whitespace-pre-line font-sans">
                        {currentEvaluation.model_answer}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Bottom Navigation Buttons */}
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
            disabled={currentIndex === 0}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl border border-slate-200 bg-white text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors disabled:opacity-40"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Previous</span>
          </button>

          {currentIndex < totalQuestions - 1 ? (
            <button
              type="button"
              onClick={() => setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1))}
              className="inline-flex items-center gap-1.5 px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-xs transition-colors"
            >
              <span>Next Question</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setShowConfirmModal(true)}
              className="inline-flex items-center gap-1.5 px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-xs transition-colors"
            >
              <span>Review & Submit Interview</span>
              <Check className="h-4 w-4" />
            </button>
          )}
        </div>

        {/* Confirmation Modal */}
        {showConfirmModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
            <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-100 space-y-4 animate-in zoom-in-95 duration-150">
              <h3 className="text-lg font-bold text-slate-900">Submit Completed Interview?</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                You have answered <strong>{answeredCount} of {totalQuestions}</strong> questions.
                Once submitted, your final scorecard and topic-level analytics will be computed and recorded.
              </p>

              <div className="flex items-center justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowConfirmModal(false)}
                  className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  Continue Answering
                </button>
                <button
                  type="button"
                  onClick={handleFinalSubmit}
                  disabled={submittingInterview}
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-xs transition-all disabled:opacity-60"
                >
                  {submittingInterview ? "Submitting..." : "Yes, Submit Interview"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

export default function InterviewWorkspacePage() {
  return (
    <Suspense
      fallback={
        <AppLayout>
          <div className="py-32 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
            <p className="text-xs font-semibold">Loading interview session...</p>
          </div>
        </AppLayout>
      }
    >
      <InterviewWorkspaceContent />
    </Suspense>
  );
}
