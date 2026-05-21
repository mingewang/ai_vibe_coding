// ============================================================
// DELETE /api/cart/items/[productId] — Remove item from cart
// ============================================================
// Deletes a specific item from the user's cart by product ID.
// Requires authentication.
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import Cart from "@/lib/models/Cart";
import { getAuthUser } from "@/lib/auth";

export async function DELETE(
  request: NextRequest,
  { params }: { params: { productId: string } }
) {
  try {
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    await connectDB();
    const cart = await Cart.findOne({ userId: authUser.userId });

    if (!cart) {
      return NextResponse.json({ error: "Cart not found" }, { status: 404 });
    }

    // Remove the item with the matching productId
    cart.items = cart.items.filter(
      (item) => item.productId.toString() !== params.productId
    );

    await cart.save();

    return NextResponse.json({ data: { items: cart.items } });
  } catch (error) {
    console.error("Remove from cart error:", error);
    return NextResponse.json(
      { error: "Failed to remove item from cart" },
      { status: 500 }
    );
  }
}
