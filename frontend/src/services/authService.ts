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

const saveCurrentUser = (user: AuthResponse["user"]) => {
  localStorage.setItem("coreprep_user", JSON.stringify(user));
  window.dispatchEvent(new Event("coreprep-auth-change"));
};

const saveRegisteredUser = (user: AuthResponse["user"]) => {
  localStorage.setItem("coreprep_registered_user", JSON.stringify(user));
};

const savePassword = (password: string) => {
  localStorage.setItem("coreprep_password", password);
};

export const authService = {
  async login(data: LoginData): Promise<AuthResponse> {
    if (USE_MOCK_AUTH) {
      await delay(700);

      const response = {
        message: "Mock login successful",
        user: {
          id: 1,
          name:
            JSON.parse(
              localStorage.getItem("coreprep_registered_user") || "null"
            )?.email === data.email
              ? JSON.parse(
                  localStorage.getItem("coreprep_registered_user") || "null"
                )?.name
              : "CorePrep User",
          email: data.email,
        },
      };

      saveCurrentUser(response.user);
      return response;
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

    const result = await response.json();
    saveCurrentUser(result.user);
    return result;
  },

  async register(data: RegisterData): Promise<AuthResponse> {
    if (USE_MOCK_AUTH) {
      await delay(700);

      const response = {
        message: "Mock registration successful",
        user: {
          id: 1,
          name: data.name,
          email: data.email,
        },
      };

      saveRegisteredUser(response.user);
      savePassword(data.password);
      saveCurrentUser(response.user);
      return response;
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

    const result = await response.json();
    saveCurrentUser(result.user);
    return result;
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

  getCurrentUser(): AuthResponse["user"] | null {
    const stored = localStorage.getItem("coreprep_user");

    return stored ? JSON.parse(stored) : null;
  },

  signOut() {
    localStorage.removeItem("coreprep_user");
    window.dispatchEvent(new Event("coreprep-auth-change"));
  },

  updatePassword(password: string) {
    savePassword(password);
  },
};