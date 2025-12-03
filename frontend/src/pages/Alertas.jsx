// src/pages/Alertas.jsx
import { useEffect, useState } from "react";
import { api } from "../api";
import { Link } from "react-router-dom";

function diasEntre(dataStr) {
  if (!dataStr) return null;
  const d = new Date(dataStr);
  if (isNaN(d)) return null;
  const hoje = new Date();
  const hojeData = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
  return Math.ceil((d - hojeData) / (1000 * 60 * 60 * 24));
}

function formatDate(dataStr) {
  if (!dataStr) return "-";
  const d = new Date(dataStr);
  if (isNaN(d)) return "-";
  return d.toLocaleDateString();
}

export default function Alertas({ token }) {
  const [instrumentos, setInstrumentos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function carregar() {
      setLoading(true);
      try {
        const dados = await api.listarInstrumentos(token);
        const arr = (dados?.instrumentos) ? dados.instrumentos : (Array.isArray(dados) ? dados : []);
        setInstrumentos(arr || []);
      } catch (err) {
        console.error("Erro ao carregar instrumentos:", err);
        setInstrumentos([]);
      } finally {
        setLoading(false);
      }
    }
    carregar();
  }, [token]);

  const items = instrumentos.map((i) => {
    const prox =
      i?.proxima_calibracao ??
      i?.proxima ??
      i?.prox ??
      null;

    const dias = diasEntre(prox);
    let status = "ok";
    if (dias === null) status = "ok";
    else if (dias <= 0) status = "vencido";
    else if (dias <= 30) status = "proximo";

    return { ...i, prox, dias, status };
  });

  const ordemStatus = { vencido: 0, proximo: 1, ok: 2 };
  const itemsOrdenados = [...items].sort((a, b) => {
    const s = ordemStatus[a.status] - ordemStatus[b.status];
    if (s !== 0) return s;
    return (a.dias ?? 99999) - (b.dias ?? 99999);
  });

  const vencidos = itemsOrdenados.filter(i => i.status === "vencido");
  const proximos = itemsOrdenados.filter(i => i.status === "proximo");
  const ok = itemsOrdenados.filter(i => i.status === "ok");

  return (
    <div>
      <h2>Alertas de Calibração</h2>

      <p style={{ marginBottom: 12 }}>
        <strong>Total:</strong> {instrumentos.length} —{" "}
        <span className="badge" style={{ background: "#cc0000", marginRight: 6 }}>
          Vencidos: {vencidos.length}
        </span>
        <span className="badge" style={{ background: "#d98c00", marginRight: 6 }}>
          Próximos (30d): {proximos.length}
        </span>
        <span className="badge" style={{ background: "#067a00" }}>
          OK: {ok.length}
        </span>
      </p>

      {loading && <p>Carregando alertas...</p>}

      <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fill,minmax(260px,1fr))" }}>
        {itemsOrdenados.map((it) => (
          <div
            key={it.id}
            className={`alerta-card ${
              it.status === "vencido"
                ? "alerta-vencido"
                : it.status === "proximo"
                ? "alerta-proximo"
                : "alerta-ok"
            }`}
            style={{ padding: 12 }}
          >
            <div style={{ marginBottom: 8 }}>
              <span
                className={`status-text ${
                  it.status === "vencido"
                    ? "status-vencido"
                    : it.status === "proximo"
                    ? "status-proximo"
                    : "status-ok"
                }`}
                style={{ textTransform: "uppercase" }}
              >
                {it.status === "vencido"
                  ? "VENCIDO"
                  : it.status === "proximo"
                  ? "PRÓXIMO"
                  : "OK"}
              </span>
            </div>

            <div style={{ fontSize: 14 }}>
              <div><strong>ID:</strong> {it.id}</div>
              <div><strong>Próx. saída:</strong> {formatDate(it.prox)}</div>
              <div><strong>Dias restantes:</strong> {it.dias ?? "-"}</div>
            </div>

            <div style={{ marginTop: 10 }}>
              <Link to="/instrumentos" state={{ focoId: it.id }}>
                <button
                  style={{
                    padding: "6px 10px",
                    background: "#3a3a3a",
                    color: "#fff",
                    border: "none",
                    borderRadius: 6,
                  }}
                >
                  Instrumento
                </button>
              </Link>
            </div>
          </div>
        ))}
      </div>

      {!loading && itemsOrdenados.length === 0 && (
        <p>Nenhum instrumento encontrado.</p>
      )}
    </div>
  );
}
