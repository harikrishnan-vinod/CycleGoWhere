import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../components-css/changeEmail.css";
import { Mail } from "lucide-react";

function ChangeEmail() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [confirmEmail, setConfirmEmail] = useState("");
  const [emailChanged, setEmailChanged] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !confirmEmail) {
      setError("Both email fields are required");
      return;
    }
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email address");
      return;
    }
    if (email !== confirmEmail) {
      setError("Emails do not match");
      return;
    }

    const currentEmail = sessionStorage.getItem("email");
    const userUID = sessionStorage.getItem("userUID");
    if (!currentEmail || !userUID) {
      setError("User not authenticated");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:1234/change-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          currentEmail,
          newEmail: email,
          userUID,
        }),
      });

      if (response.ok) {
        setEmailChanged(true);
        setError(null);
        sessionStorage.setItem("email", email);
      } else {
        const result = await response.json();
        setError(result.message || "Failed to change email");
      }
    } catch (err) {
      setError("Something went wrong");
    }
  };

  return (
    <div className="email-container">
      <div className="email-card">
        <div className="card-border-top"></div>

        <div className="email-header">
          <div className="email-icon">
            <Mail size={24} />
          </div>
          <h2 className="email-title">Change Email</h2>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-fields">
            <div className="form-group">
              <label htmlFor="new-email">New Email</label>
              <input
                id="new-email"
                type="email"
                placeholder="Enter new email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirm-email">Confirm New Email</label>
              <input
                id="confirm-email"
                type="email"
                placeholder="Confirm your new email address"
                value={confirmEmail}
                onChange={(e) => setConfirmEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-buttons">
              <button type="submit" className="submit-button">
                {emailChanged ? "Email Changed" : "Change Email"}
              </button>
              <button
                onClick={() => navigate("/Settings")}
                type="button"
                className="cancel-button"
              >
                {emailChanged ? "Back to Settings" : "Cancel"}
              </button>
            </div>
          </div>
        </form>

        {emailChanged && (
          <div className="success-message">Email updated successfully!</div>
        )}

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default ChangeEmail;
