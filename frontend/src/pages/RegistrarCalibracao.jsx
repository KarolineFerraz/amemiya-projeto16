// src/pages/RegistrarCalibracao.jsx
import { useState, useEffect } from "react";
import { api } from "../api";

export default function RegistrarCalibracao({ token }) {
  const [instrumentos, setInstrumentos] = useState([]);
  const [instrumentoId, setInstrumentoId] = useState("");
  const [resultado, setResultado] = useState("");
  const [imagem, setImagem] = useState(null);
  const [preview, setPreview] = useState(null);

  // Carregar instrumentos automaticamente
  useEffect(() => {
    async function carregarInstru() {
      try {
        const dados = await api.listarInstrumentos(token);
        setInstrumentos(dados.instrumentos || dados);
      } catch (err) {
        console.error("Erro ao carregar instrumentos:", err);
      }
    }
    carregarInstru();
  }, [token]);

  function handleImagem(e) {
    const file = e.target.files[0];
    setImagem(file);
    if (file) setPreview(URL.createObjectURL(file));
  }

  async function registrar(e) {
    e.preventDefault();

    try {
      const formData = new FormData();
      formData.append("instrumento_id", instrumentoId);
      formData.append("resultado", resultado);
      if (imagem) formData.append("imagem", imagem);

      await api.registrarCalibracao(token, formData);

      alert("Calibração registrada com sucesso!");
      setInstrumentoId("");
      setResultado("");
      setImagem(null);
      setPreview(null);
    } catch (err) {
      console.error("Erro ao registrar:", err);
      alert("Erro ao registrar calibração");
    }
  }

  return (
    <div className="p-6 flex justify-center">
      <div className="w-full max-w-lg bg-white shadow-lg rounded p-6 border">

        <h2 className="text-2xl font-bold mb-6 text-center">
          Registrar Nova Calibração
        </h2>

        <form className="space-y-5" onSubmit={registrar}>
          
          {/* Instrumento */}
          <div>
            <label className="block font-semibold mb-1">Instrumento</label>
            <select
              className="w-full border p-2 rounded"
              value={instrumentoId}
              onChange={(e) => setInstrumentoId(e.target.value)}
              required
            >
              <option value="">Selecione...</option>
              {instrumentos.map((i) => (
                <option key={i.id} value={i.id}>
                  {i.nome}
                </option>
              ))}
            </select>
          </div>

          {/* Resultado */}
          <div>
            <label className="block font-semibold mb-1">Resultado</label>
            <select
              className="w-full border p-2 rounded"
              value={resultado}
              onChange={(e) => setResultado(e.target.value)}
              required
            >
              <option value="">Selecione...</option>
              <option value="Aprovado">Aprovado</option>
              <option value="Reprovado">Reprovado</option>
            </select>
          </div>

          {/* Imagem */}
          <div>
            <label className="block font-semibold mb-1">
              Comprovante (Imagem)
            </label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImagem}
              className="border p-2 w-full rounded"
            />

            {preview && (
              <img
                src={preview}
                alt="Preview"
                className="w-40 h-40 object-cover mt-3 rounded border"
              />
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          >
            Registrar
          </button>
        </form>
      </div>
    </div>
  );
}
