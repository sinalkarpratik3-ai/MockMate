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
  CheckCircle2,
  BookOpen
} from "lucide-react";

interface SidebarProps {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Practice Interview", href: "/interviews/new", icon: PlayCircle },
  { label: "Practice History", href: "/history", icon: History },
  { label: "Question of the Day", href: "/daily", icon: Calendar },
  { label: "Saved Questions", href: "/bookmarks", icon: Bookmark },
  { label: "Your Progress", href: "/analytics", icon: BarChart2 },
  { label: "Profile & Settings", href: "/profile", icon: UserCircle },
];

export default function Sidebar({ mobileOpen, onCloseMobile }: SidebarProps) {
  const pathname = usePathname();

  const navContent = (
    <div className="flex flex-col h-full bg-[#FAF8F4] border-r border-[#E8DDCA] w-64">
      {/* Brand area for mobile */}
      <div className="flex items-center justify-between p-4 border-b border-[#E8DDCA] lg:hidden">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-[#24483F] flex items-center justify-center text-[#F7F3EA]">
            <CheckCircle2 className="h-4 w-4" />
          </div>
          <span className="font-bold text-[#252923]">MockMate</span>
        </div>
        {onCloseMobile && (
          <button
            onClick={onCloseMobile}
            className="p-1 rounded-lg text-[#777B74] hover:text-[#252923] hover:bg-[#EDF3EB]"
          >
            <X className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Navigation links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[11px] font-semibold text-[#879477] uppercase tracking-wider">
          Practice Workspace
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
                  ? "bg-[#DCE6D8] text-[#24483F] font-semibold shadow-xs"
                  : "text-[#252923] hover:text-[#24483F] hover:bg-[#EDF3EB]"
              }`}
            >
              <Icon className={`h-4 w-4 ${isActive ? "text-[#24483F]" : "text-[#879477]"}`} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Bottom prompt box */}
      <div className="p-4 border-t border-[#E8DDCA] bg-[#FAF8F4]">
        <div className="rounded-xl p-3 bg-[#EDF3EB] border border-[#DCE6D8] text-[#252923]">
          <div className="flex items-center gap-2 mb-1">
            <BookOpen className="h-3.5 w-3.5 text-[#24483F]" />
            <span className="text-[11px] font-semibold tracking-wide text-[#24483F]">Daily Practice</span>
          </div>
          <p className="text-[11px] text-[#777B74] leading-relaxed">
            Consistently testing key concepts and reviewing sample answers builds lasting interview confidence.
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
            className="fixed inset-0 bg-[#252923]/40 backdrop-blur-xs transition-opacity" 
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
