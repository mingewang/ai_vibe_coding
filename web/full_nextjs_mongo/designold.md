# Design Document — E-Commerce Shopping Site

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│  Pages (App Router)     │     Reusable Components            │
│  /                      │     Navbar, ProductCard,           │
│  /products              │     SearchBar, Pagination,         │
│  /products/[id]         │     AuthForm, LoadingSpinner       │
│  /auth/login            │                                    │
│  /auth/register         │     State: React Context (Auth,    │
│  /cart                  │            Cart)                   │
│  /orders                │                                    │
│  /admin/products        │                                    │
└──────────┬──────────────────────────────────────────────────┘
           │ fetch() / axios
           ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend (Next.js API Routes)                    │
│                                                              │
│  /api/auth/*        →  Register / Login / Session           │
│  /api/products/*    →  CRUD + Search + Pagination           │
│  /api/cart/*        →  Add / Remove / Get Cart              │
│  /api/orders/*      →  Place order / Order history          │
│  /api/admin/*       →  Admin-only product management        │
│                                                              │
│  Middleware: auth check, input validation, error handling
│  Language: TypeScript             │    │
└──────────┬──────────────────────────────────────────────────┘
           │ mongoose
           ▼
┌─────────────────────────────────────────────────────────────┐
│              Database (MongoDB Atlas)                        │
│                                                              │
│  Collections:                                                │
│  users        │  products      │  carts       │  orders     │
│  favorites    │  categories    │  reviews     │             │
└─────────────────────────────────────────────────────────────┘
```

**Data flow (example: user searches products)**  
1. User types "wireless" in SearchBar and clicks Search.  
2. Frontend sends `GET /api/products?search=wireless&page=1`.  
3. API route queries MongoDB using a regex filter on product name/description.  
4. MongoDB returns matching documents; API adds pagination metadata.  
5. Frontend receives JSON, updates the product list UI.  
6. ProductCard components render each result.

---

## 2. Pages

| Route                | Page Name         | Purpose                                    |
|----------------------|-------------------|--------------------------------------------|
| `/`                  | HomePage          | Hero banner, featured products, categories |
| `/products`          | ProductListPage   | Browse all products with search & filters  |
| `/products/[id]`     | ProductDetailPage | Full product info, reviews, add to cart    |
| `/auth/login`        | LoginPage         | Email/password login form                  |
| `/auth/register`     | RegisterPage      | New user registration form                 |
| `/cart`              | CartPage          | View cart items, update qty, proceed       |
| `/orders`            | OrderHistoryPage  | List of past orders for logged-in user     |
| `/orders/[id]`       | OrderDetailPage   | Single order details and status            |
| `/admin/products`    | AdminProductsPage | Product CRUD table for admins              |
| `/admin/products/new`| AdminProductForm  | Create a new product                       |
| `/admin/products/[id]/edit` | AdminProductForm | Edit an existing product             |
| `/profile`           | ProfilePage       | View/edit name, email, password            |

**Layout structure:**

```
app/layout.tsx         →  Navbar + Footer (wraps all pages)
app/page.tsx           →  HomePage (Server Component)
app/products/layout.tsx →  Category sidebar (shared on product pages)
app/admin/layout.tsx   →  Admin wrapper
app/auth/layout.tsx    →  Centered card layout (login/register)
```

---

## 3. Database Schema

### users
| Field       | Type     | Notes                    |
|-------------|----------|--------------------------|
| `_id`       | ObjectId | Auto-generated           |
| `name`      | String   | Required                 |
| `email`     | String   | Required, unique         |
| `password`  | String   | Hashed (bcrypt)          |
| `role`      | String   | `"user"` or `"admin"`    |
| `createdAt` | Date     | Auto                     |

### products
| Field        | Type     | Notes                          |
|--------------|----------|--------------------------------|
| `_id`        | ObjectId | Auto-generated                 |
| `name`       | String   | Required                       |
| `description`| String   | Required                       |
| `price`      | Number   | Required, > 0                  |
| `category`   | String   | e.g. "Electronics", "Clothing" |
| `imageUrl`   | String   | URL to product image           |
| `stock`      | Number   | Integer, >= 0                  |
| `createdAt`  | Date     | Auto                           |

### carts
| Field      | Type            | Notes                         |
|------------|-----------------|-------------------------------|
| `_id`      | ObjectId        | Auto-generated                |
| `userId`   | ObjectId        | Reference to `users._id`      |
| `items`    | Array of objects| See items sub-schema below    |
| `updatedAt`| Date            | Auto                          |

**cart.items[] sub-schema:**
| Field      | Type     | Notes                    |
|------------|----------|--------------------------|
| `productId`| ObjectId | Reference to `products`  |
| `name`     | String   | Snapshot at add time     |
| `price`    | Number   | Snapshot at add time     |
| `quantity` | Number   | >= 1                     |

### orders
| Field       | Type            | Notes                         |
|-------------|-----------------|-------------------------------|
| `_id`       | ObjectId        | Auto-generated                |
| `userId`    | ObjectId        | Reference to `users._id`      |
| `items`     | Array of objects| Same shape as cart items      |
| `total`     | Number          | Sum of all item prices        |
| `status`    | String          | `"pending"`, `"shipped"`, etc |
| `createdAt` | Date            | Auto                          |

### categories *(optional, for filtering)*
| Field  | Type   | Notes          |
|--------|--------|----------------|
| `_id`  | ObjectId | Auto-generated |
| `name` | String | Unique          |

### reviews *(optional stretch feature)*
| Field      | Type     | Notes                    |
|------------|----------|--------------------------|
| `_id`      | ObjectId | Auto-generated           |
| `productId`| ObjectId | Reference to `products`  |
| `userId`   | ObjectId | Reference to `users`     |
| `rating`   | Number   | 1-5                      |
| `comment`  | String   |                          |
| `createdAt`| Date     | Auto                     |

---

## 4. API Endpoints

### Auth
| Method | Route                  | Purpose                     |
|--------|------------------------|-----------------------------|
| POST   | `/api/auth/register`   | Create new user account     |
| POST   | `/api/auth/login`      | Authenticate, return token  |
| GET    | `/api/auth/me`         | Get current user from token |

### Products
| Method | Route                  | Purpose                                |
|--------|------------------------|----------------------------------------|
| GET    | `/api/products`        | List products (search, filter, page)   |
| GET    | `/api/products/[id]`   | Get single product by ID               |
| POST   | `/api/products`        | Create product (admin only)            |
| PUT    | `/api/products/[id]`   | Update product (admin only)            |
| DELETE | `/api/products/[id]`   | Delete product (admin only)            |

### Cart
| Method | Route                  | Purpose                     |
|--------|------------------------|-----------------------------|
| GET    | `/api/cart`            | Get current user's cart     |
| POST   | `/api/cart`            | Add item to cart            |
| PUT    | `/api/cart`            | Update item quantity        |
| DELETE  | `/api/cart?productId=x`| Remove item from cart       |

### Orders
| Method | Route                  | Purpose                     |
|--------|------------------------|-----------------------------|
| GET    | `/api/orders`          | List current user's orders  |
| POST   | `/api/orders`          | Place order (from cart)     |
| GET    | `/api/orders/[id]`     | Get single order details    |

### Search query params on `GET /api/products`
| Param    | Example         | Purpose                     |
|----------|-----------------|-----------------------------|
| `search` | `?search=phone`  | Full-text match on name/desc|
| `category`| `?category=Electronics` | Filter by category |
| `minPrice`| `?minPrice=10`  | Minimum price filter        |
| `maxPrice`| `?maxPrice=500` | Maximum price filter        |
| `page`   | `?page=2`       | Page number for pagination  |
| `limit`  | `?limit=12`     | Items per page (default 12) |

**Response shape for `GET /api/products`:**
```json
{
  "products": [ { ... }, { ... } ],
  "page": 1,
  "totalPages": 5,
  "totalProducts": 58
}
```

---

## 5. UI Components

| Component            | Used In                        | Purpose                              |
|----------------------|--------------------------------|--------------------------------------|
| `Navbar`             | Root layout                    | Logo, nav links, cart icon, auth btn |
| `Footer`             | Root layout                    | Copyright, quick links               |
| `ProductCard`        | ProductListPage, HomePage      | Image, name, price — clickable card  |
| `ProductGrid`        | ProductListPage, HomePage      | Responsive grid of ProductCards      |
| `SearchBar`          | ProductListPage                | Text input + submit for search       |
| `FilterSidebar`      | ProductListPage                | Category, price range filters        |
| `Pagination`         | ProductListPage                | Page number buttons                  |
| `AuthForm`           | LoginPage, RegisterPage        | Email/password form with validation  |
| `CartItem`           | CartPage                       | Single cart row with qty controls    |
| `CartSummary`        | CartPage                       | Subtotal, total, checkout button     |
| `OrderCard`          | OrderHistoryPage               | Order summary (date, total, status)  |
| `AdminProductTable`  | AdminProductsPage              | Table with edit/delete actions       |
| `AdminProductForm`   | AdminProductForm pages         | Form fields for product CRUD         |
| `LoadingSpinner`     | Any page                       | Shows while data is loading          |
| `EmptyState`         | CartPage, OrderHistoryPage     | "No items yet" message + CTA         |
| `ProtectedRoute`     | Wraps auth-required pages      | Redirects to login if not authed     |

**Component tree example (ProductListPage):**
```
ProductListPage
├── SearchBar
├── FilterSidebar
├── ProductGrid
│   ├── ProductCard  (×N)
│   └── ProductCard
└── Pagination
```

---

## 6. AI Integration Flow

> The current project does not include AI features (per proposal.md).  
> Below is a **learning roadmap** for adding AI later.

### Option A: AI Search (Semantic Search)

```
User types query
      │
      ▼
Frontend sends  POST  /api/ai/search   with  { query: "wireless headphones" }
      │
      ▼
API route calls OpenAI Embeddings API → converts query to vector (1536 dimensions)
      │
      ▼
MongoDB Atlas Vector Search finds the 10 most similar product embeddings
      │
      ▼
Return top matching products  →  Frontend renders them
```

**Files to create:**
- `lib/embeddings.js` — helper to call OpenAI embeddings API
- `app/api/ai/search/route.ts` — search endpoint
- A script to pre-compute & store embeddings for all products

### Option B: AI Recommendations

```
User visits product detail page
      │
      ▼
Frontend calls  GET  /api/ai/recommendations?productId=xxx
      │
      ▼
API route finds category + tags of current product
      │
      ▼
Queries MongoDB for similar products (same category, similar price range)
      │
      ▼
Optionally re-rank with OpenAI: "given this product, rank these candidates"
      │
      ▼
Return top 5 recommendations  →  Frontend renders "You may also like" section
```

### Option C: AI Chat Assistant

```
User clicks chat bubble → Chat panel opens
      │
      ▼
User types "What laptops do you have under $1000?"
      │
      ▼
Frontend sends  POST  /api/ai/chat  { messages: [...] }
      │
      ▼
API route builds context: product catalog summary + user query
      │
      ▼
Calls OpenAI Chat Completions with system prompt → gets answer
      │
      ▼
Stream response back to frontend  →  Renders in chat UI
```

### Files needed for any AI feature
- `/lib/openai.ts` — shared OpenAI client initialization
- `/.env.local` — add `OPENAI_API_KEY=sk-...`
- `npm install openai`

---

## 7. Implementation Notes

### Step 1: Next.js setup (TypeScript)
```bash
npx create-next-app@latest ecommerce-app --app --tailwind --eslint --typescript
cd ecommerce-app
npm install mongoose bcryptjs jsonwebtoken
npm install -D @types/bcryptjs @types/jsonwebtoken
```

### Step 2: Folder structure (TypeScript)
```
app/
  api/
    auth/register/route.tsx
    auth/login/route.tsx
    auth/me/route.tsx
    products/route.tsx
    products/[id]/route.tsx
    cart/route.tsx
    orders/route.tsx
    orders/[id]/route.tsx
  auth/
    login/page.tsx
    register/page.tsx
  cart/page.tsx
  orders/page.tsx
  orders/[id]/page.tsx
  admin/
    products/page.tsx
    products/new/page.tsx
    products/[id]/edit/page.tsx
  profile/page.tsx
  layout.tsx
  page.tsx
  globals.css
lib/
  db.ts              → MongoDB connection
  models/
    User.ts
    Product.ts
    Cart.ts
    Order.ts
  auth.ts            → JWT token helpers
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
  index.ts           → Shared interfaces & prop types
middleware.ts         → Auth middleware (optional)
.env.local            → Environment variables
tsconfig.json         → TypeScript configuration
```

### Step 3: MongoDB connection (`lib/db.ts`)
```typescript
import mongoose from "mongoose";

const MONGODB_URI = process.env.MONGODB_URI;

interface MongooseCache {
  conn: typeof mongoose | null;
  promise: Promise<typeof mongoose> | null;
}

declare global {
  var mongoose: MongooseCache | undefined;
}

const cached: MongooseCache = global.mongoose || { conn: null, promise: null };

if (!global.mongoose) {
  global.mongoose = cached;
}

export async function connectDB(): Promise<typeof mongoose> {
  if (cached.conn) return cached.conn;
  if (!cached.promise) {
    cached.promise = mongoose.connect(MONGODB_URI, {
      bufferCommands: false,
    });
  }
  cached.conn = await cached.promise;
  return cached.conn;
}
```

### Step 4: Environment variables (`.env.local`)
```
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.xxxxx.mongodb.net/ecommerce
JWT_SECRET=your-secret-key-change-in-production
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Step 5: Key implementation tips for students

| Concept              | Tip                                                              |
|----------------------|------------------------------------------------------------------|
| Auth                 | Store JWT in `httpOnly` cookie or `localStorage`. Use context (`AuthContext`) to share user state. |
| Cart persistence     | Store cart in MongoDB (logged-in) OR localStorage (guest). Merge on login. |
| Admin protection     | Check `user.role === "admin"` in API routes + redirect on frontend. |
| Image upload         | Start with external URLs; later add upload to Cloudinary or S3.  |
| Search               | Use MongoDB `$regex` for simple search, or `$text` index for faster full-text. |
| Pagination           | Use `.skip().limit()` with `totalDocuments` count for page numbers. |
| Error handling       | Wrap API routes in try/catch, return `{ error: "message" }` consistently. |
| Styling              | Keep Tailwind utility classes minimal. Define a color palette in `tailwind.config.js`. |
| TypeScript           | Define all interfaces in `types/index.ts`. Use strict mode in `tsconfig.json`. |

### Step 6: Run the project
```bash
npm run dev
# Open http://localhost:3000
```
