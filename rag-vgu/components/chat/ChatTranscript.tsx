"use client";

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

type ChatTranscriptProps = {
  messages: ChatMessage[];
  loading: boolean;
  error: string;
};

export default function ChatTranscript({
  messages,
  loading,
  error,
}: ChatTranscriptProps) {
  return (
    <div className="flex max-h-[60vh] flex-col gap-4 overflow-y-auto rounded-2xl border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-zinc-900">
      {messages.length === 0 && (
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400">
          Ask a question about your documents to get started.
        </p>
      )}

      {messages.map((message, index) => (
        <div
          key={index}
          className={
            message.role === "user"
              ? "self-end max-w-[80%] rounded-2xl rounded-br-sm bg-indigo-600 px-4 py-2 text-sm text-white"
              : "self-start max-w-[80%] rounded-2xl rounded-bl-sm bg-zinc-100 px-4 py-2 text-sm whitespace-pre-wrap text-zinc-800 dark:bg-zinc-800 dark:text-zinc-100"
          }
        >
          {message.content}
        </div>
      ))}

      {loading && (
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400">
          Thinking…
        </p>
      )}

      {error && (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600 dark:bg-red-950 dark:text-red-400">
          {error}
        </p>
      )}
    </div>
  );
}