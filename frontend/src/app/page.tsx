"use client";

import React from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";
import { 
  CheckCircle2, 
  ArrowRight, 
  Target, 
  BarChart3, 
  Calendar, 
  Bookmark, 
  Layers,
  Code2,
  Terminal,
  Server,
  Database,
  Cpu,
  BookOpen,
  HelpCircle,
  TrendingUp,
  FileText
} from "lucide-react";

export default function LandingPage() {
  const { user } = useAuth();

  const roles = [
    { name: "Frontend Developer", icon: Code2, desc: "Modern React architecture, TypeScript, state management, rendering performance, and web standards." },
    { name: "Backend Developer", icon: Server, desc: "RESTful architecture, caching strategies, relational data modeling, indexing, and API security." },
    { name: "Python Developer", icon: Terminal, desc: "Concurrency, asynchronous programming, memory management, generators, and clean design patterns." },
    { name: "Java Developer", icon: Cpu, desc: "Object-oriented design, JVM internals, Spring Boot ecosystem, thread safety, and concurrency." },
    { name: "DevOps Engineer", icon: Layers, desc: "Containerisation, deployment pipelines, infrastructure reliability, automation, and system monitoring." },
    { name: "Data Analyst", icon: Database, desc: "Complex SQL queries, statistical analysis, data validation, metrics definition, and insights communication." },
  ];

  return (
    <div className="min-h-screen bg-[#F7F3EA] text-[#252923] flex flex-col selection:bg-[#DCE6D8] selection:text-[#24483F]">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 sm:pt-20 sm:pb-28 bg-[#FAF8F4] border-b border-[#E8DDCA]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          
          {/* Top Focus Pill */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#EDF3EB] border border-[#DCE6D8] text-[#24483F] text-xs font-semibold mb-8">
            <span className="w-2 h-2 rounded-full bg-[#24483F]" />
            <span>Structured Technical Interview Preparation</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-[#252923] tracking-tight max-w-4xl mx-auto leading-[1.15]">
            Prepare Better. <span className="text-[#24483F]">Interview With Confidence.</span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-[#777B74] max-w-2xl mx-auto leading-relaxed">
            Practice technical interviews, test your knowledge, review your answers, and build confidence one session at a time.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href={user ? "/dashboard" : "/register"}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-[#24483F] text-[#F7F3EA] font-semibold text-base shadow-sm hover:bg-[#1A342D] transition-all"
            >
              <span>{user ? "Go to Dashboard" : "Start Practising"}</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              href="#formats"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-[#EDF3EB] text-[#24483F] font-semibold text-base hover:bg-[#DCE6D8] transition-colors border border-[#DCE6D8]"
            >
              <FileText className="h-4 w-4 text-[#24483F]" />
              <span>Explore Formats</span>
            </Link>
          </div>

          {/* Quick proof badges */}
          <div className="mt-14 pt-8 border-t border-[#E8DDCA] grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto text-[#777B74] text-xs font-medium">
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-[#367451]" />
              <span>Real Assessment Flows</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-[#367451]" />
              <span>Dual Practice Modes</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-[#367451]" />
              <span>Personalised Feedback</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-[#367451]" />
              <span>Persistent Progress</span>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 sm:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="text-xs font-bold text-[#879477] uppercase tracking-widest">How It Works</span>
          <h2 className="text-3xl font-bold text-[#252923] tracking-tight mt-1">A Deliberate Practice Method</h2>
          <p className="mt-2 text-sm text-[#777B74]">Four straightforward steps to prepare effectively for your upcoming rounds.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-[#FAF8F4] p-6 rounded-2xl border border-[#E8DDCA]">
            <div className="w-8 h-8 rounded-full bg-[#24483F] text-[#F7F3EA] flex items-center justify-center text-xs font-bold mb-4">1</div>
            <h3 className="font-bold text-base text-[#252923] mb-1.5">Choose Role & Focus</h3>
            <p className="text-xs text-[#777B74] leading-relaxed">Select your target engineering domain, difficulty level, and desired session length.</p>
          </div>
          <div className="bg-[#FAF8F4] p-6 rounded-2xl border border-[#E8DDCA]">
            <div className="w-8 h-8 rounded-full bg-[#24483F] text-[#F7F3EA] flex items-center justify-center text-xs font-bold mb-4">2</div>
            <h3 className="font-bold text-base text-[#252923] mb-1.5">Answer Thoughtfully</h3>
            <p className="text-xs text-[#777B74] leading-relaxed">Solve multiple-choice challenges or articulate structured written responses in your own words.</p>
          </div>
          <div className="bg-[#FAF8F4] p-6 rounded-2xl border border-[#E8DDCA]">
            <div className="w-8 h-8 rounded-full bg-[#24483F] text-[#F7F3EA] flex items-center justify-center text-xs font-bold mb-4">3</div>
            <h3 className="font-bold text-base text-[#252923] mb-1.5">Review Analysis</h3>
            <p className="text-xs text-[#777B74] leading-relaxed">Read detailed constructive feedback, identify missed concepts, and compare with sample answers.</p>
          </div>
          <div className="bg-[#FAF8F4] p-6 rounded-2xl border border-[#E8DDCA]">
            <div className="w-8 h-8 rounded-full bg-[#24483F] text-[#F7F3EA] flex items-center justify-center text-xs font-bold mb-4">4</div>
            <h3 className="font-bold text-base text-[#252923] mb-1.5">Refine Weak Areas</h3>
            <p className="text-xs text-[#777B74] leading-relaxed">Revisit saved bookmarks and targeted topics to steadily improve accuracy over time.</p>
          </div>
        </div>
      </section>

      {/* Practice Styles */}
      <section id="formats" className="py-16 sm:py-24 bg-[#FAF8F4] border-y border-[#E8DDCA]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-bold text-[#879477] uppercase tracking-widest">Choose Your Practice Style</span>
            <h2 className="text-3xl sm:text-4xl font-bold text-[#252923] tracking-tight mt-1">Two Complementary Assessment Formats</h2>
            <p className="mt-3 text-base text-[#777B74]">Choose the format that matches your immediate preparation goal.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Multiple Choice */}
            <div className="rounded-2xl p-8 bg-white border border-[#E8DDCA] shadow-sm hover:border-[#DCE6D8] transition-all flex flex-col justify-between">
              <div>
                <div className="h-12 w-12 rounded-xl bg-[#EDF3EB] border border-[#DCE6D8] flex items-center justify-center text-[#24483F] mb-6">
                  <Target className="h-6 w-6" />
                </div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#24483F] bg-[#EDF3EB] px-2.5 py-1 rounded-md">Option A</span>
                <h3 className="text-2xl font-bold text-[#252923] mt-3 mb-2">Multiple Choice Practice</h3>
                <p className="text-[#777B74] text-sm leading-relaxed mb-6">
                  Test your foundational knowledge, terminology, and technical precision with curated 4-option questions. Correct answers remain hidden during the test to encourage authentic recall.
                </p>

                <ul className="space-y-3 text-sm text-[#252923] mb-8">
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="h-4 w-4 text-[#367451] shrink-0 mt-0.5" />
                    <span>Clear selection interface with previous and next navigation</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="h-4 w-4 text-[#367451] shrink-0 mt-0.5" />
                    <span>Comprehensive answer keys with detailed explanations after submission</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="h-4 w-4 text-[#367451] shrink-0 mt-0.5" />
                    <span>Automatic bookmarking for questions you want to revise later</span>
                  </li>
                </ul>
              </div>

              <Link
                href="/interviews/new"
                className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-[#24483F] text-[#F7F3EA] hover:bg-[#1A342D] font-semibold text-sm transition-colors w-full shadow-sm"
              >
                <span>Practice Multiple Choice</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>

            {/* Written Answers */}
            <div className="rounded-2xl p-8 bg-white border border-[#E8DDCA] shadow-sm hover:border-[#DCE6D8] transition-all flex flex-col justify-between">
              <div>
                <div className="h-12 w-12 rounded-xl bg-[#F7ECE7] border border-[#E8DDCA] flex items-center justify-center text-[#C66A4A] mb-6">
                  <BookOpen className="h-6 w-6" />
                </div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#C66A4A] bg-[#F7ECE7] px-2.5 py-1 rounded-md">Option B</span>
                <h3 className="text-2xl font-bold text-[#252923] mt-3 mb-2">Written Answers Practice</h3>
                <p className="text-[#777B74] text-sm leading-relaxed mb-6">
                  Articulate system design trade-offs, algorithms, and architectural concepts in your own words. Receive specific feedback highlighting strengths, missed points, and ideal sample answers.
                </p>

                <ul className="space-y-3 text-sm text-[#252923] mb-8">
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="h-4 w-4 text-[#367451] shrink-0 mt-0.5" />
                    <span>Evaluates conceptual correctness, depth, clarity, and key terminology</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="h-4 w-4 text-[#367451] shrink-0 mt-0.5" />
                    <span>Constructive 0-to-10 scoring with balanced actionable suggestions</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="h-4 w-4 text-[#367451] shrink-0 mt-0.5" />
                    <span>Complete engineering sample answers for transparent comparison</span>
                  </li>
                </ul>
              </div>

              <Link
                href="/interviews/new"
                className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-[#24483F] text-[#F7F3EA] hover:bg-[#1A342D] font-semibold text-sm transition-colors w-full shadow-sm"
              >
                <span>Practice Written Answers</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Supported Roles */}
      <section className="py-16 sm:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <span className="text-xs font-bold text-[#879477] uppercase tracking-widest">Focused Tracks</span>
          <h2 className="text-3xl font-bold text-[#252923] tracking-tight mt-1">6 Practical Engineering Disciplines</h2>
          <p className="mt-2 text-sm text-[#777B74]">Tailored across Junior, Mid-Level, and Senior experience tiers.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {roles.map((role) => {
            const Icon = role.icon;
            return (
              <div key={role.name} className="p-6 rounded-xl border border-[#E8DDCA] bg-[#FAF8F4] hover:bg-white hover:border-[#DCE6D8] transition-all">
                <div className="h-10 w-10 rounded-lg bg-[#EDF3EB] text-[#24483F] flex items-center justify-center mb-4 border border-[#DCE6D8]">
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="font-bold text-base text-[#252923] mb-1">{role.name}</h3>
                <p className="text-xs text-[#777B74] leading-relaxed">{role.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Progress & Revision Features */}
      <section className="py-16 sm:py-24 bg-[#FAF8F4] border-t border-[#E8DDCA]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-bold text-[#879477] uppercase tracking-widest">Revision & Progress</span>
            <h2 className="text-3xl font-bold text-[#252923] tracking-tight mt-1">Designed for Long-Term Mastery</h2>
            <p className="mt-2 text-sm text-[#777B74]">Tools that help you identify weaknesses and track genuine improvements.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-white border border-[#E8DDCA]">
              <div className="h-10 w-10 rounded-xl bg-[#FDF1F0] text-[#B8473F] flex items-center justify-center mb-4 border border-[#E8DDCA]">
                <Target className="h-5 w-5" />
              </div>
              <h3 className="font-bold text-base text-[#252923] mb-2">Weak Topic Detection</h3>
              <p className="text-xs text-[#777B74] leading-relaxed">
                Highlights topics where your accuracy is below 60%, providing direct one-click practice sessions to target gaps.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-[#E8DDCA]">
              <div className="h-10 w-10 rounded-xl bg-[#F7ECE7] text-[#C66A4A] flex items-center justify-center mb-4 border border-[#E8DDCA]">
                <Calendar className="h-5 w-5" />
              </div>
              <h3 className="font-bold text-base text-[#252923] mb-2">Question of the Day</h3>
              <p className="text-xs text-[#777B74] leading-relaxed">
                Form a daily habit with a focused challenge every single day, keeping problem-solving sharp between full tests.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-[#E8DDCA]">
              <div className="h-10 w-10 rounded-xl bg-[#EDF3EB] text-[#24483F] flex items-center justify-center mb-4 border border-[#DCE6D8]">
                <Bookmark className="h-5 w-5" />
              </div>
              <h3 className="font-bold text-base text-[#252923] mb-2">Saved Question Notebook</h3>
              <p className="text-xs text-[#777B74] leading-relaxed">
                Bookmark important questions, explanations, and model answers into your revision notebook for quick review.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-[#E8DDCA]">
              <div className="h-10 w-10 rounded-xl bg-[#EDF3EB] text-[#24483F] flex items-center justify-center mb-4 border border-[#DCE6D8]">
                <BarChart3 className="h-5 w-5" />
              </div>
              <h3 className="font-bold text-base text-[#252923] mb-2">Performance Analytics</h3>
              <p className="text-xs text-[#777B74] leading-relaxed">
                Track MCQ accuracy trends, average written answer scores, and role-specific readiness across your entire history.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-[#E8DDCA]">
              <div className="h-10 w-10 rounded-xl bg-[#EDF3EB] text-[#367451] flex items-center justify-center mb-4 border border-[#DCE6D8]">
                <TrendingUp className="h-5 w-5" />
              </div>
              <h3 className="font-bold text-base text-[#252923] mb-2">Persistent History</h3>
              <p className="text-xs text-[#777B74] leading-relaxed">
                Every completed session is safely saved to your account so you can review previous attempts and track progress.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-[#E8DDCA]">
              <div className="h-10 w-10 rounded-xl bg-[#FAF8F4] text-[#879477] flex items-center justify-center mb-4 border border-[#E8DDCA]">
                <HelpCircle className="h-5 w-5" />
              </div>
              <h3 className="font-bold text-base text-[#252923] mb-2">Transparent Reviews</h3>
              <p className="text-xs text-[#777B74] leading-relaxed">
                Clear scoring rubrics explaining what you did well, what was missing, and how to structure stronger answers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 sm:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center w-full">
        <div className="bg-[#24483F] text-[#F7F3EA] rounded-3xl p-10 sm:p-14 shadow-md max-w-4xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight mb-4">
            Ready to prepare for your next interview?
          </h2>
          <p className="text-sm sm:text-base text-[#DCE6D8] max-w-xl mx-auto mb-8 leading-relaxed">
            Create a practice session in seconds, test your technical skills, and get practical feedback to help you succeed.
          </p>
          <Link
            href={user ? "/dashboard" : "/register"}
            className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-[#FAF8F4] text-[#24483F] font-semibold text-base hover:bg-white shadow-sm transition-all"
          >
            <span>{user ? "Go to Dashboard" : "Get Started Now"}</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto bg-[#252923] text-[#FAF8F4] py-12 border-t border-[#3D443A] text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2.5">
            <div className="h-7 w-7 rounded-lg bg-[#24483F] flex items-center justify-center text-[#F7F3EA]">
              <CheckCircle2 className="h-4 w-4" />
            </div>
            <span className="font-bold text-[#F7F3EA] text-sm">MockMate</span>
            <span className="text-[#879477]">| Interview Preparation Platform</span>
          </div>

          <div className="flex items-center gap-6 text-[#DCE6D8]">
            <Link href="/login" className="hover:text-white transition-colors">Sign In</Link>
            <Link href="/register" className="hover:text-white transition-colors">Register</Link>
            <a 
              href="https://github.com/sinalkarpratik3-ai/MockMate" 
              target="_blank" 
              rel="noreferrer"
              className="text-[#FAF8F4] hover:underline transition-colors"
            >
              GitHub Repository
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
