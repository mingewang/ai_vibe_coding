// ============================================================
// Footer — simple footer shown on every page
// ============================================================

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-gray-50 border-t border-gray-200 mt-12">
      <div className="max-w-7xl mx-auto px-4 py-8 text-center text-gray-500 text-sm">
        <p>&copy; {year} ShopNext. Built with Next.js &amp; MongoDB.</p>
      </div>
    </footer>
  );
}
