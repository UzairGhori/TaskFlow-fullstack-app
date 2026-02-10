const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: { id: string; email: string; name: string };
}

interface AuthResult {
  data?: AuthResponse;
  error?: string;
}

export async function signUp(body: {
  name: string;
  email: string;
  password: string;
}): Promise<AuthResult> {
  try {
    const res = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const err = await res.json();
      return { error: err.detail || "Registration failed" };
    }

    // Auto-login after registration
    return await signIn({ email: body.email, password: body.password });
  } catch {
    return { error: "Network error" };
  }
}

export async function signIn(body: {
  email: string;
  password: string;
}): Promise<AuthResult> {
  try {
    const res = await fetch(`${API_URL}/api/auth/token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const err = await res.json();
      return { error: err.detail || "Invalid email or password" };
    }

    const data: AuthResponse = await res.json();
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    return { data };
  } catch {
    return { error: "Network error" };
  }
}

export function signOut() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export function getUser(): { id: string; email: string; name: string } | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("user");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function isAuthenticated(): boolean {
  return !!getToken();
}
