import { useState, useEffect } from "react";
import { api } from "../api";

export default function RegistrarCalibracao({ token }) {
  const [instrumentos, setInstrumentos] = useState([]);
  const [instrumentoId, setInstrumentoId] = useState("");
  const [resultado, setResultado] = useState("");
  const [imagem, setImagem] = useState(null);
  const [preview, setPreview] = useState(null);

  useEffect(() => {
    async function carregarInstru() {
      try {
        const dados = await api.listarInstrumentos(token);
        setInstrumentos(dados.instrumentos || []);
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
      setInstrumentoId(""); setResultado(""); setImagem(null); setPreview(null);
    } catch (err) {
      console.error("Erro ao registrar:", err);
      alert("Erro ao registrar calibração");
    }
  }

  return (
    <div className="p-6 flex justify-center">
      <div className="w-full max-w-lg bg-white shadow-lg rounded p-6 border">
        <h2 className="text-2xl font-bold mb-6 text-center">Registrar Nova Calibração</h2>
        <form className="space-y-5" onSubmit={registrar}>
          <div>
            <label>Instrumento</label>
            <select value={instrumentoId} onChange={(e)=>setInstrumentoId(e.target.value)} required>
              <option value="">Selecione...</option>
              {instrumentos.map(i => <option key={i.id} value={i.id}>{i.nome || i.tipo || i.id}</option>)}
            </select>
          </div>

          <div>
            <label>Resultado</label>
            <select value={resultado} onChange={(e)=>setResultado(e.target.value)} required>
              <option value="">Selecione...</option>
              <option value="Aprovado">Aprovado</option>
              <option value="Reprovado">Reprovado</option>
            </select>
          </div>

          <div>
            <label>Comprovante (Imagem)</label>
            <input type="file" accept="image/*" onChange={handleImagem} />
            {preview && <img src={preview} alt="Preview" style={{width:120,height:120,objectFit:"cover",marginTop:8}} />}
          </div>

          <button type="submit">Registrar</button>
        </form>
      </div>
    </div>
  );
}
