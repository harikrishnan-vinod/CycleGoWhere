import "../pages-css/Login.css";
import { useState } from "react";
import { UserRoundCheck, Lock } from "lucide-react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/cyclegowherelogo.png";

function Login() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignIn = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:1234/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ login, password }),
      });

      const result = await response.json();

      if (response.ok) {
        sessionStorage.setItem("email", result.email);
        sessionStorage.setItem("userId", result.userId);
        sessionStorage.setItem("username", result.username);
        window.location.href = "/mainpage";
      } else {
        setError(result.message || "Invalid credentials, try again!");
      }
    } catch (error) {
      setError("Error: Unable to sign in");
    } finally {
      setLoading(false);
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
        <h1 className="headline">Happening now</h1>
        <h2 className="subheadline">Join today.</h2>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <form onSubmit={handleSignIn} className="login-form">
          <div className="username-box">
            <UserRoundCheck size="16" color="gray" />
            <input
              type="text"
              placeholder="Email or Username"
              className="username-input"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              required
            />
          </div>

          <div className="password-box">
            <Lock size="16" color="gray" />
            <input
              type="password"
              placeholder="Password"
              className="password-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button className="login-button" type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>

          <div className="divider">
            <span>or</span>
          </div>

          <button
            type="button"
            className="google-login-button"
            onClick={() =>
              (window.location.href = "http://127.0.0.1:1234/google-login")
            }
          >
            <img
              src="https://developers.google.com/identity/images/g-logo.png"
              alt="Google logo"
              className="google-icon"
            />
            Sign in with Google
          </button>

          <button
            type="button"
            className="register-button"
            onClick={() => navigate("/register")}
          >
            Create account
          </button>

          <p className="disclaimer">
            By signing up, you agree to the <a href="#">Terms of Service</a> and{" "}
            <a href="#">Privacy Policy</a>, including <a href="#">Cookie Use</a>
            .
          </p>
        </form>
      </div>
    </div>
  );
}

export default Login;
