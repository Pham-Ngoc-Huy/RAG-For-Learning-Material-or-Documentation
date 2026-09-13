export default function SiteFooter() {
  return (
    <footer className="border-t bg-white p-4 text-center text-xs text-slate-500">
      &copy; {new Date().getFullYear()} Jarvis Assistant. All rights reserved.
    </footer>
  );
}