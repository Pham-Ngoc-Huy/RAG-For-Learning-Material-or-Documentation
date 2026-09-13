import Link from "next/link";

export default function SiteHeader() {
  return (
    <header className="border-b bg-white px-6 py-4 shadow-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <span className="text-xl font-bold text-indigo-600">Jarvis v.1.0</span>
        <nav className="space-x-4 text-sm font-medium">
          <Link href="/" className="hover:text-indigo-600">
            Home
          </Link>
          <Link href="/chat" className="hover:text-indigo-600">
            Chat
          </Link>
        </nav>
      </div>
    </header>
  );
}
