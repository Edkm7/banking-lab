export default function Sidebar({ active, onSelect }) {
  const items = [
    { id: "users", label: "👤 Utilisateurs" },
    { id: "accounts", label: "💰 Comptes" },
    { id: "reports", label: "📊 Rapports" }
  ];

  return (
    <aside className="w-64 h-screen bg-gradient-to-b from-blue-700 to-blue-900 text-white flex flex-col shadow-xl">
      <div className="p-6 border-b border-blue-600">
        <h2 className="text-2xl font-bold tracking-wide text-center">🏦 Banking Admin</h2>
      </div>

      <ul className="flex-1 p-4 space-y-2">
        {items.map((item) => (
          <li key={item.id}>
            <button
              onClick={() => onSelect(item.id)}
              className={`w-full text-left px-4 py-2 rounded-lg transition-all duration-200 ${
                active === item.id
                  ? "bg-white text-blue-700 font-semibold shadow-sm"
                  : "hover:bg-blue-800 text-gray-100"
              }`}
            >
              {item.label}
            </button>
          </li>
        ))}
      </ul>

      <div className="p-4 text-xs text-center text-gray-300 border-t border-blue-600">
        © {new Date().getFullYear()} Banking Dashboard
      </div>
    </aside>
  );
}
