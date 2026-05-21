// ============================================================
// GET /api/orders/[id] — Get a single order's details
// ============================================================
// Users can only view their own orders.
// Requires authentication.
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import Order from "@/lib/models/Order";
import { getAuthUser } from "@/lib/auth";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    await connectDB();

    const order = await Order.findById(params.id);

    if (!order) {
      return NextResponse.json({ error: "Order not found" }, { status: 404 });
    }

    // Security: users can only see their own orders
    if (order.userId.toString() !== authUser.userId) {
      return NextResponse.json(
        { error: "You don't have permission to view this order" },
        { status: 403 }
      );
    }

    return NextResponse.json({ data: order });
  } catch (error) {
    console.error("Get order error:", error);
    return NextResponse.json(
      { error: "Failed to fetch order" },
      { status: 500 }
    );
  }
}
