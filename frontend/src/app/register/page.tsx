"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { CheckCircle2, AlertCircle, Loader2, ArrowRight } from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const { register, user } = useAuth();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      router.push("/dashboard");
    }
  }, [user, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match. Please verify.");
      return;
    }

    setLoading(true);
    try {
      await register(email, password, fullName.trim() || undefined);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to create account. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F7F3EA] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link href="/" className="inline-flex items-center gap-2.5 group mb-4">
          <div className="h-10 w-10 rounded-xl bg-[#24483F] flex items-center justify-center text-[#F7F3EA] shadow-sm">
            <CheckCircle2 className="h-5 w-5" />
          </div>
          <span className="font-extrabold text-2xl text-[#252923] tracking-tight">
            Mock<span className="text-[#24483F]">Mate</span>
          </span>
        </Link>
        <h2 className="text-2xl font-bold text-[#252923] tracking-tight">Create your account</h2>
        <p className="mt-1 text-xs text-[#777B74]">
          Start practising technical interview questions and building confidence.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div className="bg-white py-8 px-6 sm:px-10 rounded-2xl border border-[#E8DDCA] shadow-sm">
          {error && (
            <div className="mb-6 p-3.5 rounded-xl bg-[#FDF1F0] border border-[#E8DDCA] text-[#B8473F] text-xs flex items-start gap-2.5">
              <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-[#252923] mb-1.5" htmlFor="fullName">
                Full Name (Optional)
              </label>
              <input
                id="fullName"
                type="text"
                autoComplete="name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Jane Developer"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[#E8DDCA] text-sm text-[#252923] placeholder:text-[#879477] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F] transition-all bg-[#FAF8F4] focus:bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-[#252923] mb-1.5" htmlFor="email">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="developer@example.com"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[#E8DDCA] text-sm text-[#252923] placeholder:text-[#879477] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F] transition-all bg-[#FAF8F4] focus:bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-[#252923] mb-1.5" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                autoComplete="new-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 6 characters"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[#E8DDCA] text-sm text-[#252923] placeholder:text-[#879477] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F] transition-all bg-[#FAF8F4] focus:bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-[#252923] mb-1.5" htmlFor="confirmPassword">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                autoComplete="new-password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Repeat password"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[#E8DDCA] text-sm text-[#252923] placeholder:text-[#879477] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:border-[#24483F] transition-all bg-[#FAF8F4] focus:bg-white"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 mt-2 px-4 py-2.5 rounded-xl bg-[#24483F] text-[#F7F3EA] font-semibold text-sm hover:bg-[#1A342D] focus:outline-none focus:ring-2 focus:ring-[#24483F] focus:ring-offset-2 transition-all shadow-sm disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Creating Account...</span>
                </>
              ) : (
                <>
                  <span>Create Account</span>
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-[#E8DDCA] text-center">
            <p className="text-xs text-[#777B74]">
              Already have an account?{" "}
              <Link href="/login" className="font-semibold text-[#24483F] hover:underline transition-colors">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
