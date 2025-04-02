import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        // Just call your Flask backend to clear session
        const response = await fetch("http://127.0.0.1:1234/logout", {
          method: "POST",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to log out from Flask server");
        }

        console.log("Flask logout successful");

        // Clear client-side storage
        sessionStorage.clear();
        sessionStorage.clear();
        document.cookie.split(";").forEach((cookie) => {
          const cookieName = cookie.split("=")[0].trim();
          document.cookie = `${cookieName}=;expires=${new Date().toUTCString()};path=/;domain=localhost`;
        });

        // Navigate back
        window.location.href = "/login";
      } catch (error) {
        console.error("Logout failed:", error);
        navigate("/login", { replace: true });
      }
    };

    handleLogout();
  }, [navigate]);

  return null;
}

export default Logout;
