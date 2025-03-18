import "../pages-css/Login.css";
import { useState } from "react";
import { UserRoundCheck, Lock } from "lucide-react";
import logo from "../assets/cyclegowherelogo.png";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Handle form submission
  const handleSignIn = async (event: { preventDefault: () => void }) => {
    event.preventDefault(); // Prevent page reload
    setLoading(true);
    setError(null);
  
    try {
      const response = await fetch("http://127.0.0.1:1234/auth", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // Ensure cookies are sent
        body: JSON.stringify({ email, password }),
      });
  
      const result = await response.json();
  
      if (response.ok) {
        console.log("Login successful:", result);
        sessionStorage.setItem("email", email);
        sessionStorage.setItem("userId", result.userId);
        window.location.href = "/dashboard"; 
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
      <img className="cyclinggowhere-logo" src={logo} alt="Cycling Go Where Logo" />
      
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSignIn}>
        <div className="username-box">
          <UserRoundCheck size="16" color="gray" />
          <input
            type="email"
            placeholder="Email"
            className="username-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
      </form>
    </div>
  );
}

export default Login;
