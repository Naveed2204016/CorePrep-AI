import { useState } from "react";
import type { ChangeEvent } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

import {
  AlertCircle,
  ArrowLeft,
  CheckCircle2,
  FileText,
  RotateCcw,
  Sparkles,
  UploadCloud,
  X,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import { cvReviewService } from "../services/cvReviewService";
import type { CVReviewResult } from "../types/cvReview";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

const CVReviewPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [reviewing, setReviewing] = useState(false);
  const [review, setReview] = useState<CVReviewResult | null>(null);

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Please upload your CV in PDF format.");
      setSelectedFile(null);
      setReview(null);
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError("Please upload a PDF that is 5 MB or smaller.");
      setSelectedFile(null);
      setReview(null);
      return;
    }

    setError("");
    setSelectedFile(file);
    setReview(null);
  };

  const removeFile = () => {
    setSelectedFile(null);
    setReview(null);
    setError("");
  };

  const handleReview = async () => {
    if (!selectedFile) {
      setError("Please upload a CV before requesting a review.");
      return;
    }

    setReviewing(true);
    setError("");
    setReview(null);

    try {
      setReview(await cvReviewService.analyze(selectedFile));
    } catch (cause) {
      setError(
        cause instanceof Error
          ? cause.message
          : "The CV could not be reviewed. Please try again.",
      );
    } finally {
      setReviewing(false);
    }
  };

  return (
    <>
      <Navbar />

      <main className="cv-review-page">
        <div className="cv-review-glow cv-glow-one" />
        <div className="cv-review-glow cv-glow-two" />

        <div className="container cv-review-container">
          <Link to="/" className="company-back-link">
            <ArrowLeft size={17} />
            Back to Home
          </Link>

          <motion.div
            className="cv-review-heading"
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="hero-badge">
              <Sparkles size={15} />
              AI-Assisted CV Review
            </div>

            <h1>
              Make your CV ready for
              <br />
              your next <span>opportunity.</span>
            </h1>

            <p>
              Upload your CV in PDF format and receive focused
              feedback on its structure, clarity, skills and overall
              presentation.
            </p>
          </motion.div>

          <div className="cv-review-workspace">
            {/* Upload side */}

            <motion.section
              className="cv-upload-panel"
              initial={{ opacity: 0, x: -25 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.12 }}
            >
              <div className="cv-panel-title">
                <div className="cv-title-icon">
                  <FileText size={21} />
                </div>

                <div>
                  <h2>Upload Your CV</h2>
                  <p>Only PDF files are accepted.</p>
                </div>
              </div>

              {!selectedFile ? (
                <label className="cv-drop-zone">
                  <input
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileChange}
                    hidden
                  />

                  <div className="cv-upload-icon">
                    <UploadCloud size={30} />
                  </div>

                  <h3>Choose your CV</h3>

                  <p>
                    Select a PDF file from your device to begin the
                    review.
                  </p>

                  <span className="cv-choose-button">
                    Browse PDF
                  </span>
                </label>
              ) : (
                <div className="cv-selected-file">
                  <div className="cv-file-icon">
                    <FileText size={25} />
                  </div>

                  <div className="cv-file-details">
                    <strong>{selectedFile.name}</strong>

                    <span>
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      &nbsp; • &nbsp; PDF
                    </span>
                  </div>

                  <button
                    type="button"
                    className="cv-remove-file"
                    onClick={removeFile}
                    aria-label="Remove uploaded CV"
                  >
                    <X size={18} />
                  </button>
                </div>
              )}

              {error && (
                <div className="cv-error">
                  <AlertCircle size={16} />
                  {error}
                </div>
              )}

              <button
                type="button"
                className="primary-button cv-review-button"
                onClick={handleReview}
                disabled={!selectedFile || reviewing}
              >
                {reviewing ? (
                  <>
                    <span className="cv-loader" />
                    Reviewing CV...
                  </>
                ) : (
                  <>
                    <Sparkles size={17} />
                    Get Review
                  </>
                )}
              </button>

              <p className="cv-privacy-note">
                Your PDF is processed in memory for this review and is
                not saved by CorePrep.
              </p>
            </motion.section>

            {/* Information / dummy response side */}

            <motion.section
              className="cv-result-panel"
              initial={{ opacity: 0, x: 25 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.18 }}
            >
              {!review ? (
                <div className="cv-empty-review">
                  <div className="cv-empty-icon">
                    <Sparkles size={28} />
                  </div>

                  <h2>Your review will appear here</h2>

                  <p>
                    Upload your CV and click <strong>Get Review</strong>{" "}
                    to see feedback on your resume.
                  </p>

                  <div className="cv-review-preview">
                    <span>
                      <CheckCircle2 size={15} />
                      Structure & readability
                    </span>

                    <span>
                      <CheckCircle2 size={15} />
                      Skills presentation
                    </span>

                    <span>
                      <CheckCircle2 size={15} />
                      Experience descriptions
                    </span>

                    <span>
                      <CheckCircle2 size={15} />
                      Improvement suggestions
                    </span>
                  </div>
                </div>
              ) : (
                <motion.div
                  className="cv-dummy-result"
                  initial={{ opacity: 0, y: 18 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <div className="cv-result-header">
                    <div>
                      <span>CV REVIEW COMPLETE</span>
                      <h2>Your CV Analysis</h2>
                    </div>

                    <div className="cv-score">
                      <strong>{review.score}</strong>
                      <span>/100</span>
                    </div>
                  </div>

                  <div className="cv-score-bar">
                    <div style={{ width: `${review.score}%` }} />
                  </div>

                  <p className="cv-review-summary">{review.summary}</p>

                  <div className="cv-feedback-section positive">
                    <h3>
                      <CheckCircle2 size={18} />
                      What looks good
                    </h3>

                    <ul>{review.strengths.map((item) => <li key={item}>{item}</li>)}</ul>
                  </div>

                  <div className="cv-feedback-section improvement">
                    <h3>
                      <Sparkles size={18} />
                      Areas to improve
                    </h3>

                    <div className="cv-improvement-list">
                      {review.improvements.map((item) => (
                        <article className="cv-improvement-card" key={`${item.priority}-${item.title}`}>
                          <div>
                            <span className={`cv-priority cv-priority-${item.priority}`}>
                              {item.priority} priority
                            </span>
                            <h4>{item.title}</h4>
                          </div>
                          <p>{item.detail}</p>
                          <small><strong>Rewrite tip:</strong> {item.rewrite_tip}</small>
                        </article>
                      ))}
                    </div>
                  </div>

                  {(review.missing_sections.length > 0 || review.keywords_found.length > 0) && (
                    <div className="cv-review-meta">
                      {review.missing_sections.length > 0 && (
                        <div>
                          <h3>Missing or useful sections</h3>
                          <div className="cv-chip-list">
                            {review.missing_sections.map((item) => <span key={item}>{item}</span>)}
                          </div>
                        </div>
                      )}
                      {review.keywords_found.length > 0 && (
                        <div>
                          <h3>Technical keywords found</h3>
                          <div className="cv-chip-list cv-keyword-list">
                            {review.keywords_found.map((item) => <span key={item}>{item}</span>)}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  <div className="cv-review-file-note">
                    Reviewed {review.file_name} · {review.page_count} {review.page_count === 1 ? "page" : "pages"}
                  </div>

                  <button
                    type="button"
                    className="secondary-button cv-review-again"
                    onClick={() => setReview(null)}
                  >
                    <RotateCcw size={16} />
                    Review Again
                  </button>
                </motion.div>
              )}
            </motion.section>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
};

export default CVReviewPage;
