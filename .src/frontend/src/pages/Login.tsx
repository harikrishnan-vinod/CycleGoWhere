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
    <div className="login-container">
      <img
        className="cyclinggowhere-logo"
        src={logo}
        alt="Cycling Go Where Logo"
      />

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSignIn}>
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

        <button
          type="button"
          className="google-login-button"
          onClick={() =>
            (window.location.href = "http://127.0.0.1:1234/google-login")
          }
        >
          Sign in with Google
        </button>

        <button
          type="button"
          className="register-button"
          onClick={() => navigate("/register")}
        >
          Register
        </button>
      </form>
    </div>
  );
}

export default Login;
