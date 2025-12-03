// src/api.js
const BASE = "http://127.0.0.1:8000"; // ou "https://amemiya-backend-karol.onrender.com"

async function request(path, options = {}) {
  const res = await fetch(BASE + path, options);

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }

  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return res.json();
  return res.text();
}

export const api = {
  // LOGIN
  async login(username, password) {
    return request("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
  },

  // INSTRUMENTOS
  async listarInstrumentos(token) {
    return request("/instrumentos/listar", {
      method: "GET",
      headers: { Authorization: "Bearer " + token },
    });
  },

  async criarInstrumento(token, dados) {
    return request("/instrumentos/criar", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });
  },

  async deletarInstrumento(token, id) {
    return request(`/instrumentos/deletar/${id}`, {
      method: "DELETE",
      headers: { Authorization: "Bearer " + token },
    });
  },

  // CALIBRAÇÕES
  async listarCalibracoes(token) {
    return request("/calibracoes/listar", {
      method: "GET",
      headers: { Authorization: "Bearer " + token },
    });
  },

  async registrarCalibracao(token, formData) {
    // Não definir Content-Type quando mandar FormData
    return request("/calibracoes/registrar", {
      method: "POST",
      headers: { Authorization: "Bearer " + token },
      body: formData,
    });
  },

  // USUÁRIOS
  async listarUsuarios(token) {
    return request("/usuarios/listar", {
      method: "GET",
      headers: { Authorization: "Bearer " + token },
    });
  },

  async criarUsuario(token, dados) {
    return request("/usuarios/criar", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });
  },

  async deletarUsuario(token, id) {
    return request(`/usuarios/deletar/${id}`, {
      method: "DELETE",
      headers: { Authorization: "Bearer " + token },
    });
  },
};
