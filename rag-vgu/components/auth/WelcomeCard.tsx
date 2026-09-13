"use client";

import Link from "next/link";
import type { User } from "@/app/lib/api";
import AuthCard from "./AuthCard";

type WelcomeCardProps = {
  user: User;
  onLogout: () => void;
};

export default function WelcomeCard({ user, onLogout }: WelcomeCardProps) {
  return (
    <AuthCard title={`Welcome, ${user.username}`} subtitle={`User ID: ${user.user_id}`}>
      <div className="flex flex-col gap-2">
        <Link
          href="/chat"
          className="rounded-full bg-indigo-600 px-6 py-2.5 text-center text-sm font-medium text-white transition-colors hover:bg-indigo-500"
        >
          Chat with your documents
        </Link>
        <button
          onClick={onLogout}
          className="w-full rounded-full bg-zinc-900 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-zinc-700 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-300"
        >
          Log out
        </button>
      </div>
    </AuthCard>
  );
}