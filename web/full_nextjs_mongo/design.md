# Design Document — E-Commerce Shopping Site

> A student-friendly guide to building this full-stack project.  
> Read each section in order — they build on each other.

---

## 1. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js App Router)                  │
│                                                                  │
│  Pages (Server + Client Components)                              │
│  /  /products  /products/[id]  /cart  /orders  /auth/*  /admin/*│
│                                                                  │
│  Reusable Components:  Navbar · ProductCard · SearchBar · etc.   │
│  State Management:     AuthContext (JWT) + CartContext (MongoDB)  │
├──────────────────────────────────────────────────────────────────┤
│                       API CALLS (fetch / axios)                   │
├──────────────────────────────────────────────────────────────────┤
│                    BACKEND (Next.js API Routes)                   │
│                                                                  │
│  /api/auth/*       →  Register, Login, Get Me                   │
│  /api/products/*   →  CRUD + Search + Filter + Paginate          │
│  /api/cart/*       →  Add, Remove, Update Cart Items             │
│  /api/orders/*     →  Place Order, View History                  │
│                                                                  │
│  Middleware:  Auth check (JWT verify) · Validation · Error wrap  │
├──────────────────────────────────────────────────────────────────┤
│                     Mongoose (ODM)                                │
├──────────────────────────────────────────────────────────────────┤
│                    DATABASE (MongoDB Atlas)                       │
│                                                                  │
│  Collections:  users · products · carts · orders                 │
└──────────────────────────────────────────────────────────────────┘
```

### How data flows (example: user searches "laptop")

```
1. User types "laptop" in SearchBar, clicks Search
2. Frontend calls → GET /api/products?search=laptop&page=1
3. API route queries MongoDB with regex on name/description
4. MongoDB returns matching products
5. API adds pagination metadata (page, totalPages, totalProducts)
6. Frontend receives JSON → updates ProductGrid state → renders ProductCards
```

**Key idea:** Next.js handles both frontend and backend in one project.  
The `app/` folder contains pages (what users see) and the `app/api/` folder contains API routes (what handles data).

---

## 2. Pages (Routes)

All pages live inside `app/` using Next.js App Router conventions:

| Route | File | Type | Purpose |
|-------|------|------|---------|
| `/` | `app/page.tsx` | Server | Home page — hero banner, featured products, category links |
| `/products` | `app/products/page.tsx` | Client | Browse all products with search bar, filters, and pagination |
| `/products/[id]` | `app/products/[id]/page.tsx` | Client | Product detail — image, price, description, add to cart |
| `/auth/login` | `app/auth/login/page.tsx` | Client | Login form (email + password) |
| `/auth/register` | `app/auth/register/page.tsx` | Client | Registration form (name, email, password) |
| `/cart` | `app/cart/page.tsx` | Client | View cart items, update quantities, proceed to checkout |
| `/orders` | `app/orders/page.tsx` | Client | Order history for logged-in user |
| `/orders/[id]` | `app/orders/[id]/page.tsx` | Client | Single order detail with status |
| `/profile` | `app/profile/page.tsx` | Client | View/edit user profile information |
| `/admin/products` | `app/admin/products/page.tsx` | Client | Admin product management table |
| `/admin/products/new` | `app/admin/products/new/page.tsx` | Client | Create new product form |
| `/admin/products/[id]/edit` | `app/admin/products/[id]/edit/page.tsx` | Client | Edit existing product form |

### Layout nesting

```
app/layout.tsx                   →  Navbar + Footer (wraps every page)
  app/page.tsx                   →  HomePage
  app/products/layout.tsx        →  Optional: category sidebar
    app/products/page.tsx
    app/products/[id]/page.tsx
  app/auth/layout.tsx            →  Centered card layout
    app/auth/login/page.tsx
    app/auth/register/page.tsx
  app/admin/layout.tsx           →  Admin sidebar + auth guard
    app/admin/products/page.tsx
    app/admin/products/new/page.tsx
    app/admin/products/[id]/edit/page.tsx
  app/(user)/layout.tsx          →  Protected route wrapper
    app/(user)/cart/page.tsx
    app/(user)/orders/page.tsx
    app/(user)/orders/[id]/page.tsx
    app/(user)/profile/page.tsx
```

> **Student tip:** Route groups `(user)` let you group pages without changing the URL.  
> Use them to apply shared layouts or middleware.

---

## 3. Database Schema (MongoDB + Mongoose)

### Users Collection

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `_id` | `ObjectId` | Auto | MongoDB auto-generates this |
| `name` | `String` | Yes | User's full name |
| `email` | `String` | Yes | Unique — used for login |
| `password` | `String` | Yes | Stored as bcrypt hash (never plain text) |
| `role` | `String` | Yes | `"user"` or `"admin"` (default: `"user"`) |
| `createdAt` | `Date` | Auto | `timestamps: true` in Mongoose |

### Products Collection

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `_id` | `ObjectId` | Auto | MongoDB auto-generates this |
| `name` | `String` | Yes | Product title |
| `description` | `String` | Yes | Product description |
| `price` | `Number` | Yes | Must be > 0 |
| `category` | `String` | Yes | e.g. "Electronics", "Clothing", "Books" |
| `imageUrl` | `String` | Yes | URL to product image |
| `stock` | `Number` | Yes | Integer, >= 0 — tracks available quantity |
| `createdAt` | `Date` | Auto | `timestamps: true` |

### Carts Collection

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `_id` | `ObjectId` | Auto | MongoDB auto-generates this |
| `userId` | `ObjectId` (ref: Users) | Yes | Links cart to a user |
| `items` | `Array` | Yes | Array of cart item objects (see below) |
| `updatedAt` | `Date` | Auto | `timestamps: true` |

**cart.items[] sub-schema:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `productId` | `ObjectId` (ref: Products) | Yes | Links to the product |
| `name` | `String` | Yes | Copied from product at add time |
| `price` | `Number` | Yes | Copied from product at add time |
| `quantity` | `Number` | Yes | >= 1 |

> **Why snapshot name + price?** If the admin later changes a product name or price, the user's cart still shows what they agreed to.

### Orders Collection

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `_id` | `ObjectId` | Auto | MongoDB auto-generates this |
| `userId` | `ObjectId` (ref: Users) | Yes | Links order to a user |
| `items` | `Array` | Yes | Same structure as cart items |
| `total` | `Number` | Yes | Sum of (price × quantity) for all items |
| `status` | `String` | Yes | `"pending"`, `"shipped"`, `"delivered"`, `"cancelled"` |
| `createdAt` | `Date` | Auto | `timestamps: true` |

### Relationship diagram

```
users ──< carts      (one user → one cart)
users ──< orders     (one user → many orders)
products ──< cart.items  (one product → many cart entries)
products ──< order.items (one product → many order entries)
```

> **Student tip:** A "one-to-many" relationship (users → orders) means one user has many orders.  
> The `userId` field inside the `orders` collection is called a **foreign key** — it points back to the user.

---

## 4. API Endpoints

All endpoints live in `app/api/` and use Route Handlers (`route.ts`).

### Auth

| Method | Route | Purpose | Auth Required |
|--------|-------|---------|---------------|
| POST | `/api/auth/register` | Create new user account (hash password with bcrypt) | No |
| POST | `/api/auth/login` | Verify credentials, return JWT token | No |
| GET | `/api/auth/me` | Get current user info from JWT token | Yes |

### Products

| Method | Route | Purpose | Auth Required |
|--------|-------|---------|---------------|
| GET | `/api/products` | List products (supports search, filter, pagination) | No |
| GET | `/api/products/[id]` | Get single product by ID | No |
| POST | `/api/products` | Create a new product | Admin only |
| PUT | `/api/products/[id]` | Update an existing product | Admin only |
| DELETE | `/api/products/[id]` | Delete a product | Admin only |

### Cart

| Method | Route | Purpose | Auth Required |
|--------|-------|---------|---------------|
| GET | `/api/cart` | Get current user's cart with populated items | Yes |
| POST | `/api/cart` | Add item to cart (or increment quantity if exists) | Yes |
| PUT | `/api/cart` | Update item quantity for a product in cart | Yes |
| DELETE | `/api/cart/items/[productId]` | Remove a specific item from cart | Yes |

### Orders

| Method | Route | Purpose | Auth Required |
|--------|-------|---------|---------------|
| GET | `/api/orders` | List current user's orders (sorted by newest first) | Yes |
| POST | `/api/orders` | Convert cart items into an order (clears cart) | Yes |
| GET | `/api/orders/[id]` | Get a single order's details | Yes |

### Query parameters for `GET /api/products`

| Param | Type | Example | Purpose |
|-------|------|---------|---------|
| `search` | `string` | `?search=laptop` | Partial match on product name/description |
| `category` | `string` | `?category=Electronics` | Exact match on category field |
| `minPrice` | `number` | `?minPrice=10` | Minimum price filter (>=) |
| `maxPrice` | `number` | `?maxPrice=500` | Maximum price filter (<=) |
| `page` | `number` | `?page=2` | Page number (default: 1) |
| `limit` | `number` | `?limit=12` | Items per page (default: 12) |

### Example response: `GET /api/products?search=phone&page=1`

```json
{
  "products": [
    {
      "_id": "abc123",
      "name": "Wireless Phone Charger",
      "price": 29.99,
      "category": "Electronics",
      "imageUrl": "https://example.com/charger.jpg",
      "stock": 15
    }
  ],
  "page": 1,
  "totalPages": 3,
  "totalProducts": 25
}
```

> **Student tip:** API routes are just regular TypeScript files that export functions named after HTTP methods.  
> Example: `export async function GET(request) { ... }` handles GET requests.

---

## 5. UI Components

All reusable components live in `components/`. They are building blocks you combine to create pages.

### Component list

| Component | Where It's Used | What It Does |
|-----------|----------------|--------------|
| `Navbar` | Root layout (`app/layout.tsx`) | Logo, navigation links, cart icon with badge, login/logout button |
| `Footer` | Root layout (`app/layout.tsx`) | Copyright, quick links, social icons |
| `ProductCard` | HomePage, ProductListPage | Card with product image, name, price — clickable to detail page |
| `ProductGrid` | HomePage, ProductListPage | Responsive CSS grid wrapper that arranges ProductCards |
| `SearchBar` | ProductListPage | Text input + submit button — triggers search on enter/click |
| `FilterSidebar` | ProductListPage | Category checkboxes + min/max price inputs — updates URL params |
| `Pagination` | ProductListPage | Page number buttons (prev, 1, 2, 3, ..., next) |
| `AuthForm` | LoginPage, RegisterPage | Shared form component — email, password, validation, error display |
| `CartItem` | CartPage | Single cart row: product image, name, price, quantity controls, remove button |
| `CartSummary` | CartPage | Subtotal, total, checkout button |
| `OrderCard` | OrderHistoryPage | Order summary card: date, item count, total, status badge |
| `AdminProductTable` | AdminProductsPage | Table with columns for name, price, stock — edit/delete action buttons |
| `AdminProductForm` | `/admin/products/new`, `/admin/products/[id]/edit` | Form with all product fields, validation, save/cancel buttons |
| `LoadingSpinner` | Any page | Simple spinner or skeleton shown while data loads |
| `EmptyState` | CartPage, OrderHistoryPage | Friendly message + call-to-action button when there's no data |
| `ProtectedRoute` | Wraps auth-required pages | Checks for JWT token — redirects to login if missing |

### Component tree example: ProductListPage

```
ProductListPage (client component)
├── SearchBar
├── FilterSidebar (category + price range)
├── ProductGrid
│   ├── ProductCard (product 1)
│   ├── ProductCard (product 2)
│   ├── ProductCard (product 3)
│   └── ... (N items, one per product)
├── Pagination (page 1, 2, 3 ...)
└── LoadingSpinner (shown during fetch)
```

### State management plan

| State | Tool | Where | What it holds |
|-------|------|-------|---------------|
| Auth state | React Context (`AuthContext`) | `context/AuthContext.tsx` | Current user object, JWT token, login/logout/register functions |
| Cart state | React Context (`CartContext`) | `context/CartContext.tsx` | Cart items array, add/remove/update functions, item count |

> **Student tip:** React Context lets you share state across multiple pages without passing props manually.  
> Wrap your layout with `<AuthProvider>` and `<CartProvider>` so every page has access.

---

## 6. AI Integration Flow

> **Per the proposal:** No AI features are implemented in this version.  
> This project focuses on core e-commerce functionality (CRUD, auth, search, cart, orders).  
> The section below is intentionally empty — AI can be explored as a future stretch goal.

```
┌─────────────────────────────────────────────────────────────────┐
│                  NOT IN SCOPE (per proposal.md)                  │
│                                                                  │
│  Possible future additions:                                      │
│    • Semantic product search (OpenAI embeddings + Vector Search) │
│    • Product recommendations ("You may also like")              │
│    • Chat assistant for product questions                        │
│                                                                  │
│  Focus on: Auth · Products CRUD · Cart · Orders · Search/Filter  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Implementation Notes

### Step 1: Create the Next.js project

```bash
npx create-next-app@latest . --app --tailwind --eslint --typescript
```

This creates a Next.js project with:
- **App Router** (`app/` folder) — modern Next.js routing
- **Tailwind CSS** — utility-first styling
- **ESLint** — code quality checks
- **TypeScript** — type safety

### Step 2: Install dependencies

```bash
npm install mongoose bcryptjs jsonwebtoken
npm install -D @types/bcryptjs @types/jsonwebtoken
```

| Package | Purpose |
|---------|---------|
| `mongoose` | Connect to MongoDB, define schemas, run queries |
| `bcryptjs` | Hash passwords before storing |
| `jsonwebtoken` | Create and verify JWT tokens for auth |

### Step 3: Set up folder structure

```
app/
  api/
    auth/
      register/route.ts      → POST handler
      login/route.ts         → POST handler
      me/route.ts            → GET handler
    products/
      route.ts               → GET (list), POST (create)
      [id]/route.ts          → GET, PUT, DELETE
    cart/
      route.ts               → GET, POST, PUT
      items/[productId]/route.ts → DELETE
    orders/
      route.ts               → GET, POST
      [id]/route.ts          → GET
  (user)/
    cart/page.tsx
    orders/
      page.tsx
      [id]/page.tsx
    profile/page.tsx
  admin/
    products/
      page.tsx
      new/page.tsx
      [id]/edit/page.tsx
  auth/
    login/page.tsx
    register/page.tsx
  products/
    page.tsx
    [id]/page.tsx
  layout.tsx
  page.tsx
  globals.css
lib/
  db.ts                     → MongoDB connection (singleton pattern)
  models/
    User.ts
    Product.ts
    Cart.ts
    Order.ts
  auth.ts                   → JWT sign/verify helpers
components/
  Navbar.tsx
  Footer.tsx
  ProductCard.tsx
  ProductGrid.tsx
  SearchBar.tsx
  FilterSidebar.tsx
  Pagination.tsx
  AuthForm.tsx
  CartItem.tsx
  CartSummary.tsx
  OrderCard.tsx
  AdminProductTable.tsx
  AdminProductForm.tsx
  LoadingSpinner.tsx
  EmptyState.tsx
  ProtectedRoute.tsx
context/
  AuthContext.tsx
  CartContext.tsx
types/
  index.ts                  → Shared TypeScript interfaces
middleware.ts               → Optional: route-level auth check
.env.local                  → Environment variables (never commit this!)
next.config.ts              → Next.js configuration
tailwind.config.ts          → Tailwind customization
tsconfig.json               → TypeScript config (strict: true)
```

### Step 4: MongoDB connection (`lib/db.ts`)

Use a cached connection to avoid creating multiple connections during hot reloads:

```typescript
import mongoose from "mongoose";

const MONGODB_URI = process.env.MONGODB_URI!;

interface MongooseCache {
  conn: typeof mongoose | null;
  promise: Promise<typeof mongoose> | null;
}

declare global {
  var mongooseCache: MongooseCache | undefined;
}

const cached: MongooseCache = global.mongooseCache ?? { conn: null, promise: null };

if (!global.mongooseCache) {
  global.mongooseCache = cached;
}

export async function connectDB(): Promise<typeof mongoose> {
  if (cached.conn) return cached.conn;
  if (!cached.promise) {
    cached.promise = mongoose.connect(MONGODB_URI).then((m) => m);
  }
  cached.conn = await cached.promise;
  return cached.conn;
}
```

> **Why the cache?** Next.js's hot module replacement can call `connectDB()` many times during development.  
> The cache ensures only one connection is ever created.

### Step 5: Set up environment variables (`.env.local`)

```bash
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster.xxxxx.mongodb.net/ecommerce
JWT_SECRET=your-secret-key-change-in-production
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

> **Never commit `.env.local`** to Git. The `.gitignore` file created by `create-next-app` already ignores it.

### Step 6: Run the project

```bash
npm run dev
# Open http://localhost:3000 in your browser
```

### Handbook: Tips for common challenges

| Challenge | How to handle it |
|-----------|-----------------|
| **Authentication** | Store JWT in a cookie (httpOnly for security). Use `AuthContext` to track login state globally. Add `ProtectedRoute` component to redirect unauthenticated users. |
| **Cart persistence** | For logged-in users: store cart in MongoDB `carts` collection. For guests: store in `localStorage`. Merge guest cart into user cart on login. |
| **Admin-only features** | In API routes: check `user.role === "admin"` from the decoded JWT and return 403 if not. In frontend: hide admin UI from non-admin users. |
| **Image uploads** | Start simple — store external image URLs. For production, add Cloudinary upload later. |
| **Search** | Use MongoDB `$regex` for simple case-insensitive search. For better performance, create a text index on `name` and `description`. |
| **Pagination** | Use Mongoose's `.skip((page - 1) * limit).limit(limit)` with a separate `countDocuments()` call for total page count. |
| **Error handling** | Wrap every API route in try/catch. Return `{ error: "message" }` with appropriate HTTP status codes. On the frontend, show errors in a toast or inline. |
| **TypeScript** | Define all interfaces in `types/index.ts`. Start each component by defining its props type. Use `strict: true` in `tsconfig.json`. |
| **Styling** | Stick to Tailwind utility classes. Define a color palette in `tailwind.config.ts` using `theme.extend.colors`. Keep components responsive with `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`. |
| **Data fetching** | Use Server Components for public data (product list). Use Client Components (`useEffect` + `fetch`) for user-specific data (cart, orders). |

---

## Quick Reference: Key TypeScript Interfaces

Put these in `types/index.ts` to share types across your app:

```typescript
// User
interface IUser {
  _id: string;
  name: string;
  email: string;
  role: "user" | "admin";
  createdAt: Date;
}

// Product
interface IProduct {
  _id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  imageUrl: string;
  stock: number;
  createdAt: Date;
}

// Cart Item
interface ICartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
}

// Cart
interface ICart {
  _id: string;
  userId: string;
  items: ICartItem[];
}

// Order
interface IOrder {
  _id: string;
  userId: string;
  items: ICartItem[];
  total: number;
  status: "pending" | "shipped" | "delivered" | "cancelled";
  createdAt: Date;
}

// API Response (for paginated lists)
interface IPaginatedResponse<T> {
  data: T[];
  page: number;
  totalPages: number;
  totalItems: number;
}
```

---

## Summary: What You Will Build

```
A full-stack e-commerce app where:
  ─ Visitors can browse, search, and filter products
  ─ Users can register, log in, manage cart, and place orders
  ─ Admins can create, edit, and delete products
  ─ All data persists in MongoDB
  ─ Authentication uses JWT + bcrypt
  ─ Everything is type-safe with TypeScript
```

> **Start with auth** (register + login) — every other feature depends on it.  
> **Then build products CRUD** — the core of the app.  
> **Then add cart + orders** — the transaction flow.  
> **Polish with search, filters, and pagination** — the user experience.
