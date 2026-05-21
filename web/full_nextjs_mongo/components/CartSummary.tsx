"use client";

// ============================================================
// CartSummary — shows order subtotal, total, and checkout button
// ============================================================
// Props:
//   subtotal: total price of all items before any adjustments
//   itemCount: total number of items
//   onCheckout: called when user clicks "Place Order"
//   loading: true while the order is being placed
// ============================================================

interface CartSummaryProps {
  subtotal: number;
  itemCount: number;
  onCheckout: () => void;
  loading: boolean;
}

export default function CartSummary({
  subtotal,
  itemCount,
  onCheckout,
  loading,
}: CartSummaryProps) {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-xl p-6 space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Order Summary</h2>

      <div className="flex justify-between text-gray-600">
        <span>Items ({itemCount})</span>
        <span>${subtotal.toFixed(2)}</span>
      </div>

      <div className="flex justify-between text-gray-600">
        <span>Shipping</span>
        <span className="text-green-600">Free</span>
      </div>

      <hr />

      <div className="flex justify-between text-lg font-bold text-gray-900">
        <span>Total</span>
        <span>${subtotal.toFixed(2)}</span>
      </div>

      <button
        onClick={onCheckout}
        disabled={loading || itemCount === 0}
        className="w-full bg-primary-600 text-white py-3 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50"
      >
        {loading ? "Placing Order..." : "Place Order"}
      </button>
    </div>
  );
}
