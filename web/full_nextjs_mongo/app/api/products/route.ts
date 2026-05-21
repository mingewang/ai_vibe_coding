// ============================================================
// /api/products — List, search, filter, paginate & create products
// ============================================================
// GET  /api/products       → List products (public)
// POST /api/products       → Create product (admin only)
//
// Query params for GET:
//   search, category, minPrice, maxPrice, page, limit
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import Product from "@/lib/models/Product";
import { getAuthUser } from "@/lib/auth";

// ---------- GET: List products with search, filter, pagination ----------
export async function GET(request: NextRequest) {
  try {
    await connectDB();

    // Get query parameters from the URL
    const { searchParams } = new URL(request.url);
    const search = searchParams.get("search") || "";
    const category = searchParams.get("category") || "";
    const minPrice = searchParams.get("minPrice");
    const maxPrice = searchParams.get("maxPrice");
    const page = parseInt(searchParams.get("page") || "1", 10);
    const limit = parseInt(searchParams.get("limit") || "12", 10);

    // Build the MongoDB filter object
    const filter: Record<string, unknown> = {};

    // Text search using MongoDB $regex (case-insensitive)
    if (search) {
      filter.$or = [
        { name: { $regex: search, $options: "i" } },
        { description: { $regex: search, $options: "i" } },
      ];
    }

    // Category filter
    if (category) {
      filter.category = category;
    }

    // Price range filter
    if (minPrice || maxPrice) {
      filter.price = {};
      if (minPrice) filter.price.$gte = parseFloat(minPrice);
      if (maxPrice) filter.price.$lte = parseFloat(maxPrice);
    }

    // Calculate pagination values
    const skip = (page - 1) * limit;

    // Run the query and count in parallel for efficiency
    const [products, totalItems] = await Promise.all([
      Product.find(filter).sort({ createdAt: -1 }).skip(skip).limit(limit),
      Product.countDocuments(filter),
    ]);

    const totalPages = Math.ceil(totalItems / limit);

    // Return paginated response
    return NextResponse.json({
      data: products,
      page,
      totalPages,
      totalItems,
    });
  } catch (error) {
    console.error("Get products error:", error);
    return NextResponse.json(
      { error: "Failed to fetch products" },
      { status: 500 }
    );
  }
}

// ---------- POST: Create a product (admin only) ----------
export async function POST(request: NextRequest) {
  try {
    // 1. Check authentication and admin role
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json(
        { error: "Not authenticated" },
        { status: 401 }
      );
    }
    if (authUser.role !== "admin") {
      return NextResponse.json(
        { error: "Admin access required" },
        { status: 403 }
      );
    }

    // 2. Parse request body
    const { name, description, price, category, imageUrl, stock } =
      await request.json();

    // 3. Validate required fields
    if (!name || !description || !price || !category || !imageUrl) {
      return NextResponse.json(
        { error: "Missing required fields: name, description, price, category, imageUrl" },
        { status: 400 }
      );
    }

    // 4. Connect and create
    await connectDB();
    const product = await Product.create({
      name,
      description,
      price,
      category,
      imageUrl,
      stock: stock ?? 0,
    });

    return NextResponse.json({ data: product }, { status: 201 });
  } catch (error) {
    console.error("Create product error:", error);
    return NextResponse.json(
      { error: "Failed to create product" },
      { status: 500 }
    );
  }
}
