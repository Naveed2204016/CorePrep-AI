import { Link, useParams } from "react-router-dom";

import {
  AlertCircle,
  ArrowLeft,
  CheckCircle2,
  RefreshCw,
  Sparkles,
  XCircle,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

import { roadmapService } from "../services/roadmapService";

import type { ExamResult } from "../types/roadmap";

const AssessmentResultPage = () => {
  const { topicId } = useParams();

  const roadmap =
    roadmapService.getRoadmap();

  const topic = roadmap?.topics.find(
    (item) => String(item.id) === topicId
  );

  const stored =
    sessionStorage.getItem(
      "coreprep_exam_result"
    );

  const result: ExamResult | null =
    stored ? JSON.parse(stored) : null;

  if (!result || !topic) {
    return (
      <>
        <Navbar />

        <main className="assessment-missing">
          <h1>No exam result found</h1>

          <Link
            to="/roadmap/current"
            className="primary-button"
          >
            Return to Roadmap
          </Link>
        </main>
      </>
    );
  }

  return (
    <>
      <Navbar />

      <main className="result-page">
        <div className="container result-container">
          <Link
            to="/roadmap/current"
            className="company-back-link"
          >
            <ArrowLeft size={17} />
            Back to Roadmap
          </Link>

          <section className="result-hero">
            <div>
              <span>
                ASSESSMENT COMPLETE
              </span>

              <h1>{topic.title}</h1>

              <p>
                Review your answers,
                explanations and recommended
                revision areas.
              </p>

              <div className={result.evaluationSource === "fallback" ? "result-source fallback" : "result-source"}>
                {result.evaluationSource === "fallback"
                  ? "Deterministic fallback evaluation"
                  : result.evaluationSource === "groq-rag"
                    ? "Groq + RAG evaluation"
                    : result.evaluationSource === "stored"
                      ? "Previously completed evaluation"
                    : "Evaluation source unavailable"}
              </div>
            </div>

            <div
              className={
                result.passed
                  ? "result-score passed"
                  : "result-score failed"
              }
            >
              <strong>
                {result.score}%
              </strong>

              <span>
                {result.passed
                  ? "PASSED"
                  : "REVISE"}
              </span>
            </div>
          </section>

          <div className="result-stats-grid">
            <div>
              <span>Score</span>
              <strong>
                {result.score}%
              </strong>
            </div>

            <div>
              <span>Correct</span>
              <strong>
                {result.correctCount}
              </strong>
            </div>

            <div>
              <span>Total</span>
              <strong>
                {result.totalQuestions}
              </strong>
            </div>

            <div>
              <span>Status</span>

              <strong>
                {result.passed
                  ? "Completed"
                  : "Revision Needed"}
              </strong>
            </div>
          </div>

          {result.passed ? (
            <div className="result-message success">
              <CheckCircle2 size={20} />

              <div>
                <strong>
                  Topic Completed
                </strong>

                <p>
                  You passed the required
                  assessment. This topic is now
                  marked as completed in your
                  roadmap.
                </p>
              </div>
            </div>
          ) : (
            <div className="result-message warning">
              <AlertCircle size={20} />

              <div>
                <strong>
                  Revision Recommended
                </strong>

                <p>
                  Review the suggested areas and
                  attempt a new assessment before
                  this topic can be marked as
                  completed.
                </p>
              </div>
            </div>
          )}

          <section className="revision-section">
            <div className="result-section-heading">
              <Sparkles size={18} />

              <div>
                <span>
                  SUGGESTED REVISION
                </span>

                <h2>Areas to revisit</h2>
              </div>
            </div>

            {result.revisionAreas.length >
            0 ? (
              <div className="revision-pills">
                {result.revisionAreas.map(
                  (area) => (
                    <span key={area}>
                      {area}
                    </span>
                  )
                )}
              </div>
            ) : (
              <p className="no-revision">
                Great work. No major revision
                area was detected in this demo
                assessment.
              </p>
            )}
          </section>

          <section className="answer-review-section">
            <div className="result-section-heading">
              <CheckCircle2 size={18} />

              <div>
                <span>ANSWER REVIEW</span>
                <h2>
                  Questions & explanations
                </h2>
              </div>
            </div>

            <div className="answer-review-list">
              {result.items.map(
                (item, index) => (
                  <article
                    className={
                      item.correct
                        ? "answer-review-card correct"
                        : "answer-review-card incorrect"
                    }
                    key={item.questionId}
                  >
                    <div className="answer-review-top">
                      <span>
                        Question {index + 1}
                      </span>

                      {item.correct ? (
                        <div className="answer-status correct">
                          <CheckCircle2
                            size={14}
                          />
                          Correct
                        </div>
                      ) : (
                        <div className="answer-status incorrect">
                          <XCircle
                            size={14}
                          />
                          Incorrect
                        </div>
                      )}
                    </div>

                    <h3>
                      {item.question}
                    </h3>

                    <div className="answer-detail">
                      <span>
                        Your Answer
                      </span>

                      <p>
                        {item.userAnswer ||
                          "No answer provided"}
                      </p>
                    </div>

                    <div className="answer-detail correct-answer">
                      <span>
                        Correct / Reference
                        Answer
                      </span>

                      <p>
                        {
                          item.correctAnswer
                        }
                      </p>
                    </div>

                    <div className="answer-explanation">
                      <strong>
                        Explanation
                      </strong>

                      <p>
                        {item.explanation}
                      </p>
                    </div>
                  </article>
                )
              )}
            </div>
          </section>

          <div className="result-actions">
            {!result.passed && (
              <Link
                to={`/roadmap/assessment/${topicId}/setup`}
                className="secondary-button"
              >
                <RefreshCw size={16} />
                Take New Assessment
              </Link>
            )}

            <Link
              to="/roadmap/current"
              className="primary-button"
            >
              Return to Roadmap
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
};

export default AssessmentResultPage;
