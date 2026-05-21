// ============================================================
// Auth Helpers (lib/auth.ts)
// ============================================================
// Utility functions for JWT token creation, verification,
// and extracting the current user from API requests.
// ============================================================

import jwt from "jsonwebtoken";
import { NextRequest } from "next/server";
import { IJwtPayload } from "@/types";

// Get the secret from environment variables
const JWT_SECRET = process.env.JWT_SECRET || "fallback-dev-secret";

/**
 * Create a JWT token for a given user.
 * This token proves the user is who they say they are.
 */
export function signToken(payload: IJwtPayload): string {
  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: "7d", // Token expires in 7 days
  });
}

/**
 * Verify a JWT token and return the decoded payload.
 * Returns null if the token is invalid or expired.
 */
export function verifyToken(token: string): IJwtPayload | null {
  try {
    return jwt.verify(token, JWT_SECRET) as IJwtPayload;
  } catch {
    // Token is invalid or expired
    return null;
  }
}

/**
 * Extract the JWT token from the Authorization header of a request.
 * The header should look like: "Bearer <token>"
 */
export function getTokenFromRequest(request: NextRequest): string | null {
  const authHeader = request.headers.get("authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return null;
  }
  return authHeader.split(" ")[1];
}

/**
 * Get the current user's JWT payload from a request.
 * Returns null if not authenticated.
 * Use this in API routes to protect them.
 */
export function getAuthUser(request: NextRequest): IJwtPayload | null {
  const token = getTokenFromRequest(request);
  if (!token) return null;
  return verifyToken(token);
}
