export type CompanyExamMode = "20" | "40" | "all";

export interface CompanyExamQuestion {
  id: number;
  question: string;
}

export interface CompanyExam {
  examId: number;
  company: {
    name: string;
    slug: string;
    shortName: string;
  };
  mode: CompanyExamMode;
  availableQuestionCount: number;
  questionCount: number;
  questions: CompanyExamQuestion[];
}

export interface CompanyExamResultItem {
  questionId: number;
  question: string;
  userAnswer: string;
  score: number;
  status: "correct" | "partially_correct" | "incorrect";
  feedback: string;
  suggestedAnswer: string;
  referenceAnswer: string | null;
}

export interface CompanyExamResult {
  examId: number;
  attemptId: number;
  score: number;
  correctCount: number;
  partialCount: number;
  totalQuestions: number;
  evaluationSource: "groq";
  items: CompanyExamResultItem[];
}
