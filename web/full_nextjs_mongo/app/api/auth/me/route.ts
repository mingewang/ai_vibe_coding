// ============================================================
// GET /api/auth/me — Get the currently logged-in user
// ============================================================
// Requires a valid JWT in the Authorization header.
// Response: { data: { user } }
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import { connectDB } from "@/lib/db";
import User from "@/lib/models/User";
import { getAuthUser } from "@/lib/auth";

export async function GET(request: NextRequest) {
  try {
    // 1. Check if the user is authenticated
    const authUser = getAuthUser(request);
    if (!authUser) {
      return NextResponse.json(
        { error: "Not authenticated. Please log in." },
        { status: 401 }
      );
    }

    // 2. Connect to database
    await connectDB();

    // 3. Find the user by ID (from the JWT payload)
    const user = await User.findById(authUser.userId).select("-password");
    if (!user) {
      return NextResponse.json(
        { error: "User not found" },
        { status: 404 }
      );
    }

    // 4. Return user data
    return NextResponse.json({
      data: {
        _id: user._id.toString(),
        name: user.name,
        email: user.email,
        role: user.role,
        createdAt: user.createdAt,
      },
    });
  } catch (error) {
    console.error("Get me error:", error);
    return NextResponse.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }
}
