import type { PerformanceSummary } from "../types/profile";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const profileService = {
  async getPerformance(): Promise<PerformanceSummary> {
    const token = localStorage.getItem("coreprep_token");
    if (!token) throw new Error("Please sign in to view your performance.");
    const response = await fetch(`${API_BASE_URL}/profile/performance`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail || "Performance data could not be loaded.");
    }
    return response.json();
  },
};
