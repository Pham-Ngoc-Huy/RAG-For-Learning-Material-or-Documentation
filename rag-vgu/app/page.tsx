"use client";

import { useState } from "react";
import { login, signup } from "./lib/api";
import type { User } from "./lib/api";
import AuthForm from "@/components/auth/AuthForm";
import WelcomeCard from "@/components/auth/WelcomeCard";

type Mode = "login" | "signup";

export default function LoginPage() {
  const [mode, setMode] = useState<Mode>("login");
  const [error, setError] = useState("");
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleAuthenticate(username: string, password: string) {
    setError("");
    setLoading(true);
    try {
      const result =
        mode === "login"
          ? await login(username, password)
          : await signup(username, password);
      setUser(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  function handleToggleMode() {
    setMode(mode === "login" ? "signup" : "login");
    setError("");
  }

  if (user) {
    return <WelcomeCard user={user} onLogout={() => setUser(null)} />;
  }

  return (
    <AuthForm
      mode={mode}
      loading={loading}
      error={error}
      onSubmit={handleAuthenticate}
      onToggleMode={handleToggleMode}
    />
  );
}
