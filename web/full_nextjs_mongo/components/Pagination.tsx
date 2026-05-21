// ============================================================
// Pagination — page navigation buttons
// ============================================================
// Props:
//   currentPage: the active page number
//   totalPages: total number of pages
//   onPageChange: callback when user clicks a page
// ============================================================

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export default function Pagination({
  currentPage,
  totalPages,
  onPageChange,
}: PaginationProps) {
  if (totalPages <= 1) return null;

  // Generate page numbers to display (show first, last, and around current)
  const pages: number[] = [];
  for (let i = 1; i <= totalPages; i++) {
    if (
      i === 1 ||
      i === totalPages ||
      (i >= currentPage - 1 && i <= currentPage + 1)
    ) {
      pages.push(i);
    } else if (pages[pages.length - 1] !== -1) {
      pages.push(-1); // -1 represents an ellipsis
    }
  }

  return (
    <div className="flex justify-center items-center gap-2 mt-8">
      {/* Previous Button */}
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage <= 1}
        className="px-4 py-2 border rounded-lg disabled:opacity-50 hover:bg-gray-50"
      >
        Prev
      </button>

      {/* Page Numbers */}
      {pages.map((page, idx) =>
        page === -1 ? (
          <span key={`ellipsis-${idx}`} className="px-2 text-gray-400">
            ...
          </span>
        ) : (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={`px-4 py-2 border rounded-lg ${
              page === currentPage
                ? "bg-primary-600 text-white border-primary-600"
                : "hover:bg-gray-50"
            }`}
          >
            {page}
          </button>
        )
      )}

      {/* Next Button */}
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage >= totalPages}
        className="px-4 py-2 border rounded-lg disabled:opacity-50 hover:bg-gray-50"
      >
        Next
      </button>
    </div>
  );
}
