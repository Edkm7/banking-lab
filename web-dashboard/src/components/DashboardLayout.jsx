import { useState } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import UsersPage from "./UsersPage";
import AccountsPage from "./AccountsPage";
import ReportsPage from "./ReportsPage";

export default function DashboardLayout({ onLogout }) {
  const [activePage, setActivePage] = useState("users");

  const renderPage = () => {
    switch (activePage) {
      case "accounts": return <AccountsPage />;
      case "reports": return <ReportsPage />;
      default: return <UsersPage />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar active={activePage} onSelect={setActivePage} />
      <div className="flex flex-col flex-1">
        <Header onLogout={onLogout} />
        <main className="p-6 overflow-auto">{renderPage()}</main>
      </div>
    </div>
  );
}
