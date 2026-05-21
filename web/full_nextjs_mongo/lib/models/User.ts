// ============================================================
// User Model (lib/models/User.ts)
// ============================================================
// Defines the structure of a user document in MongoDB.
// Passwords are hashed automatically before saving.
// ============================================================

import mongoose, { Schema, Document, Model } from "mongoose";

// The shape of a User document (what Mongoose returns from queries)
export interface IUserDocument extends Document {
  name: string;
  email: string;
  password: string;
  role: "user" | "admin";
  createdAt: Date;
  updatedAt: Date;
}

// Define the schema (the blueprint for the "users" collection)
const UserSchema = new Schema<IUserDocument>(
  {
    name: {
      type: String,
      required: [true, "Name is required"],
      trim: true,
    },
    email: {
      type: String,
      required: [true, "Email is required"],
      unique: true, // No two users can have the same email
      lowercase: true,
      trim: true,
    },
    password: {
      type: String,
      required: [true, "Password is required"],
      minlength: [6, "Password must be at least 6 characters"],
    },
    role: {
      type: String,
      enum: ["user", "admin"],
      default: "user",
    },
  },
  {
    timestamps: true, // Automatically add createdAt and updatedAt
  }
);

// Create and export the model
// We use `mongoose.models.User` to avoid redefining the model
// during hot reloads (common Next.js pattern).
const User: Model<IUserDocument> =
  mongoose.models.User || mongoose.model<IUserDocument>("User", UserSchema);

export default User;
