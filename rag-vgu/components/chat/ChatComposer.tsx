"use client";

import { useState } from "react";

type ChatComposerProps = {
  disabled: boolean;
  onSend: (question: string) => void;
};

export default function ChatComposer({ disabled, onSend }: ChatComposerProps) {
  const [question, setQuestion] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    onSend(question.trim());
    setQuestion("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex gap-2 rounded-2xl border border-black/10 bg-white p-3 dark:border-white/10 dark:bg-zinc-900"
    >
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about your documents…"
        disabled={disabled}
        className="flex-1 rounded-lg border border-black/10 bg-transparent px-3 py-2 text-sm text-zinc-900 outline-none transition-colors placeholder:text-zinc-400 focus:border-zinc-900 disabled:opacity-50 dark:border-white/10 dark:text-zinc-50 dark:focus:border-zinc-50"
      />
      <button
        type="submit"
        disabled={disabled || !question.trim()}
        className="rounded-full bg-indigo-600 px-6 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Send
      </button>
    </form>
  );
}