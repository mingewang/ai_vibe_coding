// ============================================================
// OrderCard — a summary card for a single order
// ============================================================
// Shows order date, status, item count, and total.
// Clicking navigates to the order detail page.
// ============================================================

import Link from "next/link";
import { IOrder } from "@/types";

interface OrderCardProps {
  order: IOrder;
}

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  shipped: "bg-blue-100 text-blue-800",
  delivered: "bg-green-100 text-green-800",
  cancelled: "bg-red-100 text-red-800",
};

export default function OrderCard({ order }: OrderCardProps) {
  const date = order.createdAt
    ? new Date(order.createdAt).toLocaleDateString()
    : "N/A";
  const itemCount = order.items.reduce((sum, i) => sum + i.quantity, 0);

  return (
    <Link
      href={`/orders/${order._id}`}
      className="block border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow"
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-500">Placed on {date}</p>
          <p className="text-lg font-semibold mt-1">
            ${order.total.toFixed(2)}
          </p>
          <p className="text-sm text-gray-500">{itemCount} item(s)</p>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-sm font-medium ${
            statusColors[order.status] || "bg-gray-100 text-gray-800"
          }`}
        >
          {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
        </span>
      </div>
    </Link>
  );
}
