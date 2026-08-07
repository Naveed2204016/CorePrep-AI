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

const SignUpPage = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    setError("");

    if (
      formData.password !== formData.confirmPassword
    ) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await authService.register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      });

      navigate("/signin");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to create account."
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

            <span>START PREPARING</span>

            <h2>
              Build one clear path
              <br />
              toward your goal.
            </h2>

            <p>
              Organize your CS fundamentals, practice
              interview questions and improve continuously.
            </p>

            <div className="auth-insight">
              <Sparkles size={19} />

              <div>
                <small>PERSONALIZED PREPARATION</small>
                <strong>
                  Your roadmap. Your progress.
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

            <h1>Create your account</h1>

            <p className="auth-subtitle">
              Start your interview preparation journey.
            </p>

            <GoogleButton onClick={handleGoogle} />

            <div className="divider">
              <span />
              <p>or continue with email</p>
              <span />
            </div>

            <form onSubmit={handleSubmit}>
              <div className="input-group">
                <label>Full name</label>

                <input
                  type="text"
                  placeholder="Your full name"
                  value={formData.name}
                  onChange={(event) =>
                    setFormData({
                      ...formData,
                      name: event.target.value,
                    })
                  }
                  required
                />
              </div>

              <div className="input-group">
                <label>Email address</label>

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={formData.email}
                  onChange={(event) =>
                    setFormData({
                      ...formData,
                      email: event.target.value,
                    })
                  }
                  required
                />
              </div>

              <div className="two-inputs">
                <div className="input-group">
                  <label>Password</label>

                  <input
                    type="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={(event) =>
                      setFormData({
                        ...formData,
                        password: event.target.value,
                      })
                    }
                    required
                  />
                </div>

                <div className="input-group">
                  <label>Confirm Password</label>

                  <input
                    type="password"
                    placeholder="Confirm password"
                    value={formData.confirmPassword}
                    onChange={(event) =>
                      setFormData({
                        ...formData,
                        confirmPassword:
                          event.target.value,
                      })
                    }
                    required
                  />
                </div>
              </div>

              {error && (
                <p className="error-message">{error}</p>
              )}

              <button
                type="submit"
                className="primary-button auth-button"
                disabled={loading}
              >
                {loading
                  ? "Creating account..."
                  : "Create Account"}
              </button>
            </form>

            <p className="auth-switch">
              Already have an account?
              <Link to="/signin"> Sign in</Link>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
};

export default SignUpPage;