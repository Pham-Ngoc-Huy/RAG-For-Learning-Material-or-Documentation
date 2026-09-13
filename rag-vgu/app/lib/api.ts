export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export type User = {
  user_id: string;
  username: string;
};

type AuthResponse = User & { detail?: string };

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });

  const data = (await res.json()) as T;

  if (!res.ok) {
    const detail = (data as { detail?: string }).detail ?? "Request failed";
    throw new Error(detail);
  }

  return data;
}

export function login(
  username: string,
  password: string,
): Promise<AuthResponse> {
  return request<AuthResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function signup(
  username: string,
  password: string,
): Promise<AuthResponse> {
  return request<AuthResponse>("/api/auth/signup", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export type ChatSession = {
  user_id: string;
  user_name: string;
  collection_name: string;
  model: string;
};

export type ChatQuestion = ChatSession & { question: string };

export type ChatResponse = {
  user_id: string;
  user_name: string;
  collection_name: string;
  question: string;
  answer: string;
};

export function chatQuestion(question: ChatQuestion): Promise<ChatResponse> {
  return request<ChatResponse>("/api/chat/query", {
    method: "POST",
    body: JSON.stringify(question),
  });
}
