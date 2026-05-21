// ============================================================
// Cart Model (lib/models/Cart.ts)
// ============================================================
// Defines the structure of a shopping cart in MongoDB.
// Each user has exactly one cart document.
// The cart contains an array of items (products + quantities).
// ============================================================

import mongoose, { Schema, Document, Model } from "mongoose";

// Sub-document for items inside the cart
export interface ICartItemSchema {
  productId: mongoose.Types.ObjectId;
  name: string;
  price: number;
  quantity: number;
}

export interface ICartDocument extends Document {
  userId: mongoose.Types.ObjectId;
  items: ICartItemSchema[];
  updatedAt: Date;
}

// Schema for individual cart items
const CartItemSchema = new Schema<ICartItemSchema>(
  {
    productId: {
      type: Schema.Types.ObjectId,
      ref: "Product", // References the Product model
      required: true,
    },
    name: { type: String, required: true },
    price: { type: Number, required: true },
    quantity: {
      type: Number,
      required: true,
      min: [1, "Quantity must be at least 1"],
    },
  },
  { _id: false } // Don't create separate _id for sub-documents
);

const CartSchema = new Schema<ICartDocument>(
  {
    userId: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
      unique: true, // One cart per user
    },
    items: {
      type: [CartItemSchema],
      default: [],
    },
  },
  {
    timestamps: { createdAt: false, updatedAt: true },
  }
);

const Cart: Model<ICartDocument> =
  mongoose.models.Cart || mongoose.model<ICartDocument>("Cart", CartSchema);

export default Cart;
