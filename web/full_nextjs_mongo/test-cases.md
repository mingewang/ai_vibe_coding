# Test Cases — E-Commerce Shopping Site

This document guides you through testing every feature in the app.  
Test in order — each section builds on the previous one.

---

## 1. Quick Sanity Check

Before running detailed tests, make sure the app starts:

```bash
npm run dev
# Open http://localhost:3000
```

You should see:
- A "Welcome to ShopNext" hero banner
- A "New Arrivals" section with 0 products (you haven't added any yet)
- A navigation bar with: Products, Cart, Login, Sign Up

If you see this, the app is running. If not, check the troubleshooting section.

---

## 2. Manual Test Steps (End-to-End Flow)

Test the full user journey from start to finish.

### 2.1 Registration

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Sign Up" in the navbar | You see the registration form |
| 2 | Enter a name, email, and password (min 6 chars) | Fields are filled |
| 3 | Click "Create Account" | You're redirected to the home page |
| 4 | Look at the navbar | Shows your name (or no name, just logout/admin links) — actually shows Logout, Orders, Profile |
| 5 | Click "Profile" | You see your name, email, role ("user"), and "Member since" date |

**Test edge cases:**

| Test | Expected |
|------|----------|
| Register with the same email again | Error: "An account with this email already exists" |
| Register with password < 6 characters | Error: "Password must be at least 6 characters" |
| Leave a field blank | Browser validation prevents submission |

### 2.2 Login

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Logout" in the navbar | You're logged out (nav shows Login/Sign Up) |
| 2 | Click "Login" | You see the login form |
| 3 | Enter the email and password you registered with | Fields are filled |
| 4 | Click "Log In" | You're redirected to the home page, navbar shows Logout/Orders/Profile |

**Test edge cases:**

| Test | Expected |
|------|----------|
| Login with wrong password | Error: "Invalid email or password" |
| Login with unregistered email | Error: "Invalid email or password" |

### 2.3 Adding Products (Admin)

To add products, you need an admin account.  
For testing, you can make yourself an admin directly in MongoDB:

```bash
# Option 1: Use MongoDB Compass (GUI)
# 1. Open your MongoDB Atlas cluster in Compass
# 2. Go to the "users" collection
# 3. Edit your user document — change "role": "user" to "role": "admin"
# 4. Click "Update"

# Option 2: Use mongosh (terminal)
# mongosh "YOUR_MONGODB_URI"
# db.users.updateOne({ email: "your@email.com" }, { $set: { role: "admin" } })
```

After making yourself an admin:
- Log out and log back in (so the JWT token refreshes with the admin role)
- You should see "Admin" appear in the navbar

Now add some products:

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Admin" in the navbar | You see the admin dashboard with "Manage Products" and an empty table |
| 2 | Click "Add Product" | You see the product creation form |
| 3 | Fill in: Name "Wireless Headphones", Description "Great sound", Price "79.99", Category "Electronics", Stock "15", Image URL `https://picsum.photos/seed/headphones/400` | Form is filled |
| 4 | Click "Create Product" | You're redirected to the admin product list — the table now shows your product |
| 5 | Repeat steps 2-4 to add a few more products with different categories (e.g., "Cotton T-Shirt" in "Clothing", "JavaScript Book" in "Books") | Multiple products appear in the table |

### 2.4 Browsing Products

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Products" in the navbar | You see all products you added, displayed in a grid |
| 2 | Type something in the search bar and press Enter | Only matching products appear |
| 3 | Select a category filter | Products are filtered by that category |
| 4 | Set a price range (e.g., Min: 10, Max: 50) and click "Apply Filters" | Only products in that price range appear |
| 5 | Click a product card | You go to the product detail page |

### 2.5 Product Detail & Add to Cart

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | On a product detail page, click "Add to Cart" | Green "Added to cart!" message appears |
| 2 | Click "Cart" in the navbar | You see the cart with your item, quantity controls, and price |
| 3 | Click "+" to increase quantity | Quantity and subtotal update |
| 4 | Click "−" to decrease (but not below 1) | Quantity decreases |
| 5 | Go back to products and add another product to cart | Both items appear in the cart |

### 2.6 Placing an Order

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Go to your cart | You see both items |
| 2 | Click "Place Order" | You're redirected to the order detail page |
| 3 | See the order details | Shows status "Pending", all items, and total |
| 4 | Click "Orders" in the navbar | You see the order in your order history |

### 2.7 Order History

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Orders" in the navbar | You see all past orders as cards |
| 2 | Click an order card | You see the full order details |

---

## 3. API Test Steps

Test each API endpoint directly using `curl`, Postman, or the browser console.

### 3.1 Auth Endpoints

#### Register

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}'
```

Expected response (201):
```json
{
  "data": { "_id": "...", "name": "Test User", "email": "test@example.com", "role": "user" },
  "token": "eyJ..."
}
```

#### Login

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

Expected response (200):
```json
{
  "data": { "_id": "...", "name": "Test User", "email": "test@example.com", "role": "user" },
  "token": "eyJ..."
}
```

#### Get Me

```bash
# Replace TOKEN with the token from login/register
curl http://localhost:3000/api/auth/me \
  -H "Authorization: Bearer TOKEN"
