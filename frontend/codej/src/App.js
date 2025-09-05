import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import Accounts from "./pages/Accounts";
import AuthCallback from "./pages/AuthCallback";
import Home from "./pages/Home";

function RequireAuth({ children }) {
  const token = localStorage.getItem("session_token");
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
}

function PublicOnly({ children }) {
  const token = localStorage.getItem("session_token");
  if (token) {
    return <Navigate to="/home" replace />;
  }
  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PublicOnly><Landing /></PublicOnly>} />
        <Route path="/home" element={<RequireAuth><Home /></RequireAuth>} />
        <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
