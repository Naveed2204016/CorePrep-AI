import type { CVReviewResult } from "../types/cvReview";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const cvReviewService = {
  async analyze(file: File): Promise<CVReviewResult> {
    const token = localStorage.getItem("coreprep_token");
    if (!token) throw new Error("Please sign in before reviewing your CV.");

    const form = new FormData();
    form.append("file", file);
    const response = await fetch(`${API_BASE_URL}/cv-reviews/analyze`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: form,
    });
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail || "The CV review request failed.");
    }
    return response.json();
  },
};
