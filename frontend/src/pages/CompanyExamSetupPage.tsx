import { Link, useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";

import {
  ArrowLeft,
  BookOpenCheck,
  BrainCircuit,
  Clock3,
  Infinity,
  ListChecks,
  Sparkles,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

import { companies } from "../features/company-prep/data/companies";

const CompanyExamSetupPage = () => {
  const { companySlug } = useParams();
  const navigate = useNavigate();

  const company = companies.find(
    (item) => item.slug === companySlug
  );

  if (!company) {
    return (
      <>
        <Navbar />

        <main className="company-not-found">
          <h1>Company not found</h1>

          <Link
            to="/company-prep"
            className="primary-button"
          >
            Back to Companies
          </Link>
        </main>
      </>
    );
  }

  const handleExamSelection = (
    mode: "20" | "40" | "all"
  ) => {
    /*
      UI ONLY FOR NOW.

      Later this will become something like:

      navigate(
        `/company-prep/${company.slug}/exam?mode=${mode}`
      );

      when the actual exam page is created.
    */

    alert(
      `${company.name}: ${mode === "all" ? "All questions" : `${mode} questions`} selected.\n\nExam UI will be connected later.`
    );
  };

  return (
    <>
      <Navbar />

      <main className="exam-setup-page">
        <div className="company-page-glow company-glow-one" />

        <div className="container exam-setup-container">
          <button
            className="company-back-link company-back-button"
            onClick={() => navigate("/company-prep")}
          >
            <ArrowLeft size={17} />
            All Companies
          </button>

          <motion.div
            className="exam-company-header"
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="selected-company-avatar">
              {company.shortName}
            </div>

            <div>
              <span className="exam-company-label">
                COMPANY PREPARATION
              </span>

              <h1>{company.name}</h1>

              <p>
                Choose how many questions you want to practice
                in this mock interview session.
              </p>
            </div>
          </motion.div>

          <div className="exam-option-grid">
            <motion.button
              className="exam-option-card"
              onClick={() => handleExamSelection("20")}
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              whileHover={{ y: -5 }}
            >
              <div className="exam-option-icon">
                <ListChecks size={25} />
              </div>

              <span className="exam-option-tag">
                QUICK PRACTICE
              </span>

              <h2>20 Questions</h2>

              <p>
                A focused mock exam for a shorter preparation
                session.
              </p>

              <div className="exam-meta">
                <span>
                  <Clock3 size={15} />
                  Quick session
                </span>

                <span>
                  <BrainCircuit size={15} />
                  Mixed topics
                </span>
              </div>

              <div className="exam-option-action">
                Examine Yourself
              </div>
            </motion.button>

            <motion.button
              className="exam-option-card featured-exam-option"
              onClick={() => handleExamSelection("40")}
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.18 }}
              whileHover={{ y: -5 }}
            >
              <div className="recommended-label">
                <Sparkles size={13} />
                Recommended
              </div>

              <div className="exam-option-icon">
                <BookOpenCheck size={25} />
              </div>

              <span className="exam-option-tag">
                FULL PRACTICE
              </span>

              <h2>40 Questions</h2>

              <p>
                A broader assessment covering more of the
                company's collected interview topics.
              </p>

              <div className="exam-meta">
                <span>
                  <Clock3 size={15} />
                  Extended session
                </span>

                <span>
                  <BrainCircuit size={15} />
                  Wider coverage
                </span>
              </div>

              <div className="exam-option-action">
                Examine Yourself
              </div>
            </motion.button>

            <motion.button
              className="exam-option-card"
              onClick={() => handleExamSelection("all")}
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.26 }}
              whileHover={{ y: -5 }}
            >
              <div className="exam-option-icon">
                <Infinity size={25} />
              </div>

              <span className="exam-option-tag">
                COMPLETE COLLECTION
              </span>

              <h2>All Questions</h2>

              <p>
                Attempt the complete available question
                collection for {company.name}.
              </p>

              <div className="exam-meta">
                <span>
                  <Infinity size={15} />
                  Complete set
                </span>

                <span>
                  <BrainCircuit size={15} />
                  Maximum coverage
                </span>
              </div>

              <div className="exam-option-action">
                Examine With All Questions
              </div>
            </motion.button>
          </div>

          <div className="exam-info-box">
            <Sparkles size={19} />

            <p>
              The actual number of available questions will later
              come from the backend question bank. For now, this
              screen represents the complete frontend flow.
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
};

export default CompanyExamSetupPage;