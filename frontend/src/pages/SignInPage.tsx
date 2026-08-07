import { useState } from "react";
import type { FormEvent } from "react";

import { Link, useNavigate } from "react-router-dom";

import {
  ArrowLeft,
  BrainCircuit,
  Sparkles,
} from "lucide-react";

import GoogleButton from "../components/ui/GoogleButton";
import { authService } from "../services/authService";

const SignInPage = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      await authService.login({
        email,
        password,
      });

      /*
        Later:
        navigate("/dashboard");
      */

      navigate("/");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to sign in."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGoogle = async () => {
    await authService.continueWithGoogle();
  };

  return (
    <main className="auth-page">
      <Link to="/" className="back-link">
        <ArrowLeft size={17} />
        Back Home
      </Link>

      <div className="auth-container">
        <section className="auth-visual">
          <div className="auth-visual-content">
            <div className="auth-big-icon">
              <BrainCircuit size={34} />
            </div>

            <span>COREPREP AI</span>

            <h2>
              Prepare with direction,
              <br />
              not confusion.
            </h2>

            <p>
              Personalized roadmaps, interview questions,
              intelligent assessments and measurable progress.
            </p>

            <div className="auth-insight">
              <Sparkles size={19} />

              <div>
                <small>COREPREP INSIGHT</small>
                <strong>
                  Make every study session count.
                </strong>
              </div>
            </div>
          </div>
        </section>

        <section className="auth-form-side">
          <div className="auth-form">
            <Link to="/" className="auth-logo">
              CorePrep <span>AI</span>
            </Link>

            <h1>Welcome back</h1>

            <p className="auth-subtitle">
              Continue your interview preparation journey.
            </p>

            <GoogleButton onClick={handleGoogle} />

            <div className="divider">
              <span />
              <p>or continue with email</p>
              <span />
            </div>

            <form onSubmit={handleSubmit}>
              <div className="input-group">
                <label>Email address</label>

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  required
                />
              </div>

              <div className="input-group">
                <div className="password-label">
                  <label>Password</label>

                  <button type="button">
                    Forgot password?
                  </button>
                </div>

                <input
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  required
                />
              </div>

              {error && (
                <p className="error-message">{error}</p>
              )}

              <button
                type="submit"
                className="primary-button auth-button"
                disabled={loading}
              >
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </form>

            <p className="auth-switch">
              New to CorePrep AI?
              <Link to="/signup"> Create account</Link>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
};

export default SignInPage;