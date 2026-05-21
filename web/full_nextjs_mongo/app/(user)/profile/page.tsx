"use client";

// ============================================================
// ProfilePage (/profile) — view user account information
// ============================================================

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import LoadingSpinner from "@/components/LoadingSpinner";
import ProtectedRoute from "@/components/ProtectedRoute";

function ProfileContent() {
  const { user } = useAuth();

  if (!user) return <LoadingSpinner />;

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">My Profile</h1>

      <div className="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-500">Name</label>
          <p className="text-gray-900 text-lg">{user.name}</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-500">Email</label>
          <p className="text-gray-900 text-lg">{user.email}</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-500">Role</label>
          <p className="text-gray-900 text-lg capitalize">{user.role}</p>
        </div>
        {user.createdAt && (
          <div>
            <label className="block text-sm font-medium text-gray-500">
              Member since
            </label>
            <p className="text-gray-900 text-lg">
              {new Date(user.createdAt).toLocaleDateString()}
            </p>
          </div>
        )}
      </div>

      <div className="mt-6 flex gap-4">
        <Link
          href="/orders"
          className="text-primary-600 hover:underline"
        >
          View My Orders
        </Link>
        <Link
          href="/products"
          className="text-primary-600 hover:underline"
        >
          Browse Products
        </Link>
      </div>
    </div>
  );
}

export default function ProfilePage() {
  return (
    <ProtectedRoute>
      <ProfileContent />
    </ProtectedRoute>
  );
}
