import { useEffect, useState } from "react";
import api from "../api/client";

export default function ReportsPage() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    api.get("/reports/accounts")
      .then(res => {
        console.log("Type de res.data:", typeof res.data);
        console.log("Contenu de res.data:", res.data);
        setReports(res.data);
      })
      .catch(err => console.error("Erreur chargement rapports:", err));
  }, []);

  
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Rapports</h2>
      {reports.length === 0 ? (
        <p className="text-gray-500">Aucun rapport disponible.</p>
      ) : (
        <ul className="bg-white rounded shadow divide-y">
          {reports.map(r => (
            <li key={r.id} className="p-3 flex justify-between">
              <span>{r.name}</span> {/* ajusté pour correspondre à la structure réelle */}
              <span className="text-sm text-gray-500">{r.created_at}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
