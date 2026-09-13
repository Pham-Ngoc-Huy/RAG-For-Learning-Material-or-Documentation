"use client";

import { useState } from "react";
import type { ChatSession } from "@/app/lib/api";
import AuthCard from "@/components/auth/AuthCard";

type ChatSetupCardProps = {
  onStart: (session: ChatSession) => void;
};

const inputClass =
  "rounded-lg border border-black/10 bg-transparent px-3 py-2 text-sm text-zinc-900 outline-none transition-colors placeholder:text-zinc-400 focus:border-zinc-900 dark:border-white/10 dark:text-zinc-50 dark:focus:border-zinc-50";

export default function ChatSetupCard({ onStart }: ChatSetupCardProps) {
  const [user_id, setUserId] = useState("");
  const [user_name, setUserName] = useState("");
  const [collection_name, setCollectionName] = useState("");
  const [model, setModel] = useState("openrouter");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onStart({ user_id, user_name, collection_name, model });
  }

  return (
    <AuthCard
      title="Chat with your documents"
      subtitle="Enter your session details to start a RAG conversation."
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
          User ID
          <input
            type="text"
            required
            value={user_id}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="your user id"
            className={inputClass}
          />
        </label>

        <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
          User name
          <input
            type="text"
            required
            value={user_name}
            onChange={(e) => setUserName(e.target.value)}
            placeholder="your username"
            className={inputClass}
          />
        </label>

        <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
          Collection
          <input
            type="text"
            required
            value={collection_name}
            onChange={(e) => setCollectionName(e.target.value)}
            placeholder="e.g. AI"
            className={inputClass}
          />
        </label>

        <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
          Model
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className={inputClass}
          >
            <option value="openrouter">openrouter</option>
            <option value="openai">openai</option>
          </select>
        </label>

        <button
          type="submit"
          className="mt-2 rounded-full bg-zinc-900 py-2.5 text-sm font-medium text-white transition-colors hover:bg-zinc-700 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-300"
        >
          Start chatting
        </button>
      </form>
    </AuthCard>
  );
}
