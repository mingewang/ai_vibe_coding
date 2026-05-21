"use client";

// ============================================================
// EditProductPage (/admin/products/[id]/edit) — edit a product
// ============================================================
// Admin-only. Loads existing product data and shows the form
// pre-filled so the admin can make changes.
// ============================================================

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { IProduct, IProductInput, IApiResponse } from "@/types";
import AdminProductForm from "@/components/AdminProductForm";
import LoadingSpinner from "@/components/LoadingSpinner";
import ProtectedRoute from "@/components/ProtectedRoute";

function EditProductContent() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [product, setProduct] = useState<IProduct | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Fetch existing product data
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const res = await fetch(`/api/products/${id}`);
        const data: IApiResponse<IProduct> = await res.json();
        if (data.data) setProduct(data.data);
      } catch (err) {
        console.error("Failed to fetch product", err);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchProduct();
  }, [id]);

  const handleSubmit = async (data: IProductInput) => {
    setSaving(true);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`/api/products/${id}`, {
        method: "PUT",
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
        alert(err.error || "Failed to update product");
      }
    } catch {
      alert("Something went wrong");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  if (!product) {
    return (
      <div className="text-center py-16">
        <h2 className="text-2xl font-semibold text-gray-700">Product Not Found</h2>
      </div>
    );
  }

  const initialData: IProductInput = {
    name: product.name,
    description: product.description,
    price: product.price,
    category: product.category,
    imageUrl: product.imageUrl,
    stock: product.stock,
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        Edit Product
      </h1>
      <div className="bg-white border border-gray-200 rounded-xl p-8">
        <AdminProductForm
          initialData={initialData}
          onSubmit={handleSubmit}
          loading={saving}
        />
      </div>
    </div>
  );
}

export default function EditProductPage() {
  return (
    <ProtectedRoute>
      <EditProductContent />
    </ProtectedRoute>
  );
}
