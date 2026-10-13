"use client";

import React from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";
import { 
  Sparkles, 
  CheckCircle2, 
  ArrowRight, 
  BrainCircuit, 
  Target, 
  BarChart3, 
  Calendar, 
  Bookmark, 
  ShieldCheck, 
  Layers,
  Code2,
  Terminal,
  Server,
  Database,
  Cpu
} from "lucide-react";

export default function LandingPage() {
  const { user } = useAuth();

  const roles = [
    { name: "Frontend Developer", icon: Code2, desc: "React, Next.js, CSS architecture, Core Web Vitals, state management." },
    { name: "Backend Developer", icon: Server, desc: "REST APIs, indexing, caching, microservices, database transactions." },
    { name: "Python Developer", icon: Terminal, desc: "GIL, asyncio, decorators, memory management, algorithms." },
    { name: "Java Developer", icon: Cpu, desc: "JVM internals, Spring Boot, GC tuning, concurrency, Hibernate." },
    { name: "DevOps Engineer", icon: Layers, desc: "Docker, Kubernetes, CI/CD pipelines, Terraform, zero-downtime releases." },
    { name: "Data Analyst", icon: Database, desc: "SQL window functions, pandas, data cleaning, statistical significance." },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col selection:bg-indigo-500 selection:text-white">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 sm:pt-20 sm:pb-28 bg-white border-b border-slate-200">
        <div className="absolute inset-0 bg-[radial-gradient(#e0e7ff_1px,transparent_1px)] [background-size:16px_16px] opacity-40 -z-10" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          
          {/* Top Pill */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 text-xs font-semibold mb-8 animate-fade-in">
            <Sparkles className="h-4 w-4 text-indigo-600" />
            <span>Google Gemini 3.8 Flash AI Model Integration</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-[1.15]">
            Master Technical Interviews with <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-600">Precision AI Simulation</span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Practice AI-generated technical questions, test yourself with instant MCQ scoring, receive deep architectural evaluations for written answers, and systematically eliminate your weak topics.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href={user ? "/dashboard" : "/register"}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-indigo-600 text-white font-semibold text-base shadow-lg shadow-indigo-600/25 hover:bg-indigo-700 hover:shadow-xl transition-all"
            >
              <span>{user ? "Go to Dashboard" : "Start Practicing Now"}</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              href="/interviews/new"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-slate-100 text-slate-700 font-semibold text-base hover:bg-slate-200 transition-colors"
            >
              <BrainCircuit className="h-4 w-4 text-slate-500" />
              <span>Simulate an Interview</span>
            </Link>
          </div>

          {/* Quick proof badges */}
          <div className="mt-12 pt-8 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto text-slate-600 text-xs font-medium">
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              <span>Zero Fake Placeholders</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              <span>Dual Practice Modes</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              <span>PostgreSQL Persisted</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              <span>Render Deployable</span>
            </div>
          </div>
        </div>
      </section>

      {/* Dual Mode Showcase */}
      <section className="py-16 sm:py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest mb-2">Two Distinct Assessment Modes</h2>
          <p className="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight">Tailored to How You Learn Best</p>
          <p className="mt-3 text-base text-slate-600">Choose the format that fits your study objective for the session.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Mode A: MCQ */}
          <div className="rounded-2xl p-8 bg-white border border-slate-200 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between">
            <div>
              <div className="h-12 w-12 rounded-xl bg-blue-50 border border-blue-200/60 flex items-center justify-center text-blue-600 mb-6">
                <Target className="h-6 w-6" />
              </div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md">Mode A</span>
              <h3 className="text-2xl font-bold text-slate-900 mt-3 mb-2">MCQ-Based Technical Quiz</h3>
              <p className="text-slate-600 text-sm leading-relaxed mb-6">
                Test rapid-fire conceptual knowledge and terminology with 4 curated options per question. Correct answers are hidden until submission to guarantee honest testing.
              </p>

              <ul className="space-y-3 text-sm text-slate-700 mb-8">
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
                  <span>Deterministic instant scoring without AI hallucination</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
                  <span>Explanations and correct answers revealed post-submission</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="h-4 w-4 text-blue-600 shrink-0 mt-0.5" />
                  <span>Next/Previous navigation with review screen</span>
                </li>
              </ul>
            </div>

            <Link
              href="/interviews/new"
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-blue-50 text-blue-700 hover:bg-blue-100 font-semibold text-sm transition-colors w-full"
            >
              <span>Practice MCQ Questions</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          {/* Mode B: Text */}
          <div className="rounded-2xl p-8 bg-white border border-slate-200 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between">
            <div>
              <div className="h-12 w-12 rounded-xl bg-indigo-50 border border-indigo-200/60 flex items-center justify-center text-indigo-600 mb-6">
                <Sparkles className="h-6 w-6" />
              </div>
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-md">Mode B</span>
              <h3 className="text-2xl font-bold text-slate-900 mt-3 mb-2">Text-Based Technical Interview</h3>
              <p className="text-slate-600 text-sm leading-relaxed mb-6">
                Articulate architectural reasoning, algorithms, and design choices. Your multiline answers are evaluated against a rigorous 6-point rubric by Gemini.
              </p>

              <ul className="space-y-3 text-sm text-slate-700 mb-8">
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="h-4 w-4 text-indigo-600 shrink-0 mt-0.5" />
                  <span>Evaluates correctness, depth, clarity, and missing keywords</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="h-4 w-4 text-indigo-600 shrink-0 mt-0.5" />
                  <span>Integer score from 0 to 10 with actionable improvement feedback</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="h-4 w-4 text-indigo-600 shrink-0 mt-0.5" />
                  <span>Comprehensive engineering model answer for direct comparison</span>
                </li>
              </ul>
            </div>

            <Link
              href="/interviews/new"
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-semibold text-sm transition-colors w-full"
            >
              <span>Practice Written Answers</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Supported Roles */}
      <section className="py-16 bg-white border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest mb-2">Curated Curricula</h2>
            <p className="text-3xl font-bold text-slate-900 tracking-tight">6 High-Demand Engineering Roles</p>
            <p className="mt-2 text-sm text-slate-600">From Junior fundamentals to Senior system design trade-offs.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {roles.map((role) => {
              const Icon = role.icon;
              return (
                <div key={role.name} className="p-6 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:shadow-sm transition-all">
                  <div className="h-10 w-10 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center mb-4">
                    <Icon className="h-5 w-5" />
                  </div>
                  <h3 className="font-bold text-base text-slate-900 mb-1">{role.name}</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">{role.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="py-16 sm:py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest mb-2">Complete Platform Toolkit</h2>
          <p className="text-3xl font-bold text-slate-900 tracking-tight">Engineered for Rapid Improvement</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs">
            <div className="h-10 w-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-4">
              <Target className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 mb-2">Weak Topic Auto-Detection</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Analyzes historical attempts to flag concepts with &lt;60% accuracy, offering 1-click targeted revision.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs">
            <div className="h-10 w-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-4">
              <Calendar className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 mb-2">Question of the Day</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Build a daily practice streak with a rotating daily challenge that locks once attempted to preserve integrity.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs">
            <div className="h-10 w-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mb-4">
              <Bookmark className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 mb-2">Saved Question Bookmarks</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Save tricky questions, model answers, and explanations into your personal revision notebook.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs">
            <div className="h-10 w-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-4">
              <BarChart3 className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 mb-2">Real PostgreSQL Analytics</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              True database aggregation: track MCQ accuracy, average text score, and progression across roles over time.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs">
            <div className="h-10 w-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 mb-2">Private User Isolation</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              JWT sessions and database constraints guarantee your interview records and bookmarks remain strictly private.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs">
            <div className="h-10 w-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
              <BrainCircuit className="h-5 w-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 mb-2">Bounded Resilient AI</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Google Gemini with exponential retry and deterministic fallbacks ensure the app never crashes under quota limits.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto bg-slate-900 text-slate-400 py-12 border-t border-slate-800 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <div className="h-7 w-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
              <Sparkles className="h-4 w-4" />
            </div>
            <span className="font-bold text-white text-sm">MockMate</span>
            <span className="text-slate-500">| AI-Based Interview Preparation Simulator</span>
          </div>

          <div className="flex items-center gap-6">
            <span>Powered by Google Gemini</span>
            <span>FastAPI & Next.js</span>
            <a 
              href="https://github.com/sinalkarpratik3-ai/MockMate" 
              target="_blank" 
              rel="noreferrer"
              className="text-slate-300 hover:text-white transition-colors underline"
            >
              GitHub Repository
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
