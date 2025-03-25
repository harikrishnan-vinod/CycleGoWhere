import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../components-css/changePassword.css";

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPassword((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (password.newpassword === password.confirmnewpassword) {
      console.log("Password Changed");

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
          console.log("Password updated successfully!");
          navigate("/Settings");
        } else {
          console.log("Error updating password.");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    } else {
      console.log("Passwords do not match");
    }
  };

  return (
    <div>
      <div>
        <header>CHANGE PASSWORD</header>
      </div>
      <div>
        <form onSubmit={handleSubmit}>
          <ul className="change-password">
            <li>
              <input
                type="password"
                placeholder="Enter current password"
                className="current-password"
                onChange={handleChange}
                name="password"
                required
              />
            </li>
            <li>
              <input
                type="password"
                placeholder="New Password"
                className="new-password"
                onChange={handleChange}
                name="newpassword"
                required
              />
            </li>
            <li>
              <input
                type="password"
                placeholder="Confirm New Password"
                className="new-password"
                onChange={handleChange}
                name="confirmnewpassword"
                required
              />
            </li>
            <button type="submit" className="submit-btn">
              Change Password
            </button>
            <button
              onClick={() => navigate("/Settings")}
              type="button"
              className="cancel-btn"
            >
              Cancel
            </button>
          </ul>
        </form>
      </div>
    </div>
  );
}

export default ChangePassword;
