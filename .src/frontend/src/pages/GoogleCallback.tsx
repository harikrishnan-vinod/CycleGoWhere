import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

function GoogleCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const email = searchParams.get("email");
    const userUID = searchParams.get("userUID");
    const username = searchParams.get("username");

    if (email && userUID && username) {
      sessionStorage.setItem("email", email);
      sessionStorage.setItem("userUID", userUID);
      sessionStorage.setItem("username", username);
      navigate("/mainpage");
    } else {
      // Invalid login or redirect — fallback to login
      navigate("/login");
    }
  }, [navigate, searchParams]);

  return <p>Logging you in...</p>;
}

export default GoogleCallback;
