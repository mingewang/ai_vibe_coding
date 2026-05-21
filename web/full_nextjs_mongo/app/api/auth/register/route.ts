// ============================================================
// POST /api/auth/register — Create a new user account
// ============================================================
// Request body: { name, email, password }
// Response: { data: { user }, token }
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { connectDB } from "@/lib/db";
import User from "@/lib/models/User";
import { signToken } from "@/lib/auth";

export async function POST(request: NextRequest) {
  try {
    // 1. Parse the request body
    const { name, email, password } = await request.json();

    // 2. Validate input
    if (!name || !email || !password) {
      return NextResponse.json(
        { error: "Name, email, and password are required" },
        { status: 400 }
      );
    }

    if (password.length < 6) {
      return NextResponse.json(
        { error: "Password must be at least 6 characters" },
        { status: 400 }
      );
    }

    // 3. Connect to database
    await connectDB();

    // 4. Check if user already exists
    const existingUser = await User.findOne({ email: email.toLowerCase() });
    if (existingUser) {
      return NextResponse.json(
        { error: "An account with this email already exists" },
        { status: 409 }
      );
    }

    // 5. Hash the password (never store plain text!)
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // 6. Create the user
    const user = await User.create({
      name,
      email: email.toLowerCase(),
      password: hashedPassword,
    });

    // 7. Sign a JWT token for the new user
    const token = signToken({
      userId: user._id.toString(),
      email: user.email,
      role: user.role,
    });

    // 8. Return user data (without password) and token
    return NextResponse.json(
      {
        data: {
          _id: user._id.toString(),
          name: user.name,
          email: user.email,
          role: user.role,
        },
        token,
      },
      { status: 201 }
    );
  } catch (error) {
    console.error("Register error:", error);
    return NextResponse.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }
}
