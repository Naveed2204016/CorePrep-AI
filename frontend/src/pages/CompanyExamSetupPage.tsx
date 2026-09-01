import { useEffect, useRef, useState } from "react";
import { AlertCircle, LoaderCircle } from "lucide-react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { companyPrepService } from "../services/companyPrepService";

const CompanyExamSetupPage = () => {
  const { companySlug } = useParams();
  const navigate = useNavigate();
  const started = useRef(false);
  const [startError, setStartError] = useState("");

  useEffect(() => {
    if (!companySlug || started.current) return;
    started.current = true;

    companyPrepService
      .createExam(companySlug, "20")
      .then(() =>
        navigate(`/company-prep/${companySlug}/exam`, { replace: true }),
      )
      .catch((cause: unknown) => {
        setStartError(
          cause instanceof Error
            ? cause.message
            : "Could not start the exam.",
        );
      });
  }, [companySlug, navigate]);

  return (
    <main className="assessment-evaluation-loading">
      {startError ? <AlertCircle size={42} /> : <LoaderCircle size={42} />}
      <span>COMPANY PREPARATION</span>
      <h1>
        {startError
          ? "Could not start practice"
          : "Preparing your questions"}
      </h1>
      <p>
        {startError || "Loading a tailored 20-question practice set..."}
      </p>
      {startError && (
        <Link to="/company-prep" className="primary-button">
          Return to Companies
        </Link>
      )}
    </main>
  );
};

export default CompanyExamSetupPage;
