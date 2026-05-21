// ============================================================
// Shared TypeScript Types & Interfaces
// These are used across the whole app so we have one source of truth.
// ============================================================

// --- User ---
export interface IUser {
  _id: string;
  name: string;
  email: string;
  role: "user" | "admin";
  createdAt?: string;
}

// Used when creating/updating a user (no _id yet, no timestamps)
export interface IUserInput {
  name: string;
  email: string;
  password: string;
}

// --- Product ---
export interface IProduct {
  _id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  imageUrl: string;
  stock: number;
  createdAt?: string;
}

export interface IProductInput {
  name: string;
  description: string;
  price: number;
  category: string;
  imageUrl: string;
  stock: number;
}

// --- Cart ---
export interface ICartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
}

export interface ICart {
  _id: string;
  userId: string;
  items: ICartItem[];
}

// --- Order ---
export interface IOrder {
  _id: string;
  userId: string;
  items: ICartItem[];
  total: number;
  status: "pending" | "shipped" | "delivered" | "cancelled";
  createdAt?: string;
}

// --- API Response Wrappers ---
export interface IApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface IPaginatedResponse<T> {
  data: T[];
  page: number;
  totalPages: number;
  totalItems: number;
}

// --- JWT payload stored inside the token ---
export interface IJwtPayload {
  userId: string;
  email: string;
  role: "user" | "admin";
}
