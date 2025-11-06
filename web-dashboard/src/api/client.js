import axios from "axios";

// Base URL "/" pour que Nginx fasse le proxy vers les services backend
const api = axios.create({
  baseURL: "/", 
});

// Ajouter le token JWT à chaque requête si présent
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
