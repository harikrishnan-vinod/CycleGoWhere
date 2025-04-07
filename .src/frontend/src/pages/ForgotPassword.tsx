import "../pages-css/Login.css";
import { useState } from "react";
import logo from "../assets/cyclegowherelogo.png";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:1234";

  const handleResetPassword = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setMessage(null);
    setError(null);

    if (!email.trim()) {
      setError("Email cannot be empty");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email }),
      });

      const result = await response.json();
      if (response.ok) {
        setMessage("Reset link sent to your email.");
      } else {
        setError(result.message || "Unable to send reset link.");
      }
    } catch {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="login-page-container">
      <div className="logo-section">
        <img
          src={logo}
          alt="Cycling Go Where Logo"
          className="cyclinggowhere-logo"
        />
      </div>
      <div className="form-section">
        <h1 className="headline">Forgot your password?</h1>
        <h2 className="subheadline">We’ll send you a reset link.</h2>

        {message && <p style={{ color: "green" }}>{message}</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        <form onSubmit={handleResetPassword} className="login-form">
          <div className="username-box">
            <input
              type="email"
              placeholder="Enter your email"
              className="username-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <button className="login-button" type="submit">
            Send Reset Link
          </button>

          <button
            type="button"
            className="back-to-login-button"
            onClick={() => (window.location.href = "/")}
          >
            Go back to login page
          </button>
        </form>
      </div>
    </div>
  );
}

export default ForgotPassword;
