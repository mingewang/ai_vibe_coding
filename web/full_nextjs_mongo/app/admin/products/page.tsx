"use client";

// ============================================================
// AdminProductsPage (/admin/products) — product management dashboard
// ============================================================
// Lists all products in a table with Edit / Delete actions.
// Admin-only page.
// ============================================================

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { IProduct, IPaginatedResponse, IApiResponse } from "@/types";
import AdminProductTable from "@/components/AdminProductTable";
import LoadingSpinner from "@/components/LoadingSpinner";
import ProtectedRoute from "@/components/ProtectedRoute";

function AdminProductsContent() {
  const router = useRouter();
  const [products, setProducts] = useState<IProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState<string | null>(null);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/products?limit=100");
      const data: IPaginatedResponse<IProduct> = await res.json();
      if (data.data) setProducts(data.data);
    } catch (err) {
      console.error("Failed to fetch products", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const handleEdit = (id: string) => {
    router.push(`/admin/products/${id}/edit`);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this product?")) return;

    setDeleting(id);
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`/api/products/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      const data: IApiResponse<null> = await res.json();

      if (data.message) {
        // Remove from local state
        setProducts((prev) => prev.filter((p) => p._id !== id));
      } else {
        alert(data.error || "Failed to delete product");
      }
    } catch {
      alert("Something went wrong");
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Manage Products
        </h1>
        <button
          onClick={() => router.push("/admin/products/new")}
          className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700"
        >
          Add Product
        </button>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <AdminProductTable
            products={products}
            onEdit={handleEdit}
            onDelete={handleDelete}
            deleting={deleting}
          />
        </div>
      )}
    </div>
  );
}

export default function AdminProductsPage() {
  return (
    <ProtectedRoute>
      <AdminProductsContent />
    </ProtectedRoute>
  );
}
