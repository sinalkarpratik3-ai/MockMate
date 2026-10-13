"use client";

import React from "react";
import AppLayout from "@/components/AppLayout";
import { useAuth } from "@/context/AuthContext";
import { 
  UserCircle, 
  LogOut, 
  ShieldCheck, 
  Server, 
  Sparkles, 
  Database,
  Calendar,
  Mail,
  CheckCircle2
} from "lucide-react";

export default function ProfilePage() {
  const { user, logout } = useAuth();

  return (
    <AppLayout>
      <div className="max-w-3xl mx-auto space-y-8 animate-fade-in pb-16">
        {/* Header */}
        <div className="border-b border-slate-200 pb-4">
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <UserCircle className="h-6 w-6 text-indigo-600" />
            <span>Profile & Account Settings</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Manage your developer profile and inspect runtime configuration.
          </p>
        </div>

        {/* Profile Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs space-y-6">
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 rounded-2xl bg-indigo-600 text-white font-bold text-2xl flex items-center justify-center shadow-md shadow-indigo-600/20">
              {user?.full_name ? user.full_name.charAt(0).toUpperCase() : user?.email.charAt(0).toUpperCase()}
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">{user?.full_name || "Technical Candidate"}</h2>
              <p className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
                <Mail className="h-3.5 w-3.5" />
                <span>{user?.email}</span>
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-100 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-semibold text-slate-400 block mb-0.5">Account ID</span>
              <span className="font-mono text-slate-800">#{user?.id}</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-semibold text-slate-400 block mb-0.5">Account Created</span>
              <span className="text-slate-800">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "Active Session"}
              </span>
            </div>
          </div>
        </div>

        {/* System & Architecture Specifications Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Server className="h-5 w-5 text-indigo-600" />
            <span>Platform Engine Specifications</span>
          </h2>

          <div className="space-y-3 text-xs text-slate-700">
            <div className="p-3 rounded-xl border border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <Sparkles className="h-4 w-4 text-indigo-600" />
                <span className="font-semibold">AI Runtime Model</span>
              </div>
              <span className="font-mono text-[11px] bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded font-semibold">
                Google Gemini API (Configurable)
              </span>
            </div>

            <div className="p-3 rounded-xl border border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <Database className="h-4 w-4 text-emerald-600" />
                <span className="font-semibold">Database Engine</span>
              </div>
              <span className="font-mono text-[11px] bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded font-semibold">
                PostgreSQL (Render Managed)
              </span>
            </div>

            <div className="p-3 rounded-xl border border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <ShieldCheck className="h-4 w-4 text-blue-600" />
                <span className="font-semibold">Security Strategy</span>
              </div>
              <span className="font-mono text-[11px] bg-blue-50 text-blue-700 px-2 py-0.5 rounded font-semibold">
                Bcrypt + JWT (HS256) Data Isolation
              </span>
            </div>
          </div>
        </div>

        {/* Sign Out Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Sign Out of MockMate</h3>
            <p className="text-xs text-slate-500 mt-0.5">End your authenticated session on this browser.</p>
          </div>

          <button
            type="button"
            onClick={logout}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold text-xs border border-rose-200/80 transition-colors"
          >
            <LogOut className="h-4 w-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </AppLayout>
  );
}
