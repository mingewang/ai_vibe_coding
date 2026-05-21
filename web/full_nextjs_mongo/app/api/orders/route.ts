// ============================================================
// /api/orders — List orders and place new orders
// ============================================================
// GET  /api/orders   → List current user's orders (auth required)
// POST /api/orders   → Place a new order from the cart (auth required)
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import Order from "@/lib/models/Order";
import Cart from "@/lib/models/Cart";
import { getAuthUser } from "@/lib/auth";

// ---------- GET: List user's orders ----------
export async function GET(request: NextRequest) {
  try {
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    await connectDB();

    const orders = await Order.find({ userId: authUser.userId })
      .sort({ createdAt: -1 }) // Newest first
      .limit(50);

    return NextResponse.json({ data: orders });
  } catch (error) {
    console.error("Get orders error:", error);
    return NextResponse.json(
      { error: "Failed to fetch orders" },
      { status: 500 }
    );
  }
}

// ---------- POST: Place a new order ----------
// This converts the current cart into an order, then clears the cart.
export async function POST(request: NextRequest) {
  try {
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    await connectDB();

    // 1. Get the user's cart
    const cart = await Cart.findOne({ userId: authUser.userId });
    if (!cart || cart.items.length === 0) {
      return NextResponse.json(
        { error: "Cart is empty. Add items before placing an order." },
        { status: 400 }
      );
    }

    // 2. Calculate the total
    const total = cart.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );

    // 3. Create the order from cart items
    const order = await Order.create({
      userId: authUser.userId,
      items: cart.items,
      total,
      status: "pending",
    });

    // 4. Clear the cart
    cart.items = [];
    await cart.save();

    return NextResponse.json({ data: order }, { status: 201 });
  } catch (error) {
    console.error("Place order error:", error);
    return NextResponse.json(
      { error: "Failed to place order" },
      { status: 500 }
    );
  }
}
