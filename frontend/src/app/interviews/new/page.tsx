"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { Interview } from "@/types";
import { 
  Sparkles, 
  Target, 
  FileText, 
  ArrowRight, 
  Loader2, 
  CheckCircle2, 
  Code2, 
  Server, 
  Terminal, 
  Cpu, 
  Layers, 
  Database,
  Sliders,
  AlertCircle
} from "lucide-react";

const ROLES = [
  { id: "Frontend Developer", name: "Frontend Developer", icon: Code2, desc: "React, Next.js, DOM, CSS Grid/Flexbox, Core Web Vitals" },
  { id: "Backend Developer", name: "Backend Developer", icon: Server, desc: "REST APIs, database indexing, caching, microservices, auth" },
  { id: "Python Developer", name: "Python Developer", icon: Terminal, desc: "GIL, asyncio, decorators, memory management, generators" },
  { id: "Java Developer", name: "Java Developer", icon: Cpu, desc: "JVM memory, Spring Boot, GC, thread pools, Hibernate" },
  { id: "DevOps Engineer", name: "DevOps Engineer", icon: Layers, desc: "Docker, Kubernetes, CI/CD, Terraform, Linux networking" },
  { id: "Data Analyst", name: "Data Analyst", icon: Database, desc: "SQL window functions, pandas, data cleaning, stats" },
];

const DIFFICULTIES = [
  { id: "Junior", name: "Junior", desc: "Core syntax, data types, functions, standard libraries, foundational concepts" },
  { id: "Mid-Level", name: "Mid-Level", desc: "Design patterns, API optimization, error handling, database performance" },
  { id: "Senior", name: "Senior", desc: "System design, distributed architecture, scalability, complex trade-offs" },
];

