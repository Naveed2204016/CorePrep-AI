import type {
  CompanyExam,
  CompanyExamMode,
  CompanyExamResult,
} from "../types/companyPrep";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000/api/v1";

const ACTIVE_EXAM_KEY = "coreprep_company_exam";
const EXAM_RESULT_KEY = "coreprep_company_exam_result";

const errorMessage = async (response: Response) => {
  try {
    const body = await response.json();
    return body.detail || "Could not start the company exam.";
  } catch {
    return "Could not start the company exam.";
  }
};

export const companyPrepService = {
  async createExam(
    companySlug: string,
    mode: CompanyExamMode,
  ): Promise<CompanyExam> {
    const token = localStorage.getItem("coreprep_token");
    if (!token) {
      throw new Error("Your session has expired. Please sign in again.");
    }

    const response = await fetch(
      `${API_BASE_URL}/company-prep/companies/${companySlug}/exams`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ mode }),
      },
    );

    if (!response.ok) {
      throw new Error(await errorMessage(response));
    }

    const exam = (await response.json()) as CompanyExam;
    sessionStorage.setItem(ACTIVE_EXAM_KEY, JSON.stringify(exam));
    sessionStorage.removeItem(`coreprep_company_exam_answers_${companySlug}`);
    return exam;
  },

  getActiveExam(): CompanyExam | null {
    try {
      const stored = sessionStorage.getItem(ACTIVE_EXAM_KEY);
      return stored ? (JSON.parse(stored) as CompanyExam) : null;
    } catch {
      return null;
    }
  },

  async submitExam(
    examId: number,
    answers: Record<string, string>,
  ): Promise<CompanyExamResult> {
    const token = localStorage.getItem("coreprep_token");
    if (!token) {
      throw new Error("Your session has expired. Please sign in again.");
    }
    const response = await fetch(
      `${API_BASE_URL}/company-prep/exams/${examId}/submit`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          answers: Object.entries(answers).map(([questionId, answer]) => ({
            question_id: Number(questionId),
            answer,
          })),
        }),
      },
    );
    if (!response.ok) {
      throw new Error(await errorMessage(response));
    }
    const result = (await response.json()) as CompanyExamResult;
    sessionStorage.setItem(EXAM_RESULT_KEY, JSON.stringify(result));
    return result;
  },

  getResult(): CompanyExamResult | null {
    try {
      const stored = sessionStorage.getItem(EXAM_RESULT_KEY);
      return stored ? (JSON.parse(stored) as CompanyExamResult) : null;
    } catch {
      return null;
    }
  },
};
