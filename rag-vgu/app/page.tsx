"use client";

import { useState } from "react";
import { login, signup } from "./lib/api";

export default function LoginPage() {
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [user, setUser] = useState<{ user_id: string; username: string } | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result =
        mode === "login" ? await login(username, password) : await signup(username, password);
      setUser(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  if (user) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center gap-4 bg-zinc-50 font-sans dark:bg-black">
        <div className="w-full max-w-sm rounded-2xl border border-black/10 bg-white p-8 text-center shadow-sm dark:border-white/10 dark:bg-zinc-900">
          <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-50">
            Welcome, {user.username}
          </h1>
          <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
            User ID: {user.user_id}
          </p>
          <button
            onClick={() => setUser(null)}
            className="mt-6 rounded-full bg-zinc-900 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-zinc-700 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-300"
          >
            Log out
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="w-full max-w-sm rounded-2xl border border-black/10 bg-white p-8 shadow-sm dark:border-white/10 dark:bg-zinc-900">
        <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-50">
          {mode === "login" ? "Sign in" : "Create account"}
        </h1>
        <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
          {mode === "login"
            ? "Welcome back, please enter your details."
            : "Create an account to get started."}
        </p>

        <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-4">
          <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Username
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="your_username"
              className="rounded-lg border border-black/10 bg-transparent px-3 py-2 text-sm text-zinc-900 outline-none transition-colors placeholder:text-zinc-400 focus:border-zinc-900 dark:border-white/10 dark:text-zinc-50 dark:focus:border-zinc-50"
            />
          </label>

          <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Password
            <input
              type="password"
              required
              maxLength={72}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="rounded-lg border border-black/10 bg-transparent px-3 py-2 text-sm text-zinc-900 outline-none transition-colors placeholder:text-zinc-400 focus:border-zinc-900 dark:border-white/10 dark:text-zinc-50 dark:focus:border-zinc-50"
            />
          </label>

          {error && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600 dark:bg-red-950 dark:text-red-400">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-2 rounded-full bg-zinc-900 py-2.5 text-sm font-medium text-white transition-colors hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-300"
          >
            {loading ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}
          </button>
        </form>

        <button
          onClick={() => {
            setMode(mode === "login" ? "signup" : "login");
            setError("");
          }}
          className="mt-4 w-full text-center text-sm text-zinc-500 underline-offset-4 hover:underline dark:text-zinc-400"
        >
          {mode === "login" ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
        </button>
      </div>
    </div>
  );
}