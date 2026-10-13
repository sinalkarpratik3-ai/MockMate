"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  PlayCircle, 
  History, 
  Calendar, 
  Bookmark, 
  BarChart2, 
  UserCircle,
  X,
  Sparkles
} from "lucide-react";

interface SidebarProps {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Start Interview", href: "/interviews/new", icon: PlayCircle },
  { label: "Interview History", href: "/history", icon: History },
  { label: "Question of the Day", href: "/daily", icon: Calendar },
  { label: "Saved Questions", href: "/bookmarks", icon: Bookmark },
  { label: "Progress Analytics", href: "/analytics", icon: BarChart2 },
  { label: "Profile & Settings", href: "/profile", icon: UserCircle },
];

export default function Sidebar({ mobileOpen, onCloseMobile }: SidebarProps) {
  const pathname = usePathname();

  const navContent = (
    <div className="flex flex-col h-full bg-white border-r border-slate-200 w-64">
      {/* Brand area for mobile */}
      <div className="flex items-center justify-between p-4 border-b border-slate-200 lg:hidden">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="font-bold text-slate-900">MockMate</span>
        </div>
        {onCloseMobile && (
          <button
            onClick={onCloseMobile}
            className="p-1 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100"
          >
            <X className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Navigation links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
          Practice & Evaluation
        </div>
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onCloseMobile}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? "bg-indigo-50 text-indigo-700 font-semibold shadow-xs shadow-indigo-100"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
              }`}
            >
              <Icon className={`h-4 w-4 ${isActive ? "text-indigo-600" : "text-slate-400"}`} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Bottom prompt box */}
      <div className="p-4 border-t border-slate-100 bg-slate-50/50">
        <div className="rounded-xl p-3 bg-gradient-to-br from-indigo-500 to-blue-600 text-white shadow-sm">
          <div className="flex items-center gap-2 mb-1.5">
            <Sparkles className="h-3.5 w-3.5 text-amber-300" />
            <span className="text-[11px] font-bold uppercase tracking-wide">Gemini 3.8 AI</span>
          </div>
          <p className="text-[11px] text-indigo-100 leading-snug">
            AI-powered question generation and deep answer evaluations active.
          </p>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop static sidebar */}
      <aside className="hidden lg:block shrink-0 sticky top-16 h-[calc(100vh-4rem)] z-30">
        {navContent}
      </aside>

      {/* Mobile drawer backdrop and overlay */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div 
            className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs transition-opacity" 
            onClick={onCloseMobile} 
          />
          <div className="fixed inset-y-0 left-0 w-64 z-50 shadow-2xl animate-in slide-in-from-left duration-200">
            {navContent}
          </div>
        </div>
      )}
    </>
  );
}
