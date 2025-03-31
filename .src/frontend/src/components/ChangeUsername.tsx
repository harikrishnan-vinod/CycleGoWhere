import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../components-css/changeUsername.css";
import { User } from "lucide-react";

function ChangeUsername() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [confirmUsername, setConfirmUsername] = useState("");
  const [usernameChanged, setUsernameChanged] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!username || !confirmUsername) {
      setError("Both username fields are required");
      return;
    }

    if (username !== confirmUsername) {
      setError("Usernames do not match");
      return;
    }

    const userUID = sessionStorage.getItem("userUID");
    if (!userUID) {
      setError("User not authenticated");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:1234/change-username", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userUID,
          newUsername: username,
        }),
      });

      if (response.ok) {
        setUsernameChanged(true);
        setError(null);
        sessionStorage.setItem("username", username);
      } else {
        const result = await response.json();
        setError(result.message || "Failed to change username");
      }
    } catch (err) {
      setError("Something went wrong");
    }
  };

  return (
    <div className="username-container">
      <div className="username-card">
        <div className="card-border-top"></div>

        <div className="username-header">
          <div className="username-icon">
            <User size={24} />
          </div>
          <h2 className="username-title">Change Username</h2>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-fields">
            <div className="form-group">
              <label htmlFor="new-username">New Username</label>
              <input
                id="new-username"
                type="text"
                placeholder="Enter new username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirm-username">Confirm New Username</label>
              <input
                id="confirm-username"
                type="text"
                placeholder="Confirm your new username"
                value={confirmUsername}
                onChange={(e) => setConfirmUsername(e.target.value)}
                required
              />
            </div>

            <div className="form-buttons">
              <button type="submit" className="submit-button">
                {usernameChanged ? "Username Changed" : "Change Username"}
              </button>
              <button
                onClick={() => navigate("/Settings")}
                type="button"
                className="cancel-button"
              >
                {usernameChanged ? "Back to Settings" : "Cancel"}
              </button>
            </div>
          </div>
        </form>

        {usernameChanged && (
          <div className="success-message">Username updated successfully!</div>
        )}

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default ChangeUsername;
