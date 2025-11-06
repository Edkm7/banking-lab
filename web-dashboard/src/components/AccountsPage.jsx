import { useEffect, useState } from "react";
import api from "../api/client";

export default function AccountsPage() {
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    api
      .get("/accounts")
      .then((res) => setAccounts(res.data))
      .catch((err) => console.error("Erreur chargement comptes:", err));
  }, []);

  if (accounts.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-gray-500">
        <p className="text-lg">Aucun compte disponible 😕</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-6">💰 Comptes clients</h2>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {accounts.map((a) => (
          <div
            key={a.id}
            className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 p-6 border border-gray-100"
          >
            <h3 className="text-xl font-semibold text-blue-700 mb-2">{a.name}</h3>
            <p className="text-gray-600 text-sm mb-4">Utilisateur ID : {a.user_id}</p>
            <p className="text-3xl font-bold text-gray-800">{a.balance} €</p>
            <p className="text-sm text-gray-400 mt-2">
              Créé le {new Date(a.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
