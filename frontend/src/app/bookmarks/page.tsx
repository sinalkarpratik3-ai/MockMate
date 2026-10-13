"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { apiRequest } from "@/lib/api";
import { BookmarkItem } from "@/types";
import { 
  Bookmark, 
  Trash2, 
  BookOpen, 
  CheckCircle2, 
  Filter, 
  Loader2, 
  AlertCircle,
  PlusCircle
} from "lucide-react";

export default function BookmarksPage() {
  const [bookmarks, setBookmarks] = useState<BookmarkItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [roleFilter, setRoleFilter] = useState("all");

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiRequest<BookmarkItem[]>("/bookmarks");
      setBookmarks(data);
    } catch (err: any) {
      setError(err.message || "Failed to load bookmarks.");
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (questionId: number) => {
    try {
      await apiRequest(`/bookmarks/${questionId}`, { method: "DELETE" });
      setBookmarks((prev) => prev.filter((b) => b.question_id !== questionId));
    } catch (err: any) {
      alert(err.message || "Failed to remove bookmark.");
    }
  };

  const availableRoles = Array.from(new Set(bookmarks.map((b) => b.question.role)));
  const filtered = bookmarks.filter((b) => {
    if (roleFilter === "all") return true;
    return b.question.role === roleFilter;
  });

  return (
    <AppLayout>
      <div className="space-y-6 animate-fade-in pb-16">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <Bookmark className="h-6 w-6 text-indigo-600 fill-indigo-600/20" />
              <span>Saved Questions & Revision Notebook</span>
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Your personal library of bookmarked questions, explanations, and model answers.
            </p>
          </div>

          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 w-fit">
            {bookmarks.length} Bookmarks Saved
          </span>
        </div>

        {/* Filters */}
        {availableRoles.length > 1 && (
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-slate-400" />
            <span className="text-xs font-semibold text-slate-500">Filter Role:</span>
            <button
              onClick={() => setRoleFilter("all")}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                roleFilter === "all"
                  ? "bg-indigo-600 text-white shadow-xs"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
              }`}
            >
              All Roles
            </button>
            {availableRoles.map((r) => (
              <button
                key={r}
                onClick={() => setRoleFilter(r)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  roleFilter === r
                    ? "bg-indigo-600 text-white shadow-xs"
                    : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
                }`}
              >
                {r}
              </button>
            ))}
          </div>
        )}

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-600 mb-3" />
            <p className="text-xs font-medium">Retrieving saved questions...</p>
          </div>
        ) : error ? (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center justify-between">
            <span>{error}</span>
            <button onClick={fetchBookmarks} className="font-semibold underline">Retry</button>
          </div>
        ) : filtered.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-md mx-auto shadow-xs">
            <Bookmark className="h-10 w-10 text-slate-300 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-900">No saved questions yet</h3>
            <p className="text-xs text-slate-500 mt-1">
              While taking interviews or reviewing results, click the Bookmark icon to save questions here for easy revision.
            </p>
            <Link
              href="/interviews/new"
              className="inline-flex items-center gap-1.5 mt-5 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold shadow-xs hover:bg-indigo-700 transition-colors"
            >
              <PlusCircle className="h-3.5 w-3.5" />
              <span>Practice Questions Now</span>
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
                  className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4"
                >
                  {/* Meta Bar */}
                  <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700">
                        {q.role}
                      </span>
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                        {q.difficulty}
                      </span>
                      <span className="text-xs font-bold text-indigo-600">
                        {q.topic}
                      </span>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleRemove(q.id)}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                      title="Remove from saved questions"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>

                  {/* Question text */}
                  <p className="text-base font-bold text-slate-900 leading-snug">
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
                                    ? "bg-emerald-50/70 border-emerald-300 text-emerald-900 font-semibold" 
                                    : "bg-slate-50/50 border-slate-200 text-slate-700"
                                }`}
                              >
                                <span className="h-5 w-5 rounded font-bold text-[11px] bg-white border border-slate-200 flex items-center justify-center shrink-0">
                                  {opt.key}
                                </span>
                                <span className="flex-1">{opt.text}</span>
                                {isCorrect && (
                                  <span className="text-[10px] bg-emerald-600 text-white px-2 py-0.5 rounded-full font-bold shrink-0">
                                    Correct Option
                                  </span>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}

                      {q.explanation && (
                        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 leading-relaxed">
                          <span className="font-bold text-slate-900 block mb-0.5">Explanation:</span>
                          {q.explanation}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Text Model Answer */}
                  {!isMCQ && q.model_answer && (
                    <div className="pt-2">
                      <span className="text-[11px] font-bold uppercase text-slate-700 tracking-wider flex items-center gap-1.5 mb-1.5">
                        <BookOpen className="h-3.5 w-3.5 text-indigo-600" />
                        Engineering Model Answer
                      </span>
                      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 leading-relaxed whitespace-pre-line font-sans">
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
