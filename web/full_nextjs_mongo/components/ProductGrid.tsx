// ============================================================
// ProductGrid — a responsive grid of ProductCard components
// ============================================================
// Props:
//   products: array of product objects to display
// ============================================================

import { IProduct } from "@/types";
import ProductCard from "./ProductCard";

interface ProductGridProps {
  products: IProduct[];
}

export default function ProductGrid({ products }: ProductGridProps) {
  if (products.length === 0) {
    return (
      <p className="text-gray-500 text-center py-12">
        No products found. Try a different search or filter.
      </p>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard key={product._id} product={product} />
      ))}
    </div>
  );
}
