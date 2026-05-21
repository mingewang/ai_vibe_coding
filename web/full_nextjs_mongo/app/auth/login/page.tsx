"use client";

// ============================================================
// LoginPage (/auth/login) — login form
// ============================================================

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import AuthForm from "@/components/AuthForm";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (_name: string, email: string, password: string) => {
    setError("");
    setLoading(true);

    const result = await login(email, password);

    if (result.error) {
      setError(result.error);
      setLoading(false);
    } else {
      // Redirect to home on success
      router.push("/");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12">
      <h1 className="text-2xl font-bold text-gray-900 text-center mb-8">
        Log In
      </h1>
      <div className="bg-white border border-gray-200 rounded-xl p-8">
        <AuthForm
          mode="login"
          onSubmit={handleLogin}
          error={error}
          loading={loading}
        />
        <p className="text-center text-sm text-gray-500 mt-6">
          Don&apos;t have an account?{" "}
          <Link href="/auth/register" className="text-primary-600 hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
