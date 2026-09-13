"use client";

import { useState } from "react";
import { chatQuestion } from "@/app/lib/api";
import type { ChatSession } from "@/app/lib/api";
import ChatComposer from "@/components/chat/ChatComposer";
import ChatSetupCard from "@/components/chat/ChatSetupCard";
import ChatTranscript from "@/components/chat/ChatTranscript";
import type { ChatMessage } from "@/components/chat/ChatTranscript";

export default function ChatPage() {
  const [session, setSession] = useState<ChatSession | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSend(question: string) {
    if (!session) return;

    const userMessage: ChatMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setError("");
    setLoading(true);

    try {
      const result = await chatQuestion({ ...session, question });
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: result.answer,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  if (!session) {
    return <ChatSetupCard onStart={(s) => setSession(s)} />;
  }

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-4">
      <div className="flex items-center justify-between rounded-2xl border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-zinc-900">
        <div>
          <p className="text-sm font-medium text-zinc-900 dark:text-zinc-50">
            Collection: {session.collection_name} · model: {session.model}
          </p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400">
            {session.user_name} ({session.user_id})
          </p>
        </div>
        <button
          onClick={() => setSession(null)}
          className="text-sm text-zinc-500 underline-offset-4 hover:underline dark:text-zinc-400"
        >
          Change
        </button>
      </div>

      <ChatTranscript messages={messages} loading={loading} error={error} />

      <ChatComposer disabled={loading} onSend={handleSend} />
    </div>
  );
}