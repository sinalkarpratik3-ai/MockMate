"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { 
  CheckCircle2, 
  User as UserIcon, 
  LogOut, 
  Menu, 
  PlusCircle, 
  Calendar,
  Bookmark,
  BarChart3,
  History
} from "lucide-react";

interface NavbarProps {
  onMobileMenuToggle?: () => void;
}

export default function Navbar({ onMobileMenuToggle }: NavbarProps) {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#E8DDCA] bg-[#FAF8F4]/95 backdrop-blur-md">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Left: Mobile hamburger & Logo */}
        <div className="flex items-center gap-3">
          {onMobileMenuToggle && (
            <button
              onClick={onMobileMenuToggle}
              className="lg:hidden p-2 rounded-lg text-[#252923] hover:text-[#24483F] hover:bg-[#EDF3EB] focus:outline-none transition-colors"
              aria-label="Toggle navigation menu"
            >
              <Menu className="h-6 w-6" />
            </button>
          )}

          <Link href={user ? "/dashboard" : "/"} className="flex items-center gap-2.5 group">
            <div className="h-9 w-9 rounded-xl bg-[#24483F] flex items-center justify-center text-[#F7F3EA] shadow-sm shadow-[#24483F]/20 group-hover:bg-[#1A342D] transition-colors">
              <CheckCircle2 className="h-5 w-5" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg tracking-tight text-[#252923]">
                Mock<span className="text-[#24483F]">Mate</span>
              </span>
              <span className="text-[10px] -mt-1 font-semibold text-[#879477] tracking-wider uppercase">
                Interview Platform
              </span>
            </div>
          </Link>
        </div>

        {/* Center / Right actions */}
        <div className="flex items-center gap-3 sm:gap-4">
          {user ? (
            <>
              <Link
                href="/daily"
                className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-[#C66A4A] bg-[#F7ECE7] border border-[#E8DDCA] rounded-full hover:bg-[#F3DFD8] transition-colors"
              >
                <Calendar className="h-3.5 w-3.5" />
                <span>Daily Challenge</span>
              </Link>

              <Link
                href="/interviews/new"
                className="flex items-center gap-1.5 px-3.5 py-1.5 text-sm font-semibold text-[#F7F3EA] bg-[#24483F] hover:bg-[#1A342D] rounded-lg shadow-sm transition-all"
              >
                <PlusCircle className="h-4 w-4" />
                <span className="hidden xs:inline">Start Practising</span>
              </Link>

              {/* User Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-[#EDF3EB] transition-colors focus:outline-none"
                  aria-expanded={dropdownOpen}
                >
                  <div className="h-8 w-8 rounded-full bg-[#DCE6D8] border border-[#C6D4C0] flex items-center justify-center text-[#24483F] font-semibold text-xs">
                    {user.full_name ? user.full_name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                  </div>
                  <span className="hidden md:inline text-xs font-medium text-[#252923] max-w-[120px] truncate">
                    {user.full_name || user.email.split("@")[0]}
                  </span>
                </button>

                {dropdownOpen && (
                  <div 
                    className="absolute right-0 mt-2 w-56 rounded-xl bg-white p-2 shadow-xl border border-[#E8DDCA] z-50 animate-in fade-in slide-in-from-top-2 duration-150"
                    onMouseLeave={() => setDropdownOpen(false)}
                  >
                    <div className="px-3 py-2 border-b border-[#E8DDCA] mb-1">
                      <p className="text-xs font-semibold text-[#252923] truncate">{user.full_name || "User"}</p>
                      <p className="text-[11px] text-[#777B74] truncate">{user.email}</p>
                    </div>

                    <Link
                      href="/dashboard"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-[#252923] rounded-lg hover:bg-[#EDF3EB] hover:text-[#24483F] transition-colors"
                    >
                      <BarChart3 className="h-4 w-4 text-[#879477]" />
                      Dashboard
                    </Link>

                    <Link
                      href="/history"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-[#252923] rounded-lg hover:bg-[#EDF3EB] hover:text-[#24483F] transition-colors"
                    >
                      <History className="h-4 w-4 text-[#879477]" />
                      Practice History
                    </Link>

                    <Link
                      href="/bookmarks"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-[#252923] rounded-lg hover:bg-[#EDF3EB] hover:text-[#24483F] transition-colors"
                    >
                      <Bookmark className="h-4 w-4 text-[#879477]" />
                      Saved Questions
                    </Link>

                    <Link
                      href="/profile"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-[#252923] rounded-lg hover:bg-[#EDF3EB] hover:text-[#24483F] transition-colors"
                    >
                      <UserIcon className="h-4 w-4 text-[#879477]" />
                      Profile & Settings
                    </Link>

                    <div className="border-t border-[#E8DDCA] my-1 pt-1">
                      <button
                        onClick={() => {
                          setDropdownOpen(false);
                          logout();
                        }}
                        className="w-full flex items-center gap-2 px-3 py-2 text-xs text-[#B8473F] rounded-lg hover:bg-[#FDF1F0] transition-colors text-left font-medium"
                      >
                        <LogOut className="h-4 w-4" />
                        Sign Out
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2 sm:gap-3">
              <Link
                href="/login"
                className="px-3.5 py-1.5 text-sm font-medium text-[#252923] hover:text-[#24483F] transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-4 py-1.5 text-sm font-semibold text-[#F7F3EA] bg-[#24483F] hover:bg-[#1A342D] rounded-lg shadow-sm transition-all"
              >
                Start Practising
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
