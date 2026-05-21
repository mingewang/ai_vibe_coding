"use client";

// ============================================================
// ProtectedRoute — wraps pages that require a logged-in user
// ============================================================
// If the user is not authenticated, it redirects to the login page.
// Shows a loading spinner while checking auth state.
// ============================================================

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import LoadingSpinner from "./LoadingSpinner";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth/login");
    }
  }, [user, loading, router]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    return null; // Don't render anything while redirecting
  }

  return <>{children}</>;
}
