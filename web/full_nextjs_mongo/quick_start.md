# Quick Start Guide — E-Commerce Shopping Site

Get the app up and running in 5 minutes.

---

## Prerequisites

Before you start, make sure you have:

- **Node.js 18+** — [Download here](https://nodejs.org/)
- **MongoDB Atlas account** (free tier is fine) — [Sign up here](https://www.mongodb.com/atlas)
- **Git** (optional) — for version control

---

## Step 1: Install Dependencies

Open a terminal in the project folder and run:

```bash
npm install
```

This installs all the packages listed in `package.json`:
- `next`, `react`, `react-dom` — the framework
- `mongoose` — MongoDB connection
- `bcryptjs` — password hashing
- `jsonwebtoken` — authentication tokens
- TypeScript types and Tailwind CSS

---

## Step 2: Set Up Environment Variables

Copy the example environment file:

```bash
# On Windows (PowerShell):
copy .env.local.example .env.local

# On Mac / Linux:
# cp .env.local.example .env.local
```

> If `.env.local.example` doesn't exist, just create `.env.local` manually and paste the contents from below.

Now edit `.env.local` and fill in your real values.

### Getting your MongoDB URI

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/) and log in
2. Click "Database" → "Connect" → "Drivers"
3. Copy the connection string — it looks like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/ecommerce
   ```
4. Replace `<username>` with your database username
5. Replace `<password>` with your database password
6. Make sure the database name is `ecommerce` (add it if missing)

### Your `.env.local` should look like:

```bash
MONGODB_URI=mongodb+srv://alice:abc123@cluster0.a1b2c.mongodb.net/ecommerce
JWT_SECRET=your-super-secret-key-change-this-in-production
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

> **Important:** Never commit `.env.local` to Git!  
> It's already in `.gitignore` so you're safe by default.

---

## Step 3: Start the Development Server

```bash
npm run dev
```

You should see output like:

```
▲ Next.js 15.x.x
- Local:        http://localhost:3000
- Environments: .env.local
```

Open **http://localhost:3000** in your browser.

---

## Step 4: Create an Admin Account

Admin access is required to add/edit products. There is no default admin — you must promote yourself.

1. **Register** — Open the app at `http://localhost:3000` and click "Sign Up". Create an account with any email/password.
2. **Promote to admin** — Update your user's role in MongoDB using one of these methods:

   **Option A — Using MongoDB Shell (mongosh):**
   ```bash
   mongosh "YOUR_MONGODB_URI"
   use ecommerce
   db.users.updateOne({ email: "your@email.com" }, { $set: { role: "admin" } })
   ```

   **Option B — Using MongoDB Atlas UI:**
   - Go to [MongoDB Atlas](https://cloud.mongodb.com/) → Browse Collections
   - Select your `ecommerce` database → `users` collection
   - Find your user → edit the `role` field from `"user"` to `"admin"`
   - Click "Update"

   **Option C — Using MongoDB Compass:**
   - Connect with your connection string
   - Go to `ecommerce.users` collection
   - Right-click your user → Edit Document → change `role` to `"admin"`

3. **Log out and log back in** — The navbar will now show the "Admin" link.

---

## Step 5: Verify It Works

You should see:
- The "ShopNext" header with navigation links
- A "Welcome to ShopNext" hero section
- A "New Arrivals" section (empty — no products yet)
- Navbar with: Products, Cart, Login, Sign Up

---

## Common Commands

| Action | Command |
|--------|---------|
| Start dev server | `npm run dev` |
| Build for production | `npm run build` |
| Run production build | `npm start` |
| Check for lint errors | `npm run lint` |

---

## Quick Test Flow

Once the app is running, test it end-to-end:

1. **Register** — Click "Sign Up", create an account
2. **Make yourself admin** — In MongoDB Atlas, change your user's `role` from `"user"` to `"admin"`
3. **Log out and log back in** — So the admin role takes effect
4. **Add products** — Click "Admin" → "Add Product", add 3-4 products
5. **Browse** — Click "Products", search, filter, paginate
6. **Add to cart** — Click a product → "Add to Cart"
7. **Place order** — Go to Cart → "Place Order"
8. **View orders** — Click "Orders" to see order history

---

## Troubleshooting

### "MONGODB_URI is not defined"
→ You forgot to create `.env.local`. Create it and add the MongoDB connection string.

### "MongooseServerSelectionError: connect ECONNREFUSED"
→ Your MongoDB URI is wrong or the cluster isn't accepting connections.  
→ Check: Is your IP address whitelisted in MongoDB Atlas?  
→ Check: Is the username/password correct?  
→ Check: Does the URI end with `/ecommerce`?

### "Invalid email or password" even though you just registered
→ This is correct behavior — the password is hashed, so you can't see it.  
→ Try logging in with the exact same email and password you registered with.

### Admin link doesn't appear in navbar
→ Your user's role is still "user". Change it to "admin" in MongoDB Atlas.

### Page shows "Product Not Found"
→ The product ID in the URL doesn't exist. Go back to the products page and click a valid product.

### "Cannot find module" errors
→ Run `npm install` to install all dependencies.

### Port 3000 is already in use
→ Either close the other process, or run on a different port:
```bash
npx next dev -p 3001
```

### Changes aren't showing up
→ Next.js hot reload should pick up changes. If not:
   - Stop the server (`Ctrl+C`)
   - Delete `.next` folder: `Remove-Item -Recurse -Force .next`
   - Restart: `npm run dev`

---

## Need Help?

- Check the full `test-cases.md` for detailed testing steps
- Check `design.md` for the full architecture explanation
- Ask your instructor if you're stuck
