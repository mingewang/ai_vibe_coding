// ============================================================
// FilterSidebar — category and price range filters
// ============================================================
// Props:
//   categories: list of available categories to show
//   selectedCategory: currently selected category
//   minPrice / maxPrice: current price filter values
//   onCategoryChange, onMinPriceChange, onMaxPriceChange: callbacks
// ============================================================

interface FilterSidebarProps {
  categories: string[];
  selectedCategory: string;
  minPrice: string;
  maxPrice: string;
  onCategoryChange: (category: string) => void;
  onMinPriceChange: (value: string) => void;
  onMaxPriceChange: (value: string) => void;
  onApply: () => void;
}

export default function FilterSidebar({
  categories,
  selectedCategory,
  minPrice,
  maxPrice,
  onCategoryChange,
  onMinPriceChange,
  onMaxPriceChange,
  onApply,
}: FilterSidebarProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 space-y-6">
      {/* Category Filter */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Category</h3>
        <div className="space-y-2">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="category"
              checked={selectedCategory === ""}
              onChange={() => onCategoryChange("")}
              className="text-primary-600"
            />
            <span className="text-gray-700">All</span>
          </label>
          {categories.map((cat) => (
            <label key={cat} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="category"
                checked={selectedCategory === cat}
                onChange={() => onCategoryChange(cat)}
                className="text-primary-600"
              />
              <span className="text-gray-700">{cat}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Price Range */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Price Range</h3>
        <div className="flex gap-2 items-center">
          <input
            type="number"
            placeholder="Min"
            value={minPrice}
            onChange={(e) => onMinPriceChange(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
          />
          <span className="text-gray-400">—</span>
          <input
            type="number"
            placeholder="Max"
            value={maxPrice}
            onChange={(e) => onMaxPriceChange(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
          />
        </div>
      </div>

      {/* Apply Button */}
      <button
        onClick={onApply}
        className="w-full bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700"
      >
        Apply Filters
      </button>
    </div>
  );
}
