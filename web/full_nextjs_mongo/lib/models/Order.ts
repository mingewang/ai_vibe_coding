// ============================================================
// Order Model (lib/models/Order.ts)
// ============================================================
// Defines the structure of an order document in MongoDB.
// When a user checks out, their cart items are saved as an order.
// ============================================================

import mongoose, { Schema, Document, Model } from "mongoose";
import { ICartItemSchema } from "./Cart";

export interface IOrderDocument extends Document {
  userId: mongoose.Types.ObjectId;
  items: ICartItemSchema[];
  total: number;
  status: "pending" | "shipped" | "delivered" | "cancelled";
  createdAt: Date;
  updatedAt: Date;
}

const OrderItemSchema = new Schema<ICartItemSchema>(
  {
    productId: {
      type: Schema.Types.ObjectId,
      ref: "Product",
      required: true,
    },
    name: { type: String, required: true },
    price: { type: Number, required: true },
    quantity: { type: Number, required: true },
  },
  { _id: false }
);

const OrderSchema = new Schema<IOrderDocument>(
  {
    userId: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    items: {
      type: [OrderItemSchema],
      required: true,
    },
    total: {
      type: Number,
      required: true,
    },
    status: {
      type: String,
      enum: ["pending", "shipped", "delivered", "cancelled"],
      default: "pending",
    },
  },
  {
    timestamps: true,
  }
);

const Order: Model<IOrderDocument> =
  mongoose.models.Order ||
  mongoose.model<IOrderDocument>("Order", OrderSchema);

export default Order;
