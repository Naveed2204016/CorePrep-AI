import type {
  AuthResponse,
  LoginData,
  RegisterData,
} from "../types/auth";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000/api/v1";

const USE_MOCK_AUTH =
  import.meta.env.VITE_USE_MOCK_AUTH !== "false";

const delay = (ms: number) =>
  new Promise((resolve) => setTimeout(resolve, ms));

export const authService = {
  async login(data: LoginData): Promise<AuthResponse> {
    if (USE_MOCK_AUTH) {
      await delay(700);

      return {
        message: "Mock login successful",
        user: {
          id: 1,
          name: "CorePrep User",
          email: data.email,
        },
      };
    }

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Login failed");
    }

    return response.json();
  },

  async register(data: RegisterData): Promise<AuthResponse> {
    if (USE_MOCK_AUTH) {
      await delay(700);

      return {
        message: "Mock registration successful",
        user: {
          id: 1,
          name: data.name,
          email: data.email,
        },
      };
    }

    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Registration failed");
    }

    return response.json();
  },

  async continueWithGoogle(): Promise<void> {
    if (USE_MOCK_AUTH) {
      alert(
        "Google authentication UI is ready. FastAPI Google OAuth will be connected later."
      );

      return;
    }

    window.location.href = `${API_BASE_URL}/auth/google`;
  },
};