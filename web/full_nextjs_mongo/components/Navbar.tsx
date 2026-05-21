"use client";

// ============================================================
// Navbar — top navigation bar shown on every page
// ============================================================
// Shows logo, navigation links, cart badge, and login/logout.
// Adapts based on auth state (logged in vs visitor).
// ============================================================

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useCart } from "@/context/CartContext";

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth();
  const { itemCount } = useCart();

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo / Site Name */}
          <Link href="/" className="text-xl font-bold text-primary-600">
            ShopNext
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-6">
            <Link href="/products" className="text-gray-600 hover:text-primary-600">
              Products
            </Link>

            {/* Cart link (always visible) */}
            <Link href="/cart" className="relative text-gray-600 hover:text-primary-600">
              Cart
              {itemCount > 0 && (
                <span className="absolute -top-2 -right-4 bg-primary-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {itemCount > 99 ? "99+" : itemCount}
                </span>
              )}
            </Link>

            {/* Auth-dependent links */}
            {user ? (
              <>
                <Link href="/orders" className="text-gray-600 hover:text-primary-600">
                  Orders
                </Link>
                <Link href="/profile" className="text-gray-600 hover:text-primary-600">
                  Profile
                </Link>
                {isAdmin && (
                  <Link
                    href="/admin/products"
                    className="text-purple-600 hover:text-purple-800 font-medium"
                  >
                    Admin
                  </Link>
                )}
                <button
                  onClick={logout}
                  className="text-gray-500 hover:text-red-600"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/auth/login" className="text-gray-600 hover:text-primary-600">
                  Login
                </Link>
                <Link
                  href="/auth/register"
                  className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
