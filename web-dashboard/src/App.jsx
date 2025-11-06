import { useState, useEffect } from "react";
import LoginForm from "./components/LoginForm";
import DashboardLayout from "./components/DashboardLayout";

export default function App() {
  const [isLogged, setIsLogged] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) setIsLogged(true);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setIsLogged(false);
  };

  return isLogged ? (
    <DashboardLayout onLogout={handleLogout} />
  ) : (
    <LoginForm onLogin={() => setIsLogged(true)} />
  );
}
