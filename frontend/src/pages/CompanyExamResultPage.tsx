import {
  ArrowLeft,
  CheckCircle2,
  CircleAlert,
  Sparkles,
  XCircle,
} from "lucide-react";
import { Link, useParams } from "react-router-dom";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import { companyPrepService } from "../services/companyPrepService";

const CompanyExamResultPage = () => {
  const { companySlug } = useParams();
  const exam = companyPrepService.getActiveExam();
  const result = companyPrepService.getResult();

  if (!exam || !result || exam.examId !== result.examId || !companySlug) {
    return (
      <main className="assessment-missing">
        <h1>No company exam result found</h1>
        <Link to="/company-prep" className="primary-button">
          Return to Companies
        </Link>
      </main>
    );
  }

  return (
    <>
      <Navbar />
      <main className="result-page">
        <div className="container result-container">
          <Link to="/company-prep" className="company-back-link">
            <ArrowLeft size={17} />
            All Companies
          </Link>

          <section className="result-hero">
            <div>
              <span>INTERVIEW PRACTICE COMPLETE</span>
              <h1>{exam.company.name}</h1>
              <p>Review your score, feedback and suggested answers.</p>
              <div className="result-source">Groq semantic evaluation</div>
            </div>
            <div className={result.score >= 60 ? "result-score passed" : "result-score failed"}>
              <strong>{result.score}%</strong>
              <span>{result.score >= 60 ? "GOOD PROGRESS" : "KEEP PRACTICING"}</span>
            </div>
          </section>

          <div className="result-stats-grid">
            <div><span>Score</span><strong>{result.score}%</strong></div>
            <div><span>Strong</span><strong>{result.correctCount}</strong></div>
            <div><span>Partial</span><strong>{result.partialCount}</strong></div>
            <div><span>Total</span><strong>{result.totalQuestions}</strong></div>
          </div>

          <section className="answer-review-section">
            <div className="result-section-heading">
              <Sparkles size={18} />
              <div><span>ANSWER REVIEW</span><h2>Detailed evaluation</h2></div>
            </div>
            <div className="answer-review-list">
              {result.items.map((item, index) => {
                const strong = item.status === "correct";
                const partial = item.status === "partially_correct";
                return (
                  <article
                    className={strong ? "answer-review-card correct" : "answer-review-card incorrect"}
                    key={item.questionId}
                  >
                    <div className="answer-review-top">
                      <span>Question {index + 1} · {item.score}/10</span>
                      <div className={strong ? "answer-status correct" : "answer-status incorrect"}>
                        {strong ? <CheckCircle2 size={14} /> : partial ? <CircleAlert size={14} /> : <XCircle size={14} />}
                        {strong ? "Correct" : partial ? "Partially correct" : "Incorrect"}
                      </div>
                    </div>
                    <h3>{item.question}</h3>
                    <div className="answer-detail">
                      <span>Your Answer</span>
                      <p>{item.userAnswer || "No answer provided"}</p>
                    </div>
                    <div className="answer-detail correct-answer">
                      <span>{item.referenceAnswer ? "Reference Answer" : "Suggested Answer"}</span>
                      <p>{item.referenceAnswer || item.suggestedAnswer}</p>
                    </div>
                    <div className="answer-explanation">
                      <strong>Feedback</strong>
                      <p>{item.feedback}</p>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>

          <div className="result-actions">
            <Link to="/company-prep" className="primary-button">Return to Companies</Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
};

export default CompanyExamResultPage;
