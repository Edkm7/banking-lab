export default function Header({ onLogout }) {
  return (
    <header className="flex justify-between items-center bg-white border-b shadow-sm px-8 py-4 sticky top-0 z-10">
      <h1 className="text-2xl font-bold text-blue-700 tracking-wide">
        Tableau de bord
      </h1>
      <button
        onClick={onLogout}
        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg shadow transition-all duration-150"
      >
        Déconnexion
      </button>
    </header>
  );
}
