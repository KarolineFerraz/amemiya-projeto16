// src/App.js
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";

import Login from "./pages/Login";
import ListarCalibracoes from "./pages/ListarCalibracoes";
import RegistrarCalibracao from "./pages/RegistrarCalibracao";
import Instrumentos from "./pages/Instrumentos";
import Usuarios from "./pages/Usuarios";
import Alertas from "./pages/Alertas";

import { api } from "./api";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [usuario, setUsuario] = useState(
    JSON.parse(localStorage.getItem("usuario") || "{}")
  );

  const [alertasTotal, setAlertasTotal] = useState(0);

  // Atualiza quantidade de alertas
  useEffect(() => {
    async function carregarAlertas() {
      if (!token) return;

      try {
        const dados = await api.listarInstrumentos(token);
        const lista = dados.instrumentos || dados;

        const vencidos = lista.filter((i) => i.status_calibracao === "vencido");
        const proximos = lista.filter(
          (i) => i.status_calibracao === "proximo"
        );

        setAlertasTotal(vencidos.length + proximos.length);
      } catch (err) {
        console.error("Erro ao atualizar alertas:", err);
      }
    }

    carregarAlertas();
  }, [token]);

  function sair() {
    setToken("");
    setUsuario({});
    setAlertasTotal(0);

    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
  }

  return (
    <BrowserRouter>
      {/* NAVBAR */}
      <nav className="navbar">

        {!token && <Link to="/">Login</Link>}

        {token && (
          <>
            <Link to="/listar">Calibrações</Link>
            <Link to="/registrar-calibracao" >Registrar Calibração
            </Link>
            <Link to="/instrumentos">Instrumentos</Link>

            <Link to="/alertas" className="alerta-menu-btn">
              ⚠️ Alertas
              {alertasTotal > 0 && (
                <span className="badge-alert">{alertasTotal}</span>
              )}
            </Link>

            {usuario.role === "gerente" && (
              <Link to="/usuarios">Usuários</Link>
            )}

            <button className="logout-btn" onClick={sair}>
              Sair
            </button>
          </>
        )}
      </nav>

      {/* ROTAS */}
      <div className="container">
        <Routes>
          <Route
            path="/"
            element={<Login setToken={setToken} setUsuario={setUsuario} />}
          />

          <Route path="/listar" element={<ListarCalibracoes token={token} />} />

          <Route
            path="/registrar-calibracao"
            element={<RegistrarCalibracao token={token} />}
          />

          <Route
            path="/instrumentos"
            element={<Instrumentos token={token} />}
          />

          <Route path="/alertas" element={<Alertas token={token} />} />

          <Route
            path="/usuarios"
            element={
              usuario.role === "gerente" ? (
                <Usuarios token={token} />
              ) : (
                <h2>Acesso negado.</h2>
              )
            }
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

const styles = {
  button: {
    padding: "6px 12px",
    background: "#0066ff",
    color: "white",
    borderRadius: "6px",
    textDecoration: "none",
  },
};

export default App;