```

Expected response (200):
```json
{
  "data": { "_id": "...", "name": "Test User", "email": "test@example.com", "role": "user", "createdAt": "..." }
}
```

### 3.2 Products Endpoints

#### List Products

```bash
curl http://localhost:3000/api/products
```

Expected response (200):
```json
{
  "data": [ ... ],
  "page": 1,
  "totalPages": 1,
  "totalItems": 3
}
```

Try with query params:
```bash
curl "http://localhost:3000/api/products?search=headphones"
curl "http://localhost:3000/api/products?category=Electronics"
curl "http://localhost:3000/api/products?minPrice=10&maxPrice=50"
curl "http://localhost:3000/api/products?page=1&limit=2"
```

#### Get Single Product

```bash
# Replace ID with a product _id from the list
curl http://localhost:3000/api/products/ID
```

Expected response (200):
```json
{
  "data": { "_id": "...", "name": "Wireless Headphones", ... }
}
```

#### Create Product (Admin only)

```bash
# Replace TOKEN with an admin JWT token
curl -X POST http://localhost:3000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"New Product","description":"Test","price":29.99,"category":"Electronics","imageUrl":"https://picsum.photos/seed/test/400","stock":10}'
```

#### Update Product (Admin only)

```bash
curl -X PUT http://localhost:3000/api/products/ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"price": 24.99}'
```

#### Delete Product (Admin only)

```bash
curl -X DELETE http://localhost:3000/api/products/ID \
  -H "Authorization: Bearer TOKEN"
```

### 3.3 Cart Endpoints

All cart endpoints require authentication.

#### Get Cart

```bash
curl http://localhost:3000/api/cart \
  -H "Authorization: Bearer TOKEN"
```

#### Add Item

```bash
# Replace PRODUCT_ID with an actual product _id
curl -X POST http://localhost:3000/api/cart \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"productId":"PRODUCT_ID","name":"Wireless Headphones","price":79.99,"quantity":1}'
```

#### Update Quantity

```bash
curl -X PUT http://localhost:3000/api/cart \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"productId":"PRODUCT_ID","quantity":3}'
```

#### Remove Item

```bash
curl -X DELETE "http://localhost:3000/api/cart/items/PRODUCT_ID" \
  -H "Authorization: Bearer TOKEN"
```

### 3.4 Orders Endpoints

All order endpoints require authentication.

#### Place Order

```bash
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN"
```

#### List Orders

```bash
curl http://localhost:3000/api/orders \
  -H "Authorization: Bearer TOKEN"
```

#### Get Single Order

```bash
curl http://localhost:3000/api/orders/ORDER_ID \
  -H "Authorization: Bearer TOKEN"
