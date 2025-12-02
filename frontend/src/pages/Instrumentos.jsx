// src/pages/Instrumentos.jsx
import { useEffect, useState } from "react";
import { api } from "../api";

export default function Instrumentos({ token }) {
  const [lista, setLista] = useState([]);
  const [tipo, setTipo] = useState("");

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
      await api.criarInstrumento(token, { tipo });
      setTipo("");
      carregar();
    } catch (err) {
      console.error("Erro ao criar instrumento:", err);
      alert("Erro ao criar instrumento.");
    }
  }

  async function deletar(id) {
    try {
      await api.deletarInstrumento(token, id);
      carregar();
    } catch (err) {
      console.error("Erro ao deletar:", err);
      alert("Erro ao excluir instrumento.");
    }
  }

  useEffect(() => {
    carregar();
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Instrumentos</h2>

      <form onSubmit={criar} className="space-y-4 mb-6">
        <input
          type="text"
          placeholder="Tipo do Instrumento"
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          className="border p-2 w-full"
        />

        <button className="bg-green-600 text-white px-4 py-2 rounded">
          Criar Instrumento
        </button>
      </form>

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-200">
            <th>ID</th>
            <th>Tipo</th>
            <th>Ação</th>
          </tr>
        </thead>

        <tbody>
          {lista.map((item) => (
            <tr key={item.id} className="border">
              <td>{item.id}</td>
              <td>{item.tipo}</td>
              <td>
                <button
                  onClick={() => deletar(item.id)}
                  className="bg-red-600 text-white px-2 py-1 rounded"
                >
                  Excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
}
