"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { Interview } from "@/types";
import { 
  Target, 
  BookOpen, 
  ArrowRight, 
  Loader2, 
  CheckCircle2, 
  Code2, 
  Server, 
  Terminal, 
  Cpu, 
  Layers, 
  Database,
  AlertCircle
} from "lucide-react";

const ROLES = [
  { id: "Python Developer", name: "Python Developer", icon: Terminal, desc: "Python fundamentals, data structures, functions, OOP, exception handling, asyncio" },
  { id: "Java Developer", name: "Java Developer", icon: Cpu, desc: "Java syntax, OOP, collections, exception handling, JVM, and multithreading" },
  { id: "Web Developer", name: "Web Developer", icon: Code2, desc: "HTML5, CSS3, JavaScript, HTTP/REST, responsive design, browser APIs, security" },
  { id: "Frontend Developer", name: "Frontend Developer", icon: Code2, desc: "React, Next.js, DOM, CSS architecture, Core Web Vitals, state management" },
  { id: "Backend Developer", name: "Backend Developer", icon: Server, desc: "REST APIs, database indexing, caching, microservices, auth, concurrency" },
  { id: "Data Analyst", name: "Data Analyst", icon: Database, desc: "SQL queries, Excel, data cleaning, statistics, visualization, analytical problem-solving" },
  { id: "Machine Learning Engineer", name: "Machine Learning Engineer", icon: Cpu, desc: "ML algorithms, feature engineering, model evaluation, overfitting, deep learning" },
  { id: "Database Administrator", name: "Database Administrator", icon: Database, desc: "SQL, normalization, indexing, transactions, ACID, query optimization, security" },
  { id: "Computer Networks", name: "Computer Networks", icon: Layers, desc: "OSI and TCP/IP models, routing, switching, DNS, TCP/UDP, network troubleshooting" },
  { id: "DevOps Engineer", name: "DevOps Engineer", icon: Layers, desc: "Docker, Kubernetes, CI/CD pipelines, Terraform, Linux networking, observability" },
  { id: "Custom", name: "Custom Domain / Role", icon: Target, desc: "Specify any custom domain, framework, or specialized job role" },
];

const DIFFICULTIES = [
  { id: "Junior", name: "Junior", desc: "Core syntax, data types, functions, standard libraries, foundational concepts" },
  { id: "Mid-Level", name: "Mid-Level", desc: "Design patterns, API optimization, error handling, database performance" },
  { id: "Senior", name: "Senior", desc: "System design, distributed architecture, scalability, complex trade-offs" },
];

function NewInterviewContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const roleParam = searchParams.get("role") || "";
  const diffParam = searchParams.get("difficulty") || "";
  const modeParam = searchParams.get("mode") || "";
  const countParam = parseInt(searchParams.get("count") || "0", 10);

  const isPresetRole = ROLES.some((r) => r.id.toLowerCase() === roleParam.toLowerCase());
  const initialRoleId = isPresetRole
    ? ROLES.find((r) => r.id.toLowerCase() === roleParam.toLowerCase())!.id
    : roleParam
    ? "Custom"
    : "Python Developer";

  const [selectedRoleId, setSelectedRoleId] = useState(initialRoleId);
  const [customRoleText, setCustomRoleText] = useState(!isPresetRole && roleParam ? roleParam : "");
  const [selectedDifficulty, setSelectedDifficulty] = useState(
    ["Junior", "Mid-Level", "Senior"].includes(diffParam) ? diffParam : "Junior"
  );
  const [selectedMode, setSelectedMode] = useState<"mcq" | "text">(
    modeParam === "text" ? "text" : "mcq"
  );
  const [questionCount, setQuestionCount] = useState(
    [3, 5, 10].includes(countParam) ? countParam : 5
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (roleParam) {
      const match = ROLES.find((r) => r.id.toLowerCase() === roleParam.toLowerCase());
      if (match) {
        setSelectedRoleId(match.id);
        setCustomRoleText("");
      } else {
        setSelectedRoleId("Custom");
        setCustomRoleText(roleParam);
      }
    }
    if (diffParam && ["Junior", "Mid-Level", "Senior"].includes(diffParam)) {
      setSelectedDifficulty(diffParam);
    }
    if (modeParam && ["mcq", "text"].includes(modeParam)) {
      setSelectedMode(modeParam as "mcq" | "text");
    }
    if (countParam && [3, 5, 10].includes(countParam)) {
      setQuestionCount(countParam);
    }
  }, [roleParam, diffParam, modeParam, countParam]);

  const effectiveRole = selectedRoleId === "Custom" ? customRoleText.trim() : selectedRoleId;

  const handleStart = async () => {
    setError(null);

    if (selectedRoleId === "Custom" && !customRoleText.trim()) {
      setError("Please enter your custom domain or job role.");
      return;
    }

    setLoading(true);

    try {
      const interview = await apiRequest<Interview>("/interviews/create", {
        method: "POST",
        body: JSON.stringify({
          job_role: effectiveRole,
          difficulty: selectedDifficulty,
          mode: selectedMode,
          num_questions: questionCount,
        }),
      });

      router.push(`/interviews/${interview.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to prepare your practice session. Please try again.");
      setLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
        {/* Header */}
        <div className="border-b border-[#E8DDCA] pb-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold text-[#879477] uppercase tracking-widest">Configuration</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#252923] tracking-tight">
            Set Up Your Practice Session
          </h1>
          <p className="text-xs sm:text-sm text-[#777B74] mt-1">
            Choose what you want to practise and create a session that matches your goals.
          </p>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-[#FDF1F0] border border-[#E8DDCA] text-[#B8473F] text-xs flex items-start gap-2.5">
            <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Step 1: Select Role */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-[#879477]">
            Step 1: Target Role / Domain
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {ROLES.map((role) => {
              const Icon = role.icon;
              const isSelected = selectedRoleId === role.id;
              return (
                <button
                  key={role.id}
                  type="button"
                  onClick={() => setSelectedRoleId(role.id)}
                  className={`p-4 rounded-xl text-left border transition-all flex flex-col justify-between ${
                    isSelected
                      ? "border-[#24483F] bg-[#EDF3EB] shadow-xs ring-1 ring-[#24483F]"
                      : "border-[#E8DDCA] bg-white hover:border-[#DCE6D8] hover:bg-[#FAF8F4]"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className={`h-8 w-8 rounded-lg flex items-center justify-center ${
                      isSelected ? "bg-[#24483F] text-[#F7F3EA]" : "bg-[#FAF8F4] text-[#252923] border border-[#E8DDCA]"
                    }`}>
                      <Icon className="h-4 w-4" />
                    </div>
                    {isSelected && <CheckCircle2 className="h-4 w-4 text-[#24483F]" />}
                  </div>
                  <div>
                    <h3 className="font-bold text-xs text-[#252923]">{role.name}</h3>
                    <p className="text-[11px] text-[#777B74] mt-0.5 line-clamp-2">{role.desc}</p>
                  </div>
                </button>
              );
            })}
          </div>

          {selectedRoleId === "Custom" && (
            <div className="mt-3 p-4 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] space-y-2 animate-in fade-in duration-150">
              <label className="block text-xs font-bold text-[#252923]">
                Enter Custom Domain or Job Role
              </label>
              <input
                type="text"
                value={customRoleText}
                onChange={(e) => setCustomRoleText(e.target.value)}
                placeholder="e.g. Cybersecurity Analyst, Cloud Architect, Go Developer, Systems Engineer..."
                className="w-full px-3.5 py-2.5 rounded-lg border border-[#E8DDCA] text-xs text-[#252923] bg-white focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F]"
              />
              <p className="text-[11px] text-[#777B74]">
                Questions will be dynamically generated and structured for this target role.
              </p>
            </div>
          )}
        </div>

        {/* Step 2: Select Difficulty */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-[#879477]">
            Step 2: Experience Level
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
                      ? "border-[#24483F] bg-[#EDF3EB] shadow-xs ring-1 ring-[#24483F]"
                      : "border-[#E8DDCA] bg-white hover:border-[#DCE6D8] hover:bg-[#FAF8F4]"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <h3 className="font-bold text-xs text-[#252923]">{diff.name}</h3>
                    {isSelected && <CheckCircle2 className="h-4 w-4 text-[#24483F]" />}
                  </div>
                  <p className="text-[11px] text-[#777B74] leading-relaxed">{diff.desc}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* Step 3: Select Mode */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-[#879477]">
            Step 3: Practice Format
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Multiple Choice */}
            <button
              type="button"
              onClick={() => setSelectedMode("mcq")}
              className={`p-5 rounded-2xl text-left border transition-all flex flex-col justify-between ${
                selectedMode === "mcq"
                  ? "border-[#24483F] bg-[#EDF3EB] shadow-sm ring-2 ring-[#24483F]"
                  : "border-[#E8DDCA] bg-white hover:border-[#DCE6D8] hover:bg-[#FAF8F4]"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className={`h-10 w-10 rounded-xl flex items-center justify-center ${
                    selectedMode === "mcq" ? "bg-[#24483F] text-[#F7F3EA]" : "bg-[#FAF8F4] text-[#24483F] border border-[#E8DDCA]"
                  }`}>
                    <Target className="h-5 w-5" />
                  </div>
                  <span className={`text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full ${
                    selectedMode === "mcq" ? "bg-[#24483F] text-[#F7F3EA]" : "bg-[#FAF8F4] text-[#777B74] border border-[#E8DDCA]"
                  }`}>
                    Multiple Choice
                  </span>
                </div>
                <h3 className="text-base font-bold text-[#252923] mb-1">Multiple Choice</h3>
                <p className="text-xs text-[#777B74] leading-relaxed mb-4">
                  Test your knowledge by choosing the correct answer. Instant scoring and detailed explanations upon completion.
                </p>
              </div>

              <div className="text-[11px] font-medium text-[#24483F] flex items-center gap-1.5 pt-2 border-t border-[#DCE6D8]">
                <CheckCircle2 className="h-3.5 w-3.5" />
                <span>Deterministic Scoring & Explanations</span>
              </div>
            </button>

            {/* Written Answers */}
            <button
              type="button"
              onClick={() => setSelectedMode("text")}
              className={`p-5 rounded-2xl text-left border transition-all flex flex-col justify-between ${
                selectedMode === "text"
                  ? "border-[#24483F] bg-[#EDF3EB] shadow-sm ring-2 ring-[#24483F]"
                  : "border-[#E8DDCA] bg-white hover:border-[#DCE6D8] hover:bg-[#FAF8F4]"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className={`h-10 w-10 rounded-xl flex items-center justify-center ${
                    selectedMode === "text" ? "bg-[#24483F] text-[#F7F3EA]" : "bg-[#FAF8F4] text-[#C66A4A] border border-[#E8DDCA]"
                  }`}>
                    <BookOpen className="h-5 w-5" />
                  </div>
                  <span className={`text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full ${
                    selectedMode === "text" ? "bg-[#24483F] text-[#F7F3EA]" : "bg-[#FAF8F4] text-[#777B74] border border-[#E8DDCA]"
                  }`}>
                    Written Answers
                  </span>
                </div>
                <h3 className="text-base font-bold text-[#252923] mb-1">Written Answers</h3>
                <p className="text-xs text-[#777B74] leading-relaxed mb-4">
                  Explain your understanding in your own words and receive detailed feedback, missed concepts, and sample answers.
                </p>
              </div>

              <div className="text-[11px] font-medium text-[#24483F] flex items-center gap-1.5 pt-2 border-t border-[#DCE6D8]">
                <CheckCircle2 className="h-3.5 w-3.5" />
                <span>Personalised Feedback & Sample Answers</span>
              </div>
            </button>
          </div>
        </div>

        {/* Step 4: Question Count */}
        <div className="space-y-3">
          <label className="block text-xs font-bold uppercase tracking-wider text-[#879477]">
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
                    ? "bg-[#24483F] text-[#F7F3EA] border-[#24483F] shadow-xs"
                    : "bg-white text-[#252923] border-[#E8DDCA] hover:bg-[#FAF8F4]"
                }`}
              >
                {num} Questions
              </button>
            ))}
          </div>
        </div>

        {/* Configuration Summary & Action */}
        <div className="p-5 rounded-2xl bg-white border border-[#E8DDCA] shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <span className="text-[11px] font-bold uppercase text-[#879477]">Session Summary</span>
            <p className="text-sm font-bold text-[#252923] mt-0.5">
              {selectedDifficulty} {effectiveRole || "Custom Role"} • {selectedMode === "mcq" ? "Multiple Choice" : "Written"} ({questionCount} Questions)
            </p>
          </div>

          <button
            type="button"
            onClick={handleStart}
            disabled={loading}
            className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-[#24483F] hover:bg-[#1A342D] text-[#F7F3EA] font-semibold text-sm shadow-sm transition-all disabled:opacity-60"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Preparing your questions...</span>
              </>
            ) : (
              <>
                <span>Create Practice Test</span>
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </AppLayout>
  );
}

export default function NewInterviewPage() {
  return (
    <Suspense
      fallback={
        <AppLayout>
          <div className="py-24 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-semibold">Preparing setup...</p>
          </div>
        </AppLayout>
      }
    >
      <NewInterviewContent />
    </Suspense>
  );
}