```

---

## 4. UI Test Steps

### 4.1 Responsive Design

| Test | Expected |
|------|----------|
| Resize browser to mobile width (320px) | Navbar collapses, product grid becomes 1 column, all pages remain usable |
| Open the app on a tablet (768px) | Product grid shows 2 columns, layout adjusts |
| Open on desktop (1280px+) | Full layout with 4-column product grid, sidebar filters visible |

### 4.2 Navigation

| Test | Expected |
|------|----------|
| Click each navbar link | Every link goes to the correct page |
| Click "ShopNext" logo | Always goes to home page |
| Use browser back/forward buttons | Navigation works correctly |
| Refresh any page | Content loads correctly (no 404s) |

### 4.3 Authentication UI

| Test | Expected |
|------|----------|
| Visit /cart while logged out | Redirected to /auth/login |
| Visit /orders while logged out | Redirected to /auth/login |
| Visit /profile while logged out | Redirected to /auth/login |
| Visit /admin/products while logged out | Redirected to /auth/login |
| Log in, then visit protected pages | Content shows correctly |

### 4.4 Error States

| Test | Expected |
|------|----------|
| Visit `/products/invalid-id` | Product detail shows "Product Not Found" |
| Visit `/orders/invalid-id` | Order detail shows "Order Not Found" |
| Visit a non-existent route like `/xyz` | Next.js shows a 404 page |
| Try to place order with empty cart | Should not be possible (button is disabled) |

---

## 5. AI Test Steps

> **Note:** This project does not include AI features (per the proposal).  
> This section is intentionally left blank.  
> If AI features are added in the future, add test cases here for:
> - Semantic search results
> - Product recommendation accuracy
> - Chat assistant responses

---

## 6. Automated Testing (Optional — For Students Who Want More)

If you want to go further, here's how to set up automated tests with Jest.

### Setup

```bash
npm install -D jest @types/jest @testing-library/react @testing-library/jest-dom
```

Add to `package.json`:
```json
"scripts": {
  "test": "jest",
  "test:watch": "jest --watch"
}
```

### Sample Test File

Create `__tests__/auth.test.ts`:

```typescript
import { signToken, verifyToken } from "@/lib/auth";

describe("Auth utilities", () => {
  it("should sign and verify a valid token", () => {
    const payload = { userId: "123", email: "test@test.com", role: "user" as const };
    const token = signToken(payload);
    const decoded = verifyToken(token);
    expect(decoded?.email).toBe("test@test.com");
  });

  it("should return null for an invalid token", () => {
    const result = verifyToken("invalid-token");
    expect(result).toBeNull();
  });
});
```

### API Route Testing

For testing API routes, use `node-mocks-http` or Supertest.  
Example with Supertest:

```bash
npm install -D supertest @types/supertest
```

```typescript
import { GET } from "@/app/api/products/route";
import { NextRequest } from "next/server";

// This requires mocking the database connection
// For a simpler approach, test via curl or Postman (see section 3)
```

### What to Test

| Area | What to Test |
|------|-------------|
| Auth | Token creation, verification, invalid token rejection |
| Products | CRUD operations, validation, admin-only access |
| Cart | Add/update/remove items, quantity limits |
| Orders | Place order, empty cart rejection, order ownership |
| API | Response format, error messages, status codes |

---

## 7. Troubleshooting Common Test Issues

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| API returns 500 | MongoDB not connected | Check `MONGODB_URI` in `.env.local` |
| Auth endpoints return 500 | Missing `JWT_SECRET` | Add `JWT_SECRET` to `.env.local` |
| "Cannot find module" | Dependencies not installed | Run `npm install` |
| Empty product list | No products in MongoDB | Add products via admin UI or API |
| Cart returns empty | Not authenticated | Include valid `Bearer` token |
| Order placement fails | Cart is empty | Add items to cart first |
| Admin features don't work | User role is "user" | Change role to "admin" in MongoDB |
