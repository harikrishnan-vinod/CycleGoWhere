import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../pages-css/Register.css";
import logo from "../assets/cyclegowherelogo.png";

function Register() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords do not match!");
      return;
    }

    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:1234/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          email,
          username,
          password,
          firstName,
          lastName,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        alert(result.message);
        navigate("/login");
      } else {
        setError(result.message || "Registration failed!");
      }
    } catch (error) {
      setError("Error: Unable to register.");
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = "http://127.0.0.1:1234/google-login";
  };

  return (
    <div className="register-page-container">
      <div className="register-logo-section">
        <img
          src={logo}
          alt="Cycling Go Where Logo"
          className="cyclinggowhere-logo"
        />
      </div>

      <div className="register-form-section">
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button
          type="button"
          className="google-login-button"
          onClick={handleGoogleLogin}
        >
          <img
            src="https://developers.google.com/identity/images/g-logo.png"
            alt="Google logo"
            className="google-icon"
          />
          Log in with Google
        </button>

        <div className="divider">
          <span>OR</span>
        </div>

        <form onSubmit={handleRegister} className="register-form">
          <div className="register-box">
            <input
              type="email"
              placeholder="Email"
              className="register-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="register-box">
            <input
              type="text"
              placeholder="Username"
              className="register-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="register-box">
            <input
              type="text"
              placeholder="First Name"
              className="register-input"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          <div className="register-box">
            <input
              type="text"
              placeholder="Last Name"
              className="register-input"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>

          <div className="register-box">
            <input
              type="password"
              placeholder="Password"
              className="register-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="register-box">
            <input
              type="password"
              placeholder="Confirm Password"
              className="register-input"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button className="register-submit-button" type="submit">
            Register
          </button>

          <button
            type="button"
            className="back-to-login-button"
            onClick={() => navigate("/login")}
          >
            Back to Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;
