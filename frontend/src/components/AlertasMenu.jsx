import { useEffect, useState } from "react";
import { api } from "../api";
import { Link } from "react-router-dom";

export default function AlertasMenu({ token }) {
  const [instrumentos, setInstrumentos] = useState([]);

  useEffect(() => {
    async function carregar() {
      try {
        const dados = await api.listarInstrumentos(token);
        setInstrumentos(dados.instrumentos || dados);
      } catch (err) {
        console.error(err);
      }
    }
    carregar();
  }, [token]);

  const vencidos = instrumentos.filter(i => i.status_calibracao === "vencido");
  const proximos = instrumentos.filter(i => i.status_calibracao === "proximo");

  const total = vencidos.length + proximos.length;

  return (
    <Link to="/alertas" style={{ color: "white", textDecoration: "none" }}>
      ⚠️ {total > 0 && <span className="badge">{total}</span>}
    </Link>
  );
}
