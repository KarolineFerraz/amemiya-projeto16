import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Login from "./pages/Login";
import ListarCalibracoes from "./pages/ListarCalibracoes";
import RegistrarCalibracao from "./pages/RegistrarCalibracao";
import Instrumentos from "./pages/Instrumentos";

export default function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (t) setToken(t);
  }, []);

  if (!token) return <Login setToken={setToken} />;

  return (
    <BrowserRouter>
      <div className="navbar">
        <Link to="/listar">Calibrações</Link>
        <Link to="/registrar">Registrar</Link>
        <Link to="/instrumentos">Instrumentos</Link>

        <button
          onClick={() => {
            localStorage.removeItem("token");
            setToken(null);
          }}
          style={{
            marginLeft: "auto",
            background: "transparent",
            border: "1px solid white",
            color: "white",
            padding: "5px 10px",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Sair
        </button>
      </div>

      <div className="container">
        <Routes>
          <Route path="/listar" element={<ListarCalibracoes token={token} />} />
          <Route path="/registrar" element={<RegistrarCalibracao token={token} />} />
          <Route path="/instrumentos" element={<Instrumentos token={token} />} />

          <Route path="*" element={<ListarCalibracoes token={token} />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