export default function NewInterviewPage() {
  const router = useRouter();

  const [selectedRole, setSelectedRole] = useState("Frontend Developer");
  const [selectedDifficulty, setSelectedDifficulty] = useState("Mid-Level");
  const [selectedMode, setSelectedMode] = useState<"mcq" | "text">("mcq");
  const [questionCount, setQuestionCount] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleStart = async () => {
    setError(null);
    setLoading(true);

    try {
      const interview = await apiRequest<Interview>("/interviews/create", {
        method: "POST",
        body: JSON.stringify({
          job_role: selectedRole,
          difficulty: selectedDifficulty,
          mode: selectedMode,
          num_questions: questionCount,
        }),
      });

      router.push(`/interviews/${interview.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to generate interview. Please try again.");
      setLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
        {/* Header */}
        <div className="border-b border-slate-200 pb-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Configuration</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Configure Interview Simulation
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Select your target domain, difficulty, and preferred answer mode to generate AI-curated questions.
          </p>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5">
            <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Step 1: Select Role */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Step 1: Select Job Role
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {ROLES.map((role) => {
              const Icon = role.icon;
              const isSelected = selectedRole === role.id;
              return (
                <button
                  key={role.id}
                  type="button"
                  onClick={() => setSelectedRole(role.id)}
                  className={`p-4 rounded-xl text-left border transition-all flex flex-col justify-between ${
                    isSelected
                      ? "border-indigo-600 bg-indigo-50/60 shadow-xs ring-1 ring-indigo-600"
                      : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className={`h-8 w-8 rounded-lg flex items-center justify-center ${
                      isSelected ? "bg-indigo-600 text-white" : "bg-slate-100 text-slate-600"
                    }`}>
                      <Icon className="h-4 w-4" />
                    </div>
                    {isSelected && <CheckCircle2 className="h-4 w-4 text-indigo-600" />}
                  </div>
                  <div>
                    <h3 className="font-bold text-xs text-slate-900">{role.name}</h3>
                    <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-2">{role.desc}</p>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Step 2: Select Difficulty */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Step 2: Select Experience Difficulty
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {DIFFICULTIES.map((diff) => {
              const isSelected = selectedDifficulty === diff.id;
              return (
                <button
                  key={diff.id}
                  type="button"
                  onClick={() => setSelectedDifficulty(diff.id)}
                  className={`p-4 rounded-xl text-left border transition-all ${
                    isSelected
                      ? "border-indigo-600 bg-indigo-50/60 shadow-xs ring-1 ring-indigo-600"
                      : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <h3 className="font-bold text-xs text-slate-900">{diff.name}</h3>
                    {isSelected && <CheckCircle2 className="h-4 w-4 text-indigo-600" />}
                  </div>
                  <p className="text-[11px] text-slate-500 leading-relaxed">{diff.desc}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* Step 3: Select Mode (Prominently highlighted cards) */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Step 3: Select Answer Mode
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Mode A: MCQ */}
            <button
              type="button"
              onClick={() => setSelectedMode("mcq")}
              className={`p-5 rounded-2xl text-left border transition-all flex flex-col justify-between ${
                selectedMode === "mcq"
                  ? "border-blue-600 bg-blue-50/60 shadow-md ring-2 ring-blue-500"
                  : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className={`h-10 w-10 rounded-xl flex items-center justify-center ${
                    selectedMode === "mcq" ? "bg-blue-600 text-white" : "bg-blue-100 text-blue-700"
                  }`}>
                    <Target className="h-5 w-5" />
                  </div>
                  <span className={`text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full ${
                    selectedMode === "mcq" ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-600"
                  }`}>
                    Mode A
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-1">MCQ-Based Interview</h3>
                <p className="text-xs text-slate-600 leading-relaxed mb-4">
                  Select the correct option from 4 possibilities. Practice fast-paced technical concepts and receive instant deterministic marks and explanations upon submission.
                </p>
              </div>

              <div className="text-[11px] font-medium text-blue-700 flex items-center gap-1.5 pt-2 border-t border-blue-100/60">
                <CheckCircle2 className="h-3.5 w-3.5" />
                <span>Deterministic Scoring & Explanations</span>
              </div>
            </button>

            {/* Mode B: Text */}
            <button
              type="button"
              onClick={() => setSelectedMode("text")}
              className={`p-5 rounded-2xl text-left border transition-all flex flex-col justify-between ${
                selectedMode === "text"
                  ? "border-indigo-600 bg-indigo-50/60 shadow-md ring-2 ring-indigo-500"
                  : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className={`h-10 w-10 rounded-xl flex items-center justify-center ${
                    selectedMode === "text" ? "bg-indigo-600 text-white" : "bg-indigo-100 text-indigo-700"
                  }`}>
                    <Sparkles className="h-5 w-5" />
                  </div>
                  <span className={`text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full ${
                    selectedMode === "text" ? "bg-indigo-600 text-white" : "bg-slate-100 text-slate-600"
                  }`}>
                    Mode B
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-1">Text-Based Technical Interview</h3>
                <p className="text-xs text-slate-600 leading-relaxed mb-4">
                  Write your own answers in multiline response editor. Evaluated by Gemini AI on correctness, technical depth, clarity, missing keywords, and accompanied by full model answers.
                </p>
              </div>

              <div className="text-[11px] font-medium text-indigo-700 flex items-center gap-1.5 pt-2 border-t border-indigo-100/60">
                <CheckCircle2 className="h-3.5 w-3.5" />
                <span>AI Rubric Evaluation & Model Answers</span>
              </div>
            </button>
          </div>
        </div>

        {/* Step 4: Question Count */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Step 4: Number of Questions
          </label>
          <div className="flex gap-3">
            {[3, 5, 10].map((num) => (
              <button
                key={num}
                type="button"
                onClick={() => setQuestionCount(num)}
                className={`flex-1 py-3 px-4 rounded-xl font-bold text-xs border transition-all ${
                  questionCount === num
                    ? "bg-slate-900 text-white border-slate-900 shadow-xs"
                    : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                }`}
              >
                {num} Questions
              </button>
            ))}
          </div>
        </div>

        {/* Configuration Summary & Action */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <span className="text-[11px] font-bold uppercase text-slate-400">Ready to begin</span>
            <p className="text-sm font-bold text-slate-900 mt-0.5">
              {selectedDifficulty} {selectedRole} • {selectedMode.toUpperCase()} Mode ({questionCount} Qs)
            </p>
          </div>

          <button
            type="button"
            onClick={handleStart}
            disabled={loading}
            className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-md shadow-indigo-600/20 transition-all disabled:opacity-60"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Generating Questions via Gemini AI...</span>
              </>
            ) : (
              <>
                <span>Start Interview Simulation</span>
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </AppLayout>
  );
}
