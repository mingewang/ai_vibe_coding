// ============================================================
// /api/products/[id] — Get, update, or delete a single product
// ============================================================
// GET    /api/products/[id] → Get product by ID (public)
// PUT    /api/products/[id] → Update product (admin only)
// DELETE /api/products/[id] → Delete product (admin only)
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import Product from "@/lib/models/Product";
import { getAuthUser } from "@/lib/auth";

// Helper: get the product ID from the URL
function getId(request: NextRequest): string {
  const url = new URL(request.url);
  const segments = url.pathname.split("/");
  return segments[segments.length - 1];
}

// ---------- GET: Fetch a single product ----------
export async function GET(request: NextRequest) {
  try {
    await connectDB();
    const product = await Product.findById(getId(request));

    if (!product) {
      return NextResponse.json(
        { error: "Product not found" },
        { status: 404 }
      );
    }

    return NextResponse.json({ data: product });
  } catch (error) {
    console.error("Get product error:", error);
    return NextResponse.json(
      { error: "Failed to fetch product" },
      { status: 500 }
    );
  }
}

// ---------- PUT: Update a product (admin only) ----------
export async function PUT(request: NextRequest) {
  try {
    // Check auth
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }
    if (authUser.role !== "admin") {
      return NextResponse.json({ error: "Admin access required" }, { status: 403 });
    }

    // Parse body and update
    const body = await request.json();
    await connectDB();

    const product = await Product.findByIdAndUpdate(getId(request), body, {
      new: true, // Return the updated document
      runValidators: true, // Run Mongoose validation
    });

    if (!product) {
      return NextResponse.json({ error: "Product not found" }, { status: 404 });
    }

    return NextResponse.json({ data: product });
  } catch (error) {
    console.error("Update product error:", error);
    return NextResponse.json(
      { error: "Failed to update product" },
      { status: 500 }
    );
  }
}

// ---------- DELETE: Remove a product (admin only) ----------
export async function DELETE(request: NextRequest) {
  try {
    // Check auth
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }
    if (authUser.role !== "admin") {
      return NextResponse.json({ error: "Admin access required" }, { status: 403 });
    }

    await connectDB();
    const product = await Product.findByIdAndDelete(getId(request));

    if (!product) {
      return NextResponse.json({ error: "Product not found" }, { status: 404 });
    }

    return NextResponse.json({ message: "Product deleted successfully" });
  } catch (error) {
    console.error("Delete product error:", error);
    return NextResponse.json(
      { error: "Failed to delete product" },
      { status: 500 }
    );
  }
}
