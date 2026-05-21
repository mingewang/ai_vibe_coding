// ============================================================
// HomePage (/) — the landing page of our e-commerce site
// ============================================================
// Shows a hero banner and a grid of featured products.
// ============================================================

import Link from "next/link";
import { connectDB } from "@/lib/db";
import Product from "@/lib/models/Product";
import ProductGrid from "@/components/ProductGrid";

// This is a Server Component — it fetches data directly from MongoDB
export default async function HomePage() {
  await connectDB();

  // Get the 8 most recently added products
  const products = await Product.find()
    .sort({ createdAt: -1 })
    .limit(8)
    .lean();

  // Convert MongoDB documents to plain objects
  const featuredProducts = products.map((p) => ({
    _id: p._id.toString(),
    name: p.name,
    description: p.description,
    price: p.price,
    category: p.category,
    imageUrl: p.imageUrl,
    stock: p.stock,
  }));

  return (
    <div>
      {/* Hero Section */}
      <section className="text-center py-16 bg-gradient-to-br from-primary-50 to-white rounded-2xl mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Welcome to ShopNext
        </h1>
        <p className="text-lg text-gray-600 mb-8 max-w-xl mx-auto">
          Discover amazing products at great prices. Fast shipping and easy
          returns.
        </p>
        <Link
          href="/products"
          className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-primary-700"
        >
          Browse Products
        </Link>
      </section>

      {/* Featured Products */}
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            New Arrivals
          </h2>
          <Link
            href="/products"
            className="text-primary-600 hover:text-primary-800 font-medium"
          >
            View All →
          </Link>
        </div>
        <ProductGrid products={featuredProducts} />
      </section>
    </div>
  );
}
