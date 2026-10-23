"use client";

import React, { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { BookmarkItem } from "@/types";
import { 
  Bookmark, 
  Trash2, 
  BookOpen, 
  Filter, 
  Loader2, 
  PlusCircle,
  Search
} from "lucide-react";

export default function BookmarksPage() {
  const [bookmarks, setBookmarks] = useState<BookmarkItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [roleFilter, setRoleFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  const fetchBookmarks = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiRequest<BookmarkItem[]>("/bookmarks");
      setBookmarks(data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load saved questions.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let ignore = false;
    apiRequest<BookmarkItem[]>("/bookmarks")
      .then((data) => {
        if (!ignore) {
          setBookmarks(data);
        }
      })
      .catch((err: unknown) => {
        if (!ignore) {
          const msg = err instanceof Error ? err.message : "Failed to load saved questions.";
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

  const handleRemove = async (questionId: number) => {
    try {
      await apiRequest(`/bookmarks/${questionId}`, { method: "DELETE" });
      setBookmarks((prev) => prev.filter((b) => b.question_id !== questionId));
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to remove saved question.";
      alert(msg);
    }
  };

  const availableRoles = Array.from(new Set(bookmarks.map((b) => b.question.role)));
  const filtered = bookmarks.filter((b) => {
    const matchesRole = roleFilter === "all" || b.question.role === roleFilter;
    if (!matchesRole) return false;
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      b.question.question_text.toLowerCase().includes(q) ||
      b.question.topic.toLowerCase().includes(q) ||
      (b.question.explanation && b.question.explanation.toLowerCase().includes(q)) ||
      (b.question.model_answer && b.question.model_answer.toLowerCase().includes(q))
    );
  });

  return (
    <AppLayout>
      <div className="space-y-6 animate-fade-in pb-16">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-[#E8DDCA] pb-4">
          <div>
            <h1 className="text-2xl font-bold text-[#252923] tracking-tight flex items-center gap-2">
              <Bookmark className="h-6 w-6 text-[#24483F] fill-[#24483F]/20" />
              <span>Saved Questions</span>
            </h1>
            <p className="text-xs sm:text-sm text-[#777B74] mt-1">
              Your personal revision notebook of saved questions, explanations, and sample answers.
            </p>
          </div>

          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-[#EDF3EB] text-[#24483F] border border-[#DCE6D8] w-fit">
            {bookmarks.length} Saved Questions
          </span>
        </div>

        {/* Search & Filters Bar */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#879477]" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search saved questions, topics, concepts..."
              className="w-full pl-9 pr-4 py-2 rounded-xl border border-[#E8DDCA] bg-white text-xs text-[#252923] placeholder:text-[#879477] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F]"
            />
          </div>

          {availableRoles.length > 1 && (
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
              <Filter className="h-4 w-4 text-[#879477] shrink-0" />
              <button
                onClick={() => setRoleFilter("all")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  roleFilter === "all"
                    ? "bg-[#24483F] text-[#F7F3EA] shadow-xs"
                    : "bg-white text-[#252923] border border-[#E8DDCA] hover:bg-[#FAF8F4]"
                }`}
              >
                All Roles
              </button>
              {availableRoles.map((r) => (
                <button
                  key={r}
                  onClick={() => setRoleFilter(r)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                    roleFilter === r
                      ? "bg-[#24483F] text-[#F7F3EA] shadow-xs"
                      : "bg-white text-[#252923] border border-[#E8DDCA] hover:bg-[#FAF8F4]"
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          )}
        </div>

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-[#777B74]">
            <Loader2 className="h-8 w-8 animate-spin text-[#24483F] mb-3" />
            <p className="text-xs font-medium">Retrieving saved questions...</p>
          </div>
        ) : error ? (
          <div className="p-4 rounded-xl bg-[#FDF1F0] border border-[#E8DDCA] text-[#B8473F] text-xs flex items-center justify-between">
            <span>{error}</span>
            <button onClick={fetchBookmarks} className="font-semibold underline">Retry</button>
          </div>
        ) : filtered.length === 0 ? (
          <div className="bg-white rounded-2xl border border-[#E8DDCA] p-12 text-center max-w-md mx-auto shadow-xs">
            <Bookmark className="h-10 w-10 text-[#879477] mx-auto mb-3" />
            <h3 className="text-base font-bold text-[#252923]">No saved questions yet</h3>
            <p className="text-xs text-[#777B74] mt-1">
              While taking practice tests or reviewing answers, click the Save icon to save questions here for easy revision.
            </p>
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 mt-5 px-4 py-2 rounded-xl bg-[#24483F] text-[#F7F3EA] text-xs font-semibold shadow-xs hover:bg-[#1A342D] transition-colors"
            >
              <PlusCircle className="h-3.5 w-3.5" />
              <span>Start Practising Now</span>
            </Link>
          </div>
        ) : (
          <div className="space-y-5">
            {filtered.map((item) => {
              const q = item.question;
              const isMCQ = q.question_type === "mcq";

              return (
                <div 
                  key={item.id} 
                  className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs space-y-4"
                >
                  {/* Meta Bar */}
                  <div className="flex items-center justify-between border-b border-[#E8DDCA] pb-3">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#EDF3EB] text-[#24483F] border border-[#DCE6D8]">
                        {q.role}
                      </span>
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#FAF8F4] text-[#252923] border border-[#E8DDCA]">
                        {q.difficulty}
                      </span>
                      <span className="text-xs font-bold text-[#879477]">
                        {q.topic}
                      </span>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleRemove(q.id)}
                      className="p-1.5 rounded-lg text-[#777B74] hover:text-[#B8473F] hover:bg-[#FDF1F0] transition-colors"
                      title="Remove from saved questions"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>

                  {/* Question text */}
                  <p className="text-base font-bold text-[#252923] leading-snug">
                    {q.question_text}
                  </p>

                  {/* MCQ Options and Explanation */}
                  {isMCQ && (
                    <div className="space-y-3 pt-1">
                      {q.options && (
                        <div className="space-y-1.5">
                          {q.options.map((opt) => {
                            const isCorrect = opt.key === q.correct_option;
                            return (
                              <div
                                key={opt.key}
                                className={`p-2.5 rounded-xl border text-xs flex items-center gap-2.5 ${
                                  isCorrect 
                                    ? "bg-[#EDF3EB] border-[#DCE6D8] text-[#252923] font-semibold" 
                                    : "bg-[#FAF8F4] border-[#E8DDCA] text-[#252923]"
                                }`}
                              >
                                <span className="h-5 w-5 rounded font-bold text-[11px] bg-white border border-[#E8DDCA] flex items-center justify-center shrink-0">
                                  {opt.key}
                                </span>
                                <span className="flex-1">{opt.text}</span>
                                {isCorrect && (
                                  <span className="text-[10px] bg-[#367451] text-white px-2 py-0.5 rounded-full font-bold shrink-0">
                                    Correct Option
                                  </span>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}

                      {q.explanation && (
                        <div className="p-3.5 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] text-xs text-[#252923] leading-relaxed">
                          <span className="font-bold text-[#24483F] block mb-0.5">Explanation:</span>
                          {q.explanation}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Text Model Answer */}
                  {!isMCQ && q.model_answer && (
                    <div className="pt-2">
                      <span className="text-[11px] font-bold uppercase text-[#252923] tracking-wider flex items-center gap-1.5 mb-1.5">
                        <BookOpen className="h-3.5 w-3.5 text-[#24483F]" />
                        Sample Answer
                      </span>
                      <div className="p-4 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] text-xs text-[#252923] leading-relaxed whitespace-pre-line font-sans">
                        {q.model_answer}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </AppLayout>
  );
}
