import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../components-css/changeEmail.css";

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
    <div>
      <div>
        <header>EMAIL</header>
      </div>
      <div>
        <form onSubmit={handleSubmit}>
          <ul className="change-email">
            <li>
              <input
                type="email"
                placeholder="New Email"
                className="new-email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </li>
            <li>
              <input
                type="email"
                placeholder="Confirm New Email"
                className="new-email"
                value={confirmEmail}
                onChange={(e) => setConfirmEmail(e.target.value)}
                required
              />
            </li>
            <button type="submit" className="submit-btn">
              {emailChanged ? "Email Changed" : "Change Email"}
            </button>
            <button
              onClick={() => navigate("/Settings")}
              type="button"
              className="cancel-btn"
            >
              {emailChanged ? "Back to Settings" : "Cancel"}
            </button>
          </ul>
        </form>
        {emailChanged && (
          <p style={{ color: "green", textAlign: "center", marginTop: "10px" }}>
            Email updated successfully!
          </p>
        )}
        {error && (
          <p style={{ color: "red", textAlign: "center", marginTop: "10px" }}>
            {error}
          </p>
        )}
      </div>
    </div>
  );
}

export default ChangeEmail;
