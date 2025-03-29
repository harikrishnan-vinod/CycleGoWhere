import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../components-css/changeEmail.css";

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
        sessionStorage.setItem("username", username); // optional: update sessionStorage
      } else {
        const result = await response.json();
        setError(result.message || "Failed to change username");
      }
    } catch (err) {
      setError("Something went wrong");
    }
  };

  return (
    <div>
      <div>
        <header>USERNAME</header>
      </div>
      <div>
        <form onSubmit={handleSubmit}>
          <ul className="change-email">
            <li>
              <input
                type="text"
                placeholder="New Username"
                className="new-email"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </li>
            <li>
              <input
                type="text"
                placeholder="Confirm New Username"
                className="new-email"
                value={confirmUsername}
                onChange={(e) => setConfirmUsername(e.target.value)}
                required
              />
            </li>
            <button type="submit" className="submit-btn">
              {usernameChanged ? "Username Changed" : "Change Username"}
            </button>
            <button
              onClick={() => navigate("/Settings")}
              type="button"
              className="cancel-btn"
            >
              {usernameChanged ? "Back to Settings" : "Cancel"}
            </button>
            {error && <p style={{ color: "red" }}>{error}</p>}
          </ul>
        </form>
      </div>
    </div>
  );
}

export default ChangeUsername;
