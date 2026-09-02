import { useEffect, useState } from "react";
import { AlertCircle, ArrowLeft, Building2, CheckCircle2, LoaderCircle, Send } from "lucide-react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { companyPrepService } from "../services/companyPrepService";

const CompanyExamPage = () => {
  const { companySlug } = useParams();
  const navigate = useNavigate();
  const exam = companyPrepService.getActiveExam();
  const answerKey = `coreprep_company_exam_answers_${companySlug ?? "unknown"}`;
  const [answers, setAnswers] = useState<Record<string, string>>(() => {
    try {
      const stored = sessionStorage.getItem(answerKey);
      return stored ? JSON.parse(stored) : {};
    } catch {
      return {};
    }
  });
  const [evaluating, setEvaluating] = useState(false);
  const [submitError, setSubmitError] = useState("");

  useEffect(() => {
    sessionStorage.setItem(answerKey, JSON.stringify(answers));
  }, [answerKey, answers]);

  if (!exam || !companySlug || exam.company.slug !== companySlug) {
    return (
      <main className="assessment-missing">
        <h1>No active company exam found</h1>
        <p>Choose a company and an exam size before opening this page.</p>
        <Link to="/company-prep" className="primary-button">
          Return to Companies
        </Link>
      </main>
    );
  }

  const answeredCount = exam.questions.filter(
    (question) => answers[question.id]?.trim(),
  ).length;

  const submitExam = async () => {
    setEvaluating(true);
    setSubmitError("");
    try {
      await companyPrepService.submitExam(exam.examId, answers);
      navigate(`/company-prep/${companySlug}/result`);
    } catch (cause) {
      setSubmitError(
        cause instanceof Error ? cause.message : "Could not evaluate the exam.",
      );
      setEvaluating(false);
    }
  };

  if (evaluating) {
    return (
      <main className="assessment-evaluation-loading">
        <LoaderCircle size={42} />
        <span>AI EVALUATION IN PROGRESS</span>
        <h1>Evaluating your answers</h1>
        <p>This can take up to three minutes. Please keep this page open.</p>
      </main>
    );
  }

  return (
    <main className="exam-page">
      <header className="exam-header">
        <div>
          <span>COMPANY PREPARATION</span>
          <strong>{exam.company.name}</strong>
        </div>
        <div className="exam-timer">
          <Building2 size={17} />
          {answeredCount}/{exam.questionCount}
        </div>
      </header>

      <div className="container exam-container">
        <Link
          to="/company-prep"
          className="company-back-link"
        >
          <ArrowLeft size={17} />
          All Companies
        </Link>

        <div className="exam-info-banner company-exam-banner">
          <CheckCircle2 size={17} />
          <p>
            Your tailored interview practice set is ready. Written answers are
            saved in this browser while this tab is open.
          </p>
        </div>

        <div className="exam-question-list">
          {exam.questions.map((question, index) => (
            <section key={question.id} className="exam-question-card">
              <div className="exam-question-number">
                Question {index + 1}
              </div>
              <h2 className="company-question-text">{question.question}</h2>
              <textarea
                className="exam-short-answer"
                placeholder="Write your practice answer here..."
                value={answers[question.id] ?? ""}
                onChange={(event) =>
                  setAnswers((previous) => ({
                    ...previous,
                    [question.id]: event.target.value,
                  }))
                }
              />
            </section>
          ))}
        </div>

        {submitError && (
          <div className="exam-info-banner company-exam-error">
            <AlertCircle size={17} />
            <p>{submitError}</p>
          </div>
        )}

        <div className="exam-submit-area">
          <div>
            <span>{answeredCount}/{exam.questionCount} answered</span>
            <p>Submit when ready to receive AI feedback and suggested answers.</p>
          </div>
          <button className="primary-button" onClick={submitExam}>
            <Send size={17} />
            Submit for Evaluation
          </button>
        </div>
      </div>
    </main>
  );
};

export default CompanyExamPage;
