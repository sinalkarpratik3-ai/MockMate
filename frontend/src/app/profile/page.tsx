"use client";

import React from "react";
import AppLayout from "@/components/AppLayout";
import { useAuth } from "@/context/AuthContext";
import { 
  UserCircle, 
  LogOut, 
  ShieldCheck, 
  Mail, 
  Calendar,
  KeyRound
} from "lucide-react";

export default function ProfilePage() {
  const { user, logout } = useAuth();

  return (
    <AppLayout>
      <div className="max-w-3xl mx-auto space-y-8 animate-fade-in pb-16">
        {/* Header */}
        <div className="border-b border-[#E8DDCA] pb-4">
          <h1 className="text-2xl font-bold text-[#252923] tracking-tight flex items-center gap-2">
            <UserCircle className="h-6 w-6 text-[#24483F]" />
            <span>Profile & Account Settings</span>
          </h1>
          <p className="text-xs sm:text-sm text-[#777B74] mt-1">
            Manage your account information and practice session preferences.
          </p>
        </div>

        {/* Profile Card */}
        <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 sm:p-8 shadow-xs space-y-6">
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 rounded-2xl bg-[#24483F] text-[#F7F3EA] font-bold text-2xl flex items-center justify-center shadow-sm">
              {user?.full_name ? user.full_name.charAt(0).toUpperCase() : user?.email.charAt(0).toUpperCase()}
            </div>
            <div>
              <h2 className="text-lg font-bold text-[#252923]">{user?.full_name || "Technical Candidate"}</h2>
              <p className="text-xs text-[#777B74] flex items-center gap-1.5 mt-0.5">
                <Mail className="h-3.5 w-3.5" />
                <span>{user?.email}</span>
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-[#E8DDCA] text-xs">
            <div className="p-3.5 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA]">
              <span className="font-semibold text-[#879477] block mb-0.5">Account ID</span>
              <span className="font-mono text-[#252923]">#{user?.id}</span>
            </div>

            <div className="p-3.5 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA]">
              <span className="font-semibold text-[#879477] block mb-0.5">Account Created</span>
              <span className="text-[#252923] flex items-center gap-1">
                <Calendar className="h-3.5 w-3.5 text-[#879477]" />
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "Active Session"}
              </span>
            </div>
          </div>
        </div>

        {/* Account Privacy & Security */}
        <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 sm:p-8 shadow-xs space-y-4">
          <h2 className="text-base font-bold text-[#252923] flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-[#24483F]" />
            <span>Account Privacy & Security</span>
          </h2>

          <div className="space-y-3 text-xs text-[#252923]">
            <div className="p-3.5 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] flex items-start gap-3">
              <KeyRound className="h-4 w-4 text-[#24483F] shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-[#252923]">Encrypted Authentication</p>
                <p className="text-[11px] text-[#777B74] mt-0.5">
                  Your credentials and practice sessions are secured with industry-standard encryption and token authentication.
                </p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-[#FAF8F4] border border-[#E8DDCA] flex items-start gap-3">
              <ShieldCheck className="h-4 w-4 text-[#24483F] shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-[#252923]">Private Practice Records</p>
                <p className="text-[11px] text-[#777B74] mt-0.5">
                  Your interview history, scores, written answers, and saved bookmarks are isolated and accessible only to your account.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Sign Out Card */}
        <div className="bg-white rounded-2xl border border-[#E8DDCA] p-6 shadow-xs flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-[#252923]">Sign Out of MockMate</h3>
            <p className="text-xs text-[#777B74] mt-0.5">End your authenticated session on this device.</p>
          </div>

          <button
            type="button"
            onClick={logout}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#FDF1F0] hover:bg-[#FCE6E4] text-[#B8473F] font-semibold text-xs border border-[#E8DDCA] transition-colors"
          >
            <LogOut className="h-4 w-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </AppLayout>
  );
}
