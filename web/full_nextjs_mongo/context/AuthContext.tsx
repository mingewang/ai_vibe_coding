"use client";

// ============================================================
// AuthContext — manages login/logout state across the app
// ============================================================
// This context provides:
//   - user: the currently logged-in user (null if not logged in)
//   - loading: true while we check the saved token on page load
//   - login(email, password): logs in and stores the JWT
//   - register(name, email, password): creates an account
//   - logout(): clears the session
//   - isAdmin: true if the user has the admin role
//
// Usage: wrap your app layout with <AuthProvider>
//        then use `const { user, login, logout } = useAuth()`
//        in any child component.
// ============================================================

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { IUser, IApiResponse } from "@/types";

// The shape of what our context provides
interface AuthContextType {
  user: IUser | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<IApiResponse<IUser>>;
  register: (name: string, email: string, password: string) => Promise<IApiResponse<IUser>>;
  logout: () => void;
  isAdmin: boolean;
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Helper: get the token from localStorage
function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

// Helper: store the token
function setToken(token: string): void {
  localStorage.setItem("token", token);
}

// Helper: remove the token
function removeToken(): void {
  localStorage.removeItem("token");
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<IUser | null>(null);
  const [loading, setLoading] = useState(true);

  // On page load, check if we have a saved token and fetch user data
  useEffect(() => {
    const token = getToken();
    if (!token) {
      setLoading(false);
      return;
    }

    fetch("/api/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data: IApiResponse<IUser>) => {
        if (data.data) {
          setUser(data.data);
        } else {
          removeToken(); // Token is invalid, clear it
        }
      })
      .catch(() => {
        removeToken();
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // Login: send credentials, get back a token + user data
  const login = useCallback(async (email: string, password: string): Promise<IApiResponse<IUser>> => {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data: IApiResponse<IUser> & { token?: string } = await res.json();

    if (data.token && data.data) {
      setToken(data.token);
      setUser(data.data);
    }

    return data;
  }, []);

  // Register: create a new account
  const register = useCallback(
    async (name: string, email: string, password: string): Promise<IApiResponse<IUser>> => {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data: IApiResponse<IUser> & { token?: string } = await res.json();

      if (data.token && data.data) {
        setToken(data.token);
        setUser(data.data);
      }

      return data;
    },
    []
  );

  // Logout: clear everything
  const logout = useCallback(() => {
    removeToken();
    setUser(null);
  }, []);

  const isAdmin = user?.role === "admin";

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, isAdmin }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook — use this in components to access auth state
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside an <AuthProvider>");
  }
  return context;
}
