// ============================================================
// ProductCard — a single product card for grid display
// ============================================================
// Shows product image, name, price, and category.
// Clicking the card navigates to the product detail page.
// ============================================================

import Link from "next/link";
import { IProduct } from "@/types";

interface ProductCardProps {
  product: IProduct;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <Link
      href={`/products/${product._id}`}
      className="group border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow"
    >
      {/* Product Image */}
      <div className="aspect-square bg-gray-100 overflow-hidden">
        <img
          src={product.imageUrl}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform"
        />
      </div>

      {/* Product Info */}
      <div className="p-4">
        <p className="text-xs text-primary-600 uppercase tracking-wide mb-1">
          {product.category}
        </p>
        <h3 className="font-medium text-gray-900 truncate">{product.name}</h3>
        <p className="text-lg font-bold text-gray-900 mt-1">
          ${product.price.toFixed(2)}
        </p>
        {product.stock <= 5 && product.stock > 0 && (
          <p className="text-xs text-orange-500 mt-1">
            Only {product.stock} left in stock
          </p>
        )}
        {product.stock === 0 && (
          <p className="text-xs text-red-500 mt-1">Out of stock</p>
        )}
      </div>
    </Link>
  );
}
