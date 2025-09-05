import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function AuthCallback() {
  const navigate = useNavigate();
  useEffect(() => {
    const hash = new URLSearchParams(window.location.hash.slice(1));
    const token = hash.get("token");
    if (token) {
      localStorage.setItem("session_token", token);
      navigate("/home", { replace: true });
    } else {
      navigate("/", { replace: true });
    }
  }, [navigate]);
  return null;
}


