// ============================================================
// EmptyState — a friendly message when there's no data to show
// ============================================================
// Props:
//   title: main heading (e.g. "Your cart is empty")
//   description: helpful subtext
//   actionText: optional button label
//   actionHref: where the button goes
// ============================================================

import Link from "next/link";

interface EmptyStateProps {
  title: string;
  description: string;
  actionText?: string;
  actionHref?: string;
}

export default function EmptyState({
  title,
  description,
  actionText,
  actionHref,
}: EmptyStateProps) {
  return (
    <div className="text-center py-16">
      <h2 className="text-2xl font-semibold text-gray-700 mb-2">{title}</h2>
      <p className="text-gray-500 mb-6">{description}</p>
      {actionText && actionHref && (
        <Link
          href={actionHref}
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700"
        >
          {actionText}
        </Link>
      )}
    </div>
  );
}
