"use client";

import { useState } from "react";
import AuthCard from "./AuthCard";

type AuthFormProps = {
  mode: "login" | "signup";
  loading: boolean;
  error: string;
  onSubmit: (username: string, password: string) => void;
  onToggleMode: () => void;
};

const inputClass =
  "rounded-lg border border-black/10 bg-transparent px-3 py-2 text-sm text-zinc-900 outline-none transition-colors placeholder:text-zinc-400 focus:border-zinc-900 dark:border-white/10 dark:text-zinc-50 dark:focus:border-zinc-50";

export default function AuthForm({
  mode,
  loading,
  error,
  onSubmit,
  onToggleMode,
}: AuthFormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const isLogin = mode === "login";

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit(username, password);
  }

  return (
    <AuthCard
      title={isLogin ? "Sign in" : "Create account"}
      subtitle={
        isLogin
          ? "Welcome back, please enter your details."
          : "Create an account to get started."
      }
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
          Username
          <input
            type="text"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="your_username"
            className={inputClass}
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
            className={inputClass}
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
          {loading ? "Please wait…" : isLogin ? "Sign in" : "Create account"}
        </button>
      </form>

      <button
        onClick={onToggleMode}
        className="mt-4 w-full text-center text-sm text-zinc-500 underline-offset-4 hover:underline dark:text-zinc-400"
      >
        {isLogin
          ? "Don't have an account? Sign up"
          : "Already have an account? Sign in"}
      </button>
    </AuthCard>
  );
}