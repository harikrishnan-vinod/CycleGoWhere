import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getAuth, signOut } from "firebase/auth";

function Logout() {
    const navigate = useNavigate();

    useEffect(() => {
        const handleLogout = async () => {
            try {
                // Sign out from Firebase
                const auth = getAuth();
                await signOut(auth);
                console.log("Firebase sign-out successful");

                // Clear session on Flask server
                const response = await fetch("http://127.0.0.1:1234/logout", {
                    method: "POST",
                    credentials: "include", // Important for Flask session clearing
                });

                if (!response.ok) {
                    throw new Error("Failed to log out from Flask server");
                }

                console.log("Flask logout successful");

                // Clear all session-related storage
                sessionStorage.clear();
                localStorage.clear();
                document.cookie.split(";").forEach((cookie) => {
                    const cookieName = cookie.split("=")[0].trim();
                    document.cookie = `${cookieName}=;expires=${new Date().toUTCString()};path=/;domain=localhost`;
                });

                // Force a page refresh to ensure session is fully cleared
                setTimeout(() => {
                    window.location.href = "/login"; // Use this instead of navigate()
                }, 2000);  // Increased delay to allow session to fully clear

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
