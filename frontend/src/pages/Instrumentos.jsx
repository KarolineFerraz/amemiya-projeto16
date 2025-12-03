import { useEffect, useState } from "react";
import { api } from "../api";

export default function Instrumentos({ token }) {
  const [lista, setLista] = useState([]);
  const [nome, setNome] = useState("");

  async function carregar() {
    try {
      const data = await api.listarInstrumentos(token);
      setLista(data.instrumentos || []);
    } catch (err) {
      console.error("Erro ao carregar instrumentos:", err);
    }
  }

  async function criar(e) {
    e.preventDefault();
    try {
      await api.criarInstrumento(token, { nome });
      setNome("");
      carregar();
    } catch (err) {
      console.error("Erro ao criar instrumento:", err);
      alert("Erro ao criar instrumento.");
    }
  }

  useEffect(()=> { carregar(); }, [token]);

  return (
    <div>
      <h2>Instrumentos</h2>
      <form onSubmit={criar}>
        <input value={nome} onChange={(e)=>setNome(e.target.value)} placeholder="Nome do instrumento" />
        <button>Criar Instrumento</button>
      </form>

      <table>
        <thead><tr><th>ID</th><th>Nome</th><th>Ação</th></tr></thead>
        <tbody>
          {lista.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.nome || item.tipo}</td>
              <td><button onClick={()=>api.deletarInstrumento(token, item.id).then(carregar).catch(()=>alert("Erro"))}>Excluir</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
