"use client";

// ============================================================
// OrderDetailPage (/orders/[id]) — details of a single order
// ============================================================

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { IOrder, IApiResponse } from "@/types";
import LoadingSpinner from "@/components/LoadingSpinner";
import ProtectedRoute from "@/components/ProtectedRoute";

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  shipped: "bg-blue-100 text-blue-800",
  delivered: "bg-green-100 text-green-800",
  cancelled: "bg-red-100 text-red-800",
};

function OrderDetailContent() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [order, setOrder] = useState<IOrder | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch(`/api/orders/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.status === 403) {
          // Not authorized — redirect to orders list
          router.push("/orders");
          return;
        }

        const data: IApiResponse<IOrder> = await res.json();
        if (data.data) setOrder(data.data);
      } catch (err) {
        console.error("Failed to fetch order", err);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchOrder();
  }, [id, router]);

  if (loading) return <LoadingSpinner />;

  if (!order) {
    return (
      <div className="text-center py-16">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">
          Order Not Found
        </h2>
        <Link href="/orders" className="text-primary-600 hover:underline">
          Back to orders
        </Link>
      </div>
    );
  }

  const date = order.createdAt
    ? new Date(order.createdAt).toLocaleDateString()
    : "N/A";

  return (
    <div>
      <Link href="/orders" className="text-primary-600 hover:underline mb-4 block">
        ← Back to Orders
      </Link>

      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Order Details</h1>
          <p className="text-gray-500">Placed on {date}</p>
        </div>
        <span
          className={`px-4 py-2 rounded-full text-sm font-medium ${
            statusColors[order.status] || "bg-gray-100 text-gray-800"
          }`}
        >
          {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
        </span>
      </div>

      {/* Order Items */}
      <div className="bg-white border border-gray-200 rounded-xl p-6 mb-6">
        <h2 className="font-semibold text-gray-900 mb-4">Items</h2>
        {order.items.map((item) => (
          <div
            key={item.productId}
            className="flex justify-between py-3 border-b border-gray-100 last:border-0"
          >
            <div>
              <p className="text-gray-900">{item.name}</p>
              <p className="text-sm text-gray-500">
                Qty: {item.quantity} × ${item.price.toFixed(2)}
              </p>
            </div>
            <p className="font-medium">
              ${(item.price * item.quantity).toFixed(2)}
            </p>
          </div>
        ))}
      </div>

      {/* Total */}
      <div className="bg-gray-50 border border-gray-200 rounded-xl p-6">
        <div className="flex justify-between text-lg font-bold">
          <span>Total</span>
          <span>${order.total.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}

export default function OrderDetailPage() {
  return (
    <ProtectedRoute>
      <OrderDetailContent />
    </ProtectedRoute>
  );
}
