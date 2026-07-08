// ============================================================
// MongoDB Connection (lib/db.ts)
// ============================================================
// This module connects to MongoDB using Mongoose.
// We cache the connection so we don't create a new one
// every time a file imports this module (important in dev
// because Next.js hot-reloads files frequently).
// ============================================================

import mongoose from "mongoose";

// Get the connection string from environment variables
const MONGODB_URI = process.env.COMRITE_CLOUD_MONGO_URL;

// Check if the URI exists — if not, show a helpful error
if (!MONGODB_URI) {
  throw new Error(
    "Please define the COMRITE_CLOUD_MONGO_URL environment variable inside .env.local"
  );
}

// An interface to type our cache object
interface MongooseCache {
  conn: typeof mongoose | null;
  promise: Promise<typeof mongoose> | null;
}

// Declare a global variable so the cache survives hot reloads
declare global {
  var mongooseCache: MongooseCache | undefined;
}

// Use existing cache or create a new empty one
const cached: MongooseCache = global.mongooseCache ?? {
  conn: null,
  promise: null,
};

if (!global.mongooseCache) {
  global.mongooseCache = cached;
}

/**
 * Connect to MongoDB and return the mongoose instance.
 * Uses a cached connection if one already exists.
 */
export async function connectDB(): Promise<typeof mongoose> {
  // If we already have a connection, return it immediately
  if (cached.conn) {
    return cached.conn;
  }

  // If no connection promise exists yet, create one
  if (!cached.promise) {
    cached.promise = mongoose.connect(MONGODB_URI!).then((mongoose) => {
      return mongoose;
    });
  }

  // Wait for the connection to complete
  cached.conn = await cached.promise;
  return cached.conn;
}
