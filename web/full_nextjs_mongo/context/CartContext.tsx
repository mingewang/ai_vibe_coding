"use client";

// ============================================================
// CartContext — manages the shopping cart across the app
// ============================================================
// This context provides:
//   - items: array of cart items
//   - itemCount: total number of items (sum of quantities)
//   - total: total price of all items
//   - loading: true while fetching cart data
//   - addItem(productId, name, price): add a product to cart
//   - updateQuantity(productId, quantity): change item quantity
//   - removeItem(productId): remove an item from cart
//   - clearCart(): empty the cart
//   - refreshCart(): re-fetch cart from the server
//
// Usage: wrap your app layout with <CartProvider>
//        then use `const { items, addItem } = useCart()`.
// ============================================================

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { ICartItem, IApiResponse } from "@/types";

interface CartContextType {
  items: ICartItem[];
  itemCount: number;
  total: number;
  loading: boolean;
  addItem: (productId: string, name: string, price: number, quantity?: number) => Promise<void>;
  updateQuantity: (productId: string, quantity: number) => Promise<void>;
  removeItem: (productId: string) => Promise<void>;
  clearCart: () => Promise<void>;
  refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<ICartItem[]>([]);
  const [loading, setLoading] = useState(true);

  // Derived values
  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0);
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  // Fetch the current cart from the server
  const refreshCart = useCallback(async () => {
    const token = getToken();
    if (!token) {
      setItems([]);
      setLoading(false);
      return;
    }

    try {
      const res = await fetch("/api/cart", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data: IApiResponse<{ items: ICartItem[] }> = await res.json();
      if (data.data) {
        setItems(data.data.items);
      }
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, []);

  // Load cart on mount
  useEffect(() => {
    refreshCart();
  }, [refreshCart]);

  // Add an item to the cart (or increment quantity if it already exists)
  const addItem = useCallback(
    async (productId: string, name: string, price: number, quantity = 1) => {
      const token = getToken();
      if (!token) return;

      const res = await fetch("/api/cart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ productId, name, price, quantity }),
      });

      const data: IApiResponse<{ items: ICartItem[] }> = await res.json();
      if (data.data) {
        setItems(data.data.items);
      }
    },
    []
  );

  // Update the quantity of an item
  const updateQuantity = useCallback(async (productId: string, quantity: number) => {
    const token = getToken();
    if (!token) return;

    const res = await fetch("/api/cart", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ productId, quantity }),
    });

    const data: IApiResponse<{ items: ICartItem[] }> = await res.json();
    if (data.data) {
      setItems(data.data.items);
    }
  }, []);

  // Remove an item from the cart
  const removeItem = useCallback(async (productId: string) => {
    const token = getToken();
    if (!token) return;

    const res = await fetch(`/api/cart/items/${productId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    const data: IApiResponse<{ items: ICartItem[] }> = await res.json();
    if (data.data) {
      setItems(data.data.items);
    }
  }, []);

  // Clear the entire cart
  const clearCart = useCallback(async () => {
    // Remove each item one by one
    for (const item of items) {
      await removeItem(item.productId);
    }
    setItems([]);
  }, [items, removeItem]);

  return (
    <CartContext.Provider
      value={{ items, itemCount, total, loading, addItem, updateQuantity, removeItem, clearCart, refreshCart }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart(): CartContextType {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used inside a <CartProvider>");
  }
  return context;
}
