"use client";

// ============================================================
// CartPage (/cart) — view cart items and place an order
// ============================================================

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useCart } from "@/context/CartContext";
import { IApiResponse, IOrder } from "@/types";
import CartItem from "@/components/CartItem";
import CartSummary from "@/components/CartSummary";
import EmptyState from "@/components/EmptyState";
import LoadingSpinner from "@/components/LoadingSpinner";
import ProtectedRoute from "@/components/ProtectedRoute";

function CartContent() {
  const router = useRouter();
  const { user } = useAuth();
  const { items, total, itemCount, updateQuantity, removeItem, refreshCart } =
    useCart();
  const [placingOrder, setPlacingOrder] = useState(false);

  const handleCheckout = async () => {
    if (!user) return;
    setPlacingOrder(true);

    try {
      const res = await fetch("/api/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const data: IApiResponse<IOrder> = await res.json();

      if (data.data) {
        // Order placed successfully — refresh cart and go to orders
        await refreshCart();
        router.push(`/orders/${data.data._id}`);
      } else {
        alert(data.error || "Failed to place order");
      }
    } catch {
      alert("Something went wrong. Please try again.");
    } finally {
      setPlacingOrder(false);
    }
  };

  if (items.length === 0) {
    return (
      <EmptyState
        title="Your cart is empty"
        description="Looks like you haven't added anything yet."
        actionText="Browse Products"
        actionHref="/products"
      />
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          {items.map((item) => (
            <CartItem
              key={item.productId}
              item={item}
              onUpdateQuantity={updateQuantity}
              onRemove={removeItem}
            />
          ))}
        </div>

        {/* Summary */}
        <div>
          <CartSummary
            subtotal={total}
            itemCount={itemCount}
            onCheckout={handleCheckout}
            loading={placingOrder}
          />
        </div>
      </div>
    </div>
  );
}

export default function CartPage() {
  return (
    <ProtectedRoute>
      <CartContent />
    </ProtectedRoute>
  );
}
