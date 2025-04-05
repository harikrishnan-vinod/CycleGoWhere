import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../components-css/changePassword.css";
import { Lock } from "lucide-react";

function ChangePassword() {
  interface PasswordData {
    password: string;
    newpassword: string;
    confirmnewpassword: string;
  }

  const navigate = useNavigate();
  const [password, setPassword] = useState<PasswordData>({
    password: "",
    newpassword: "",
    confirmnewpassword: "",
  });
  const [passwordChanged, setPasswordChanged] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPassword((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (
      !password.password ||
      !password.newpassword ||
      !password.confirmnewpassword
    ) {
      setError("All password fields are required");
      return;
    }

    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$/;

    if (!passwordRegex.test(password.newpassword)) {
      setError(
        "Password must be at least 8 characters long and include an uppercase letter, lowercase letter, number, and symbol."
      );
      return;
    }

    if (password.newpassword !== password.confirmnewpassword) {
      setError("New passwords do not match");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:1234/change-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: sessionStorage.getItem("email"),
          oldPassword: password.password,
          newPassword: password.newpassword,
        }),
      });

      if (response.ok) {
        setPasswordChanged(true);
        setError(null);
      } else {
        const result = await response.json();
        setError(result.message || "Failed to change password");
      }
    } catch (error) {
      setError("Something went wrong");
    }
  };

  return (
    <div className="password-container">
      <div className="password-card">
        <div className="card-border-top"></div>

        <div className="password-header">
          <div className="password-icon">
            <Lock size={24} />
          </div>
          <h2 className="password-title">Change Password</h2>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-fields">
            <div className="form-group">
              <label htmlFor="current-password">Current Password</label>
              <input
                id="current-password"
                type="password"
                placeholder="Enter current password"
                name="password"
                value={password.password}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="new-password">New Password</label>
              <input
                id="new-password"
                type="password"
                placeholder="Enter new password"
                name="newpassword"
                value={password.newpassword}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirm-password">Confirm New Password</label>
              <input
                id="confirm-password"
                type="password"
                placeholder="Confirm your new password"
                name="confirmnewpassword"
                value={password.confirmnewpassword}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-buttons">
              <button type="submit" className="submit-button">
                {passwordChanged ? "Password Changed" : "Change Password"}
              </button>
              <button
                onClick={() => navigate("/Settings")}
                type="button"
                className="cancel-button"
              >
                {passwordChanged ? "Back to Settings" : "Cancel"}
              </button>
            </div>
          </div>
        </form>

        {passwordChanged && (
          <div className="success-message">Password updated successfully!</div>
        )}

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default ChangePassword;
