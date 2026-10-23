"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { User, AuthResponse } from "@/types";
import { apiRequest } from "@/lib/api";

import { useRouter } from "next/navigation";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("mockmate_token");
    }
    return null;
  });
  const [loading, setLoading] = useState<boolean>(() => {
    if (typeof window !== "undefined") {
      return Boolean(localStorage.getItem("mockmate_token"));
    }
    return false;
  });

  useEffect(() => {
    let ignore = false;
    if (token) {
      apiRequest<User>("/auth/me")
        .then((userData) => {
          if (!ignore) {
            setUser(userData);
          }
        })
        .catch((err) => {
          console.warn("Failed to fetch current user session:", err);
          if (!ignore) {
            if (typeof window !== "undefined") {
              localStorage.removeItem("mockmate_token");
            }
            setToken(null);
            setUser(null);
          }
        })
        .finally(() => {
          if (!ignore) {
            setLoading(false);
          }
        });
    }
    return () => {
      ignore = true;
    };
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await apiRequest<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (typeof window !== "undefined") {
      localStorage.setItem("mockmate_token", res.access_token);
    }
    setToken(res.access_token);
    setUser(res.user);
  };

  const register = async (email: string, password: string, fullName?: string) => {
    const res = await apiRequest<AuthResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, full_name: fullName }),
    });

    if (typeof window !== "undefined") {
      localStorage.setItem("mockmate_token", res.access_token);
    }
    setToken(res.access_token);
    setUser(res.user);
  };

  const logout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("mockmate_token");
    }
    setToken(null);
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
