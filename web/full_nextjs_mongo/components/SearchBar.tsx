// ============================================================
// SearchBar — search input for filtering products
// ============================================================
// Props:
//   value: current search text
//   onChange: called when the user types
//   onSubmit: called when the user presses Enter or clicks Search
// ============================================================

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

export default function SearchBar({ value, onChange, onSubmit }: SearchBarProps) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      onSubmit();
    }
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        placeholder="Search products..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
      />
      <button
        onClick={onSubmit}
        className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700"
      >
        Search
      </button>
    </div>
  );
}
