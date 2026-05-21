"use client";

// ============================================================
// ProductListPage (/products) — browse all products with search & filters
// ============================================================
// This is a Client Component that manages search, filter, and
// pagination state in the URL search params.
// ============================================================

import { useState, useEffect, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { IProduct, IPaginatedResponse } from "@/types";
import SearchBar from "@/components/SearchBar";
import FilterSidebar from "@/components/FilterSidebar";
import ProductGrid from "@/components/ProductGrid";
import Pagination from "@/components/Pagination";
import LoadingSpinner from "@/components/LoadingSpinner";

export default function ProductListPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // State from URL params
  const [search, setSearch] = useState(searchParams.get("search") || "");
  const [category, setCategory] = useState(searchParams.get("category") || "");
  const [minPrice, setMinPrice] = useState(searchParams.get("minPrice") || "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get("maxPrice") || "");
  const [page, setPage] = useState(parseInt(searchParams.get("page") || "1", 10));

  // Data state
  const [products, setProducts] = useState<IProduct[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [loading, setLoading] = useState(true);

  // Extract unique categories from all products (could also fetch from API)
  const [categories] = useState([
    "Electronics",
    "Clothing",
    "Books",
    "Home & Garden",
    "Sports",
    "Toys",
  ]);

  // Fetch products whenever filters change
  const fetchProducts = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search) params.set("search", search);
      if (category) params.set("category", category);
      if (minPrice) params.set("minPrice", minPrice);
      if (maxPrice) params.set("maxPrice", maxPrice);
      params.set("page", page.toString());
      params.set("limit", "12");

      const res = await fetch(`/api/products?${params.toString()}`);
      const data: IPaginatedResponse<IProduct> = await res.json();

      if (data.data) {
        setProducts(data.data);
        setTotalPages(data.totalPages);
        setTotalItems(data.totalItems);
      }
    } catch (err) {
      console.error("Failed to fetch products", err);
    } finally {
      setLoading(false);
    }
  }, [search, category, minPrice, maxPrice, page]);

  // Fetch on mount and when filters change
  useEffect(() => {
    fetchProducts();

    // Update URL to reflect current filters (without full page reload)
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (category) params.set("category", category);
    if (minPrice) params.set("minPrice", minPrice);
    if (maxPrice) params.set("maxPrice", maxPrice);
    if (page > 1) params.set("page", page.toString());

    const newUrl = `/products${params.toString() ? `?${params.toString()}` : ""}`;
    router.replace(newUrl, { scroll: false });
  }, [search, category, minPrice, maxPrice, page, fetchProducts, router]);

  // Apply filters (reset to page 1 when filters change)
  const applyFilters = () => {
    setPage(1);
    // fetchProducts will be called by the useEffect
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Products</h1>

      {/* Search Bar */}
      <div className="mb-6">
        <SearchBar
          value={search}
          onChange={setSearch}
          onSubmit={() => {
            setPage(1);
            // useEffect will trigger the fetch
          }}
        />
      </div>

      <div className="flex gap-8">
        {/* Filters Sidebar */}
        <div className="w-64 flex-shrink-0 hidden md:block">
          <FilterSidebar
            categories={categories}
            selectedCategory={category}
            minPrice={minPrice}
            maxPrice={maxPrice}
            onCategoryChange={(cat) => {
              setCategory(cat);
              setPage(1);
            }}
            onMinPriceChange={setMinPrice}
            onMaxPriceChange={setMaxPrice}
            onApply={applyFilters}
          />
        </div>

        {/* Product Grid */}
        <div className="flex-1">
          {loading ? (
            <LoadingSpinner />
          ) : (
            <>
              <p className="text-sm text-gray-500 mb-4">
                {totalItems} product{totalItems !== 1 ? "s" : ""} found
              </p>
              <ProductGrid products={products} />
              <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
