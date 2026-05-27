import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  timeout: 120000,
});

export async function getHealth() {
  const { data } = await api.get("/health");
  return data;
}

export async function getAtms() {
  const { data } = await api.get("/atms");
  return data;
}

export async function getAtmForecast(atmId) {
  const { data } = await api.get(`/atm/${atmId}/forecast`);
  return data;
}

export async function predictAtm(payload) {
  const { data } = await api.post("/predict", payload);
  return data;
}

export default api;
