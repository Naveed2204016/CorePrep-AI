export interface CVImprovement {
  priority: "high" | "medium" | "low";
  title: string;
  detail: string;
  rewrite_tip: string;
}

export interface CVReviewResult {
  file_name: string;
  page_count: number;
  score: number;
  summary: string;
  strengths: string[];
  improvements: CVImprovement[];
  missing_sections: string[];
  keywords_found: string[];
}

