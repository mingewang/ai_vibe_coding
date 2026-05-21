"use client";

// ============================================================
// RegisterPage (/auth/register) — sign up form
// ============================================================

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import AuthForm from "@/components/AuthForm";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (name: string, email: string, password: string) => {
    setError("");
    setLoading(true);

    const result = await register(name, email, password);

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
        Create an Account
      </h1>
      <div className="bg-white border border-gray-200 rounded-xl p-8">
        <AuthForm
          mode="register"
          onSubmit={handleRegister}
          error={error}
          loading={loading}
        />
        <p className="text-center text-sm text-gray-500 mt-6">
          Already have an account?{" "}
          <Link href="/auth/login" className="text-primary-600 hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
