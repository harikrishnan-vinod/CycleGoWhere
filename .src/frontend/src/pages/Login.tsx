import "../pages-css/Login.css";
import { useState } from "react";
import { UserRoundCheck, Lock } from "lucide-react";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div className="login-container">
      <img className="cyclinggowhere-logo" src=""></img>
      <div className="username-box">
        <UserRoundCheck size="16" />
        <input
          type="text"
          placeholder="Email ID or Username"
          className="username-input"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        ></input>
      </div>
      <div className="password-box">
        <Lock size="16" />
        <input
          type="text"
          placeholder="Password"
          className="password-input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        ></input>
      </div>
      {/* this button should submit the username and password to backend and if successful fetch the required data */}
      <button className="login-button">Login</button>
    </div>
  );
}

export default Login;
