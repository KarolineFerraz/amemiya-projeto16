import { useEffect, useState } from "react";
import { api } from "../api";

export default function ListarCalibracoes({ token }) {
  const [lista, setLista] = useState([]);

  useEffect(() => {
    async function carregar() {
      try {
        const r = await api.listarCalibracoes(token);
        setLista(r.calibracoes);
      } catch (err) {
        console.error("Erro ao carregar:", err);
      }
    }
    carregar();
  }, [token]);

  return (
    <div>
      <h1>Calibrações Registradas</h1>

      {lista.map((c) => (
        <div key={c.id} className="card">
          <p><b>ID:</b> {c.id}</p>
          <p><b>Instrumento:</b> {c.instrumento_id}</p>
          <p><b>Usuário:</b> {c.usuario_id}</p>

          <p>
            <b>Resultado:</b>
            <span className={c.resultado === "Aprovado" ? "resultado-aprovado" : "resultado-reprovado"}>
              {" "}{c.resultado}
            </span>
          </p>

          {c.imagem_url && (
            <img src={c.imagem_url} alt="Imagem da calibração" />
          )}

          <p><b>Criado em:</b> {new Date(c.created_at).toLocaleString()}</p>
        </div>
      ))}
    </div>
  );
}
