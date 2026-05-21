// ============================================================
// /api/cart — Manage the current user's shopping cart
// ============================================================
// GET  /api/cart   → Get the user's cart
// POST /api/cart   → Add an item (or increase quantity)
// PUT  /api/cart   → Update item quantity
//
// All endpoints require authentication (JWT token).
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import Cart from "@/lib/models/Cart";
import { getAuthUser } from "@/lib/auth";

// Helper: get or create the cart for the current user
async function getOrCreateCart(userId: string) {
  let cart = await Cart.findOne({ userId });
  if (!cart) {
    cart = await Cart.create({ userId, items: [] });
  }
  return cart;
}

// ---------- GET: Fetch the current user's cart ----------
export async function GET(request: NextRequest) {
  try {
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    await connectDB();
    const cart = await getOrCreateCart(authUser.userId);

    return NextResponse.json({ data: { items: cart.items } });
  } catch (error) {
    console.error("Get cart error:", error);
    return NextResponse.json({ error: "Failed to fetch cart" }, { status: 500 });
  }
}

// ---------- POST: Add an item to the cart ----------
// If the product is already in the cart, increase quantity.
export async function POST(request: NextRequest) {
  try {
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    const { productId, name, price, quantity = 1 } = await request.json();

    if (!productId || !name || !price) {
      return NextResponse.json(
        { error: "productId, name, and price are required" },
        { status: 400 }
      );
    }

    await connectDB();
    const cart = await getOrCreateCart(authUser.userId);

    // Check if the product is already in the cart
    const existingIndex = cart.items.findIndex(
      (item) => item.productId.toString() === productId
    );

    if (existingIndex > -1) {
      // Product exists → increase quantity
      cart.items[existingIndex].quantity += quantity;
    } else {
      // Product doesn't exist → add new item
      cart.items.push({ productId, name, price, quantity });
    }

    await cart.save();

    return NextResponse.json({ data: { items: cart.items } });
  } catch (error) {
    console.error("Add to cart error:", error);
    return NextResponse.json({ error: "Failed to add to cart" }, { status: 500 });
  }
}

// ---------- PUT: Update item quantity ----------
export async function PUT(request: NextRequest) {
  try {
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    const { productId, quantity } = await request.json();

    if (!productId || quantity === undefined) {
      return NextResponse.json(
        { error: "productId and quantity are required" },
        { status: 400 }
      );
    }

    await connectDB();
    const cart = await getOrCreateCart(authUser.userId);

    const existingIndex = cart.items.findIndex(
      (item) => item.productId.toString() === productId
    );

    if (existingIndex === -1) {
      return NextResponse.json(
        { error: "Item not found in cart" },
        { status: 404 }
      );
    }

    if (quantity < 1) {
      // If quantity is 0 or less, remove the item
      cart.items.splice(existingIndex, 1);
    } else {
      cart.items[existingIndex].quantity = quantity;
    }

    await cart.save();

    return NextResponse.json({ data: { items: cart.items } });
  } catch (error) {
    console.error("Update cart error:", error);
    return NextResponse.json({ error: "Failed to update cart" }, { status: 500 });
  }
}
