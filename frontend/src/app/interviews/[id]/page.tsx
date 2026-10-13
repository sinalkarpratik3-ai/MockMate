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
  Target, 
  AlertCircle, 
  Award, 
  BookOpen, 
  Check, 
  CheckSquare
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
      setError(err.message || "Failed to load practice session.");
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

  // Submit single Text Answer for Review
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
      alert(err.message || "Review failed. Please try again.");
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
        const batch = Object.entries(selectedOptions).map(([qId, opt]) => ({
          question_id: parseInt(qId),
          selected_option: opt,
        }));

        await apiRequest(`/interviews/${interviewId}/submit-batch`, {
          method: "POST",
          body: JSON.stringify({ answers: batch }),
        });
      } else {
        await apiRequest(`/interviews/${interviewId}/complete`, {
          method: "POST",
        });
      }

      router.push(`/interviews/${interviewId}/results`);
    } catch (err: any) {
      alert(err.message || "Failed to complete practice session.");
      setSubmittingInterview(false);
    }
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="py-32 flex flex-col items-center justify-center text-[#777B74]">
          <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
          <p className="text-xs font-semibold">Loading your practice session...</p>
        </div>
      </AppLayout>
    );
  }

  if (error || !interview || !currentQuestion) {
    return (
      <AppLayout>
        <div className="max-w-xl mx-auto py-16 text-center">
          <AlertCircle className="h-10 w-10 text-[#B8473F] mx-auto mb-3" />
          <h2 className="text-lg font-bold text-[#252923]">Session Notice</h2>
          <p className="text-xs text-[#777B74] mt-1">{error || "Could not load practice questions."}</p>
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
  const currentTextAnswer = textAnswers[currentQuestion.id] || "";
  const currentEvaluation = evaluatedAnswers[currentQuestion.id];
  const answeredCount = isMCQ 
    ? Object.keys(selectedOptions).length 
    : Object.keys(evaluatedAnswers).length;

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-6 animate-fade-in pb-16">
        {/* Top Header Bar */}
        <div className="bg-white rounded-2xl border border-[#E8DDCA] p-4 sm:p-5 shadow-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#EDF3EB] text-[#24483F] border border-[#DCE6D8]">
                {interview.job_role}
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#FAF8F4] text-[#252923] border border-[#E8DDCA]">
                {interview.difficulty}
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#FAF8F4] text-[#879477] border border-[#E8DDCA]">
                {isMCQ ? "Multiple Choice" : "Written Answers"}
              </span>
            </div>
            <h1 className="text-base sm:text-lg font-bold text-[#252923]">
              Question {currentIndex + 1} of {totalQuestions}
            </h1>
          </div>

          <div className="flex items-center gap-4">
            {/* Progress Counter */}
            <div className="text-right">
              <p className="text-xs font-semibold text-[#252923]">
                {answeredCount} of {totalQuestions} Answered
              </p>
              <div className="w-32 bg-[#FAF8F4] border border-[#E8DDCA] rounded-full h-2 mt-1 overflow-hidden">
                <div
                  className="bg-[#24483F] h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(answeredCount / totalQuestions) * 100}%` }}
                />
              </div>
            </div>

            <button
              type="button"
              onClick={() => setShowConfirmModal(true)}
              disabled={submittingInterview}
              className="px-4 py-2 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] font-semibold text-xs shadow-xs transition-all disabled:opacity-60"
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
                    ? "bg-[#24483F] text-[#F7F3EA] shadow-xs"
                    : isAnswered
                    ? "bg-[#EDF3EB] text-[#24483F] border border-[#DCE6D8]"
                    : "bg-white text-[#777B74] border border-[#E8DDCA] hover:bg-[#FAF8F4]"
                }`}
              >
                <span>{idx + 1}</span>
                {isAnswered && !isCurrent && <Check className="h-3 w-3 text-[#367451]" />}
              </button>
            );
          })}
        </div>

        {/* Main Question Card */}
        <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 sm:p-8 shadow-xs space-y-6">
          {/* Question Metadata */}
          <div className="flex items-center justify-between text-xs text-[#879477] border-b border-[#E8DDCA] pb-3">
            <span className="font-semibold text-[#24483F]">Topic: {currentQuestion.topic}</span>
            <span>Question #{currentIndex + 1}</span>
          </div>

          {/* Question Statement */}
          <div className="text-base sm:text-lg font-bold text-[#252923] leading-snug">
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
                        ? "border-[#24483F] bg-[#EDF3EB] shadow-xs ring-1 ring-[#24483F]"
                        : "border-[#E8DDCA] bg-white hover:border-[#DCE6D8] hover:bg-[#FAF8F4]"
                    }`}
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

          {/* Mode B: Text Editor & Feedback */}
          {!isMCQ && (
            <div className="space-y-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-[#252923] mb-1.5">
                  Your Answer
                </label>
                <textarea
                  rows={6}
                  value={currentTextAnswer}
                  onChange={(e) => setTextAnswers({ ...textAnswers, [currentQuestion.id]: e.target.value })}
                  placeholder="Explain the mechanism, trade-offs, architecture, and practical considerations in your own words..."
                  disabled={evaluatingQuestion}
                  className="w-full p-4 rounded-xl border border-[#E8DDCA] text-sm text-[#252923] placeholder:text-[#879477] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F] transition-all font-mono leading-relaxed bg-[#FAF8F4] focus:bg-white"
                />
                <div className="flex justify-between items-center text-[11px] text-[#777B74] mt-1">
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
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] font-semibold text-xs shadow-sm transition-all disabled:opacity-50"
                >
                  {evaluatingQuestion ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Reviewing your answer...</span>
                    </>
                  ) : (
                    <>
                      <CheckSquare className="h-4 w-4" />
                      <span>{currentEvaluation ? "Update Answer" : "Submit for Review"}</span>
                    </>
                  )}
                </button>
              </div>

              {/* Instant Evaluation Card */}
              {currentEvaluation && (
                <div className="mt-6 p-5 rounded-2xl bg-[#FAF8F4] border border-[#E8DDCA] space-y-4 animate-in fade-in duration-200">
                  <div className="flex items-center justify-between border-b border-[#E8DDCA] pb-3">
                    <div className="flex items-center gap-2">
                      <Award className="h-5 w-5 text-[#24483F]" />
                      <span className="font-bold text-sm text-[#252923]">Answer Review</span>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-semibold text-[#777B74]">Score: </span>
                      <span className="text-base font-extrabold text-[#24483F]">
                        {currentEvaluation.score} / 10
                      </span>
                    </div>
                  </div>

                  {/* Feedback paragraph */}
                  <p className="text-xs text-[#252923] leading-relaxed font-medium">
                    {currentEvaluation.feedback}
                  </p>

                  {/* Strengths */}
                  {currentEvaluation.strengths && currentEvaluation.strengths.length > 0 && (
                    <div>
                      <span className="text-[11px] font-bold uppercase text-[#367451] tracking-wider">What You Did Well</span>
                      <ul className="mt-1 space-y-1 text-xs text-[#252923]">
                        {currentEvaluation.strengths.map((s, idx) => (
                          <li key={idx} className="flex items-start gap-1.5">
                            <CheckCircle2 className="h-3.5 w-3.5 text-[#367451] shrink-0 mt-0.5" />
                            <span>{s}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Missing Concepts */}
                  {currentEvaluation.missing_concepts && currentEvaluation.missing_concepts.length > 0 && (
                    <div>
                      <span className="text-[11px] font-bold uppercase text-[#C66A4A] tracking-wider">Key Concepts to Review</span>
                      <ul className="mt-1 space-y-1 text-xs text-[#252923]">
                        {currentEvaluation.missing_concepts.map((m, idx) => (
                          <li key={idx} className="flex items-start gap-1.5">
                            <AlertCircle className="h-3.5 w-3.5 text-[#C66A4A] shrink-0 mt-0.5" />
                            <span>{m}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Improvement Tips */}
                  {currentEvaluation.improvement_tips && currentEvaluation.improvement_tips.length > 0 && (
                    <div>
                      <span className="text-[11px] font-bold uppercase text-[#24483F] tracking-wider">Suggestions for Improvement</span>
                      <ul className="mt-1 space-y-1 text-xs text-[#252923]">
                        {currentEvaluation.improvement_tips.map((tip, idx) => (
                          <li key={idx} className="flex items-start gap-1.5">
                            <ArrowRight className="h-3.5 w-3.5 text-[#24483F] shrink-0 mt-0.5" />
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Sample Answer Preview */}
                  {currentEvaluation.model_answer && (
                    <div className="pt-2 border-t border-[#E8DDCA]">
                      <span className="text-[11px] font-bold uppercase text-[#252923] tracking-wider flex items-center gap-1.5 mb-1.5">
                        <BookOpen className="h-3.5 w-3.5 text-[#24483F]" />
                        Sample Answer
                      </span>
                      <div className="p-3.5 rounded-xl bg-white border border-[#E8DDCA] text-xs text-[#252923] leading-relaxed whitespace-pre-line font-sans">
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
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl border border-[#E8DDCA] bg-white text-xs font-semibold text-[#252923] hover:bg-[#FAF8F4] transition-colors disabled:opacity-40"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Previous Question</span>
          </button>

          {currentIndex < totalQuestions - 1 ? (
            <button
              type="button"
              onClick={() => setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1))}
              className="inline-flex items-center gap-1.5 px-5 py-2 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] text-xs font-semibold shadow-xs transition-colors"
            >
              <span>Next Question</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setShowConfirmModal(true)}
              className="inline-flex items-center gap-1.5 px-5 py-2 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] text-xs font-semibold shadow-xs transition-colors"
            >
              <span>Review Answers & Submit</span>
              <Check className="h-4 w-4" />
            </button>
          )}
        </div>

        {/* Confirmation Modal */}
        {showConfirmModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#252923]/40 backdrop-blur-xs">
            <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-[#E8DDCA] space-y-4 animate-in zoom-in-95 duration-150">
              <h3 className="text-lg font-bold text-[#252923]">Submit Practice Session?</h3>
              <p className="text-xs text-[#777B74] leading-relaxed">
                You have answered <strong>{answeredCount} of {totalQuestions}</strong> questions.
                Once submitted, your final scorecard and topic performance will be recorded.
              </p>

              <div className="flex items-center justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowConfirmModal(false)}
                  className="px-4 py-2 rounded-xl border border-[#E8DDCA] text-xs font-semibold text-[#252923] hover:bg-[#FAF8F4] transition-colors"
                >
                  Continue Answering
                </button>
                <button
                  type="button"
                  onClick={handleFinalSubmit}
                  disabled={submittingInterview}
                  className="px-5 py-2 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] text-xs font-semibold shadow-xs transition-all disabled:opacity-60"
                >
                  {submittingInterview ? "Saving..." : "Submit Session"}
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
          <div className="py-32 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-semibold">Loading your practice session...</p>
          </div>
        </AppLayout>
      }
    >
      <InterviewWorkspaceContent />
    </Suspense>
  );
}
