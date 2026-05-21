// ============================================================
// AdminProductTable — table for admin to manage products
// ============================================================
// Shows all products with columns for name, price, stock, category.
// Each row has Edit and Delete buttons.
// ============================================================

import { IProduct } from "@/types";

interface AdminProductTableProps {
  products: IProduct[];
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  deleting: string | null;
}

export default function AdminProductTable({
  products,
  onEdit,
  onDelete,
  deleting,
}: AdminProductTableProps) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b border-gray-200 text-left">
            <th className="pb-3 font-semibold text-gray-700">Name</th>
            <th className="pb-3 font-semibold text-gray-700">Category</th>
            <th className="pb-3 font-semibold text-gray-700">Price</th>
            <th className="pb-3 font-semibold text-gray-700">Stock</th>
            <th className="pb-3 font-semibold text-gray-700">Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product._id} className="border-b border-gray-100">
              <td className="py-3 text-gray-900">{product.name}</td>
              <td className="py-3 text-gray-600">{product.category}</td>
              <td className="py-3 text-gray-900">
                ${product.price.toFixed(2)}
              </td>
              <td className="py-3">
                <span
                  className={`${
                    product.stock === 0
                      ? "text-red-500"
                      : product.stock <= 5
                      ? "text-orange-500"
                      : "text-gray-900"
                  }`}
                >
                  {product.stock}
                </span>
              </td>
              <td className="py-3 flex gap-2">
                <button
                  onClick={() => onEdit(product._id)}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Edit
                </button>
                <button
                  onClick={() => onDelete(product._id)}
                  disabled={deleting === product._id}
                  className="text-red-600 hover:text-red-800 text-sm font-medium disabled:opacity-50"
                >
                  {deleting === product._id ? "..." : "Delete"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {products.length === 0 && (
        <p className="text-center text-gray-500 py-8">
          No products yet. Click "Add Product" to create one.
        </p>
      )}
    </div>
  );
}
