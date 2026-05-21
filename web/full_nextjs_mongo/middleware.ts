// ============================================================
// Middleware — runs on every request before reaching a page/API
// ============================================================
// Currently acts as a pass-through. In the future, you could:
//   - Protect admin routes at the edge level
//   - Redirect unauthenticated users away from certain pages
//   - Rate-limit API calls
// ============================================================

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // For now, let all requests through.
  // Auth protection is handled at the page/API level.
  return NextResponse.next();
}

// Configure which routes trigger this middleware
export const config = {
  matcher: [
    // Match all routes except static files and _next internals
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
