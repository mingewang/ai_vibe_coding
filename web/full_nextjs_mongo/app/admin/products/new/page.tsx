"use client";

// ============================================================
// AdminNewProductPage (/admin/products/new) — create a product
// ============================================================
// Admin-only. Shows the AdminProductForm for creating a new product.
// ============================================================

import { useState } from "react";
import { useRouter } from "next/navigation";
import { IProductInput } from "@/types";
import AdminProductForm from "@/components/AdminProductForm";
import ProtectedRoute from "@/components/ProtectedRoute";

function NewProductContent() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data: IProductInput) => {
    setLoading(true);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch("/api/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (res.ok) {
        router.push("/admin/products");
      } else {
        const err = await res.json();
        alert(err.error || "Failed to create product");
      }
    } catch {
      alert("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        New Product
      </h1>
      <div className="bg-white border border-gray-200 rounded-xl p-8">
        <AdminProductForm onSubmit={handleSubmit} loading={loading} />
      </div>
    </div>
  );
}

export default function NewProductPage() {
  return (
    <ProtectedRoute>
      <NewProductContent />
    </ProtectedRoute>
  );
}
