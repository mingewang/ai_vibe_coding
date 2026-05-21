"use client";

// ============================================================
// CartItem — a single row in the shopping cart
// ============================================================
// Shows product info, quantity controls, and remove button.
// ============================================================

import { ICartItem } from "@/types";

interface CartItemProps {
  item: ICartItem;
  onUpdateQuantity: (productId: string, quantity: number) => void;
  onRemove: (productId: string) => void;
}

export default function CartItem({ item, onUpdateQuantity, onRemove }: CartItemProps) {
  const subtotal = item.price * item.quantity;

  return (
    <div className="flex items-center justify-between border-b border-gray-200 py-4">
      <div className="flex-1">
        <h3 className="font-medium text-gray-900">{item.name}</h3>
        <p className="text-gray-500 text-sm">${item.price.toFixed(2)} each</p>
      </div>

      {/* Quantity Controls */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => onUpdateQuantity(item.productId, item.quantity - 1)}
          disabled={item.quantity <= 1}
          className="w-8 h-8 border rounded-lg disabled:opacity-50 hover:bg-gray-50"
        >
          −
        </button>
        <span className="w-8 text-center">{item.quantity}</span>
        <button
          onClick={() => onUpdateQuantity(item.productId, item.quantity + 1)}
          className="w-8 h-8 border rounded-lg hover:bg-gray-50"
        >
          +
        </button>
      </div>

      {/* Subtotal */}
      <p className="w-24 text-right font-medium">${subtotal.toFixed(2)}</p>

      {/* Remove */}
      <button
        onClick={() => onRemove(item.productId)}
        className="ml-4 text-red-500 hover:text-red-700 text-sm"
      >
        Remove
      </button>
    </div>
  );
}
