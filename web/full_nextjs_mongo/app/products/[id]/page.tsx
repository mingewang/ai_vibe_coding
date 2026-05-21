"use client";

// ============================================================
// ProductDetailPage (/products/[id]) — full product information
// ============================================================
// Shows product image, description, price, stock status,
// and an "Add to Cart" button for logged-in users.
// ============================================================

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { IProduct, IApiResponse } from "@/types";
import { useAuth } from "@/context/AuthContext";
import { useCart } from "@/context/CartContext";
import LoadingSpinner from "@/components/LoadingSpinner";

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const { addItem } = useCart();

  const [product, setProduct] = useState<IProduct | null>(null);
  const [loading, setLoading] = useState(true);
  const [addingToCart, setAddingToCart] = useState(false);
  const [addedMessage, setAddedMessage] = useState("");

  // Fetch product on mount
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

  const handleAddToCart = async () => {
    if (!product || !user) return;

    setAddingToCart(true);
    try {
      await addItem(product._id, product.name, product.price, 1);
      setAddedMessage("Added to cart!");
      setTimeout(() => setAddedMessage(""), 3000);
    } catch {
      // Error is handled by the context
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  if (!product) {
    return (
      <div className="text-center py-16">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">
          Product Not Found
        </h2>
        <Link href="/products" className="text-primary-600 hover:underline">
          Browse all products
        </Link>
      </div>
    );
  }

  return (
    <div className="grid md:grid-cols-2 gap-8">
      {/* Product Image */}
      <div className="aspect-square bg-gray-100 rounded-xl overflow-hidden">
        <img
          src={product.imageUrl}
          alt={product.name}
          className="w-full h-full object-cover"
        />
      </div>

      {/* Product Info */}
      <div>
        <p className="text-sm text-primary-600 uppercase tracking-wide mb-2">
          {product.category}
        </p>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {product.name}
        </h1>
        <p className="text-4xl font-bold text-gray-900 mb-6">
          ${product.price.toFixed(2)}
        </p>

        {/* Stock status */}
        {product.stock > 0 ? (
          <p className="text-green-600 mb-6">
            {product.stock <= 5
              ? `Only ${product.stock} left in stock — order soon!`
              : "In stock"}
          </p>
        ) : (
          <p className="text-red-500 mb-6">Out of stock</p>
        )}

        <p className="text-gray-600 leading-relaxed mb-8">
          {product.description}
        </p>

        {/* Add to Cart */}
        {user ? (
          <div className="flex items-center gap-4">
            <button
              onClick={handleAddToCart}
              disabled={addingToCart || product.stock === 0}
              className="bg-primary-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50"
            >
              {addingToCart ? "Adding..." : "Add to Cart"}
            </button>
            {addedMessage && (
              <span className="text-green-600 font-medium">
                {addedMessage}
              </span>
            )}
          </div>
        ) : (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <p className="text-gray-600">
              <Link href="/auth/login" className="text-primary-600 hover:underline">
                Log in
              </Link>{" "}
              to add items to your cart.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
