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

const CVReviewPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [reviewing, setReviewing] = useState(false);
  const [showReview, setShowReview] = useState(false);

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Please upload your CV in PDF format.");
      setSelectedFile(null);
      setShowReview(false);
      return;
    }

    setError("");
    setSelectedFile(file);
    setShowReview(false);
  };

  const removeFile = () => {
    setSelectedFile(null);
    setShowReview(false);
    setError("");
  };

  const handleReview = () => {
    if (!selectedFile) {
      setError("Please upload a CV before requesting a review.");
      return;
    }

    setReviewing(true);
    setError("");
    setShowReview(false);

    // Temporary mock review.
    // Later this will be replaced by the FastAPI CV review endpoint.
    setTimeout(() => {
      setReviewing(false);
      setShowReview(true);
    }, 1000);
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
                Your uploaded file is currently used only for the UI
                demonstration and is not sent to a server.
              </p>
            </motion.section>

            {/* Information / dummy response side */}

            <motion.section
              className="cv-result-panel"
              initial={{ opacity: 0, x: 25 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.18 }}
            >
              {!showReview ? (
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
                      <strong>82</strong>
                      <span>/100</span>
                    </div>
                  </div>

                  <div className="cv-score-bar">
                    <div />
                  </div>

                  <div className="cv-feedback-section positive">
                    <h3>
                      <CheckCircle2 size={18} />
                      What looks good
                    </h3>

                    <ul>
                      <li>
                        Your CV has a clean and readable overall
                        structure.
                      </li>

                      <li>
                        Technical skills are presented clearly.
                      </li>

                      <li>
                        Project experience is relevant to software
                        engineering roles.
                      </li>
                    </ul>
                  </div>

                  <div className="cv-feedback-section improvement">
                    <h3>
                      <Sparkles size={18} />
                      Areas to improve
                    </h3>

                    <ul>
                      <li>
                        Make project descriptions more
                        achievement-oriented.
                      </li>

                      <li>
                        Use measurable results where possible.
                      </li>

                      <li>
                        Keep the skills section focused on technologies
                        relevant to your target role.
                      </li>
                    </ul>
                  </div>

                  <div className="cv-dummy-warning">
                    This is a temporary dummy response. AI-generated
                    CV analysis will be connected later.
                  </div>

                  <button
                    type="button"
                    className="secondary-button cv-review-again"
                    onClick={() => setShowReview(false)}
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