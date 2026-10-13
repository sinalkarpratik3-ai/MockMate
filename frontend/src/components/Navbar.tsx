"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { 
  Sparkles, 
  User as UserIcon, 
  LogOut, 
  Menu, 
  X, 
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
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur-md">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Left: Mobile hamburger & Logo */}
        <div className="flex items-center gap-3">
          {onMobileMenuToggle && (
            <button
              onClick={onMobileMenuToggle}
              className="lg:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 focus:outline-none"
              aria-label="Toggle navigation menu"
            >
              <Menu className="h-6 w-6" />
            </button>
          )}

          <Link href={user ? "/dashboard" : "/"} className="flex items-center gap-2.5 group">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
              <Sparkles className="h-5 w-5" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg tracking-tight text-slate-900">
                Mock<span className="text-indigo-600">Mate</span>
              </span>
              <span className="text-[10px] -mt-1 font-semibold text-slate-400 tracking-wider uppercase">
                Interview Simulator
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
                className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-amber-700 bg-amber-50 border border-amber-200/80 rounded-full hover:bg-amber-100 transition-colors"
              >
                <Calendar className="h-3.5 w-3.5" />
                <span>Daily Challenge</span>
              </Link>

              <Link
                href="/interviews/new"
                className="flex items-center gap-1.5 px-3.5 py-1.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-sm shadow-indigo-600/20 transition-all hover:shadow"
              >
                <PlusCircle className="h-4 w-4" />
                <span className="hidden xs:inline">New Interview</span>
              </Link>

              {/* User Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-slate-100 transition-colors focus:outline-none"
                  aria-expanded={dropdownOpen}
                >
                  <div className="h-8 w-8 rounded-full bg-slate-100 border border-slate-300 flex items-center justify-center text-slate-700 font-semibold text-xs">
                    {user.full_name ? user.full_name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                  </div>
                  <span className="hidden md:inline text-xs font-medium text-slate-700 max-w-[120px] truncate">
                    {user.full_name || user.email.split("@")[0]}
                  </span>
                </button>

                {dropdownOpen && (
                  <div 
                    className="absolute right-0 mt-2 w-56 rounded-xl bg-white p-2 shadow-xl border border-slate-100 z-50 animate-in fade-in slide-in-from-top-2 duration-150"
                    onMouseLeave={() => setDropdownOpen(false)}
                  >
                    <div className="px-3 py-2 border-b border-slate-100 mb-1">
                      <p className="text-xs font-semibold text-slate-900 truncate">{user.full_name || "User"}</p>
                      <p className="text-[11px] text-slate-500 truncate">{user.email}</p>
                    </div>

                    <Link
                      href="/dashboard"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-slate-700 rounded-lg hover:bg-slate-50 hover:text-indigo-600 transition-colors"
                    >
                      <BarChart3 className="h-4 w-4" />
                      Dashboard
                    </Link>

                    <Link
                      href="/history"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-slate-700 rounded-lg hover:bg-slate-50 hover:text-indigo-600 transition-colors"
                    >
                      <History className="h-4 w-4" />
                      Interview History
                    </Link>

                    <Link
                      href="/bookmarks"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-slate-700 rounded-lg hover:bg-slate-50 hover:text-indigo-600 transition-colors"
                    >
                      <Bookmark className="h-4 w-4" />
                      Saved Questions
                    </Link>

                    <Link
                      href="/profile"
                      onClick={() => setDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-slate-700 rounded-lg hover:bg-slate-50 hover:text-indigo-600 transition-colors"
                    >
                      <UserIcon className="h-4 w-4" />
                      Profile & Settings
                    </Link>

                    <div className="border-t border-slate-100 my-1 pt-1">
                      <button
                        onClick={() => {
                          setDropdownOpen(false);
                          logout();
                        }}
                        className="w-full flex items-center gap-2 px-3 py-2 text-xs text-rose-600 rounded-lg hover:bg-rose-50 transition-colors text-left font-medium"
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
                className="px-3.5 py-1.5 text-sm font-medium text-slate-700 hover:text-slate-900 transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-4 py-1.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-sm shadow-indigo-600/20 transition-all"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
