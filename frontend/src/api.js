// src/api.js

const BASE = "http://127.0.0.1:8000";

// --------------------------------------------------------------------
// Função genérica de requisições
// --------------------------------------------------------------------
async function request(path, options = {}) {
  const res = await fetch(BASE + path, options);

  // Se deu erro, tentamos extrair a mensagem detalhada
  if (!res.ok) {
    const text = await res.text();
    const err = new Error(text || `HTTP ${res.status}`);
    throw err;
  }

  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) {
    return res.json();
  }

  return res.text();
}

// --------------------------------------------------------------------
// Export das funções de API
// --------------------------------------------------------------------
export const api = {
  // -----------------------
  // LOGIN
  // -----------------------
  async login(username, password) {
    return request("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });
  },

  // -----------------------
  // LISTAR CALIBRAÇÕES
  // -----------------------
  async listarCalibracoes(token) {
    return request("/calibracoes/listar", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
      },
    });
  },

  // -----------------------
  // REGISTRAR CALIBRAÇÃO
  // -----------------------
  async registrarCalibracao(token, formData) {
    return request("/calibracoes/registrar", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token,
        // ⚠️ NÃO DEFINIR Content-Type AQUI
      },
      body: formData,
    });
  },

  // -----------------------
  // LISTAR INSTRUMENTOS
  // -----------------------
  async listarInstrumentos(token) {
    return request("/instrumentos/listar", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
      },
    });
  },

  // -----------------------
  // CRIAR INSTRUMENTO (somente admin)
  // -----------------------
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

  // -----------------------
  // DELETAR INSTRUMENTO
  // -----------------------
  async deletarInstrumento(token, id) {
    return request(`/instrumentos/deletar/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + token,
      },
    });
  },

  // -----------------------
  // LISTAR USUÁRIOS
  // -----------------------
  async listarUsuarios(token) {
    return request("/usuarios/listar", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
      },
    });
  },
};
