// src/pages/GerenciarUsuarios.js
import { useEffect, useState } from "react";
import { api } from "../api";

export default function GerenciarUsuarios({ token, usuario }) {
  const [usuarios, setUsuarios] = useState([]);
  const [novoUsername, setNovoUsername] = useState("");
  const [novaSenha, setNovaSenha] = useState("");
  const [novaRole, setNovaRole] = useState("funcionario");

  // ---- CARREGAR USUÁRIOS ----
  async function carregar() {
    try {
      const data = await api.listarUsuarios(token);
      setUsuarios(data.usuarios);
    } catch (err) {
      console.error(err);
      alert("Erro ao carregar usuários.");
    }
  }

  useEffect(() => {
    carregar();
  }, []);

  // ---- CRIAR USUÁRIO ----
  async function criarUsuario(e) {
    e.preventDefault();

    try {
      await api.criarUsuario(token, {
        username: novoUsername,
        password: novaSenha,
        role: novaRole,
      });

      alert("Usuário criado!");
      carregar();

      setNovoUsername("");
      setNovaSenha("");
      setNovaRole("funcionario");

    } catch (err) {
      console.error(err);
      alert("Erro ao criar usuário.");
    }
  }

  // ---- DELETAR USUÁRIO ----
  async function deletar(id) {
    if (!window.confirm("Deseja excluir?")) return;

    try {
      await api.deletarUsuario(token, id);
      carregar();
    } catch (err) {
      console.error(err);
      alert("Erro ao excluir usuário.");
    }
  }

  // ---- BLOQUEAR TÉCNICOS ----
  if (usuario?.role !== "gerente") {
    return <p>Apenas o gerente pode gerenciar usuários.</p>;
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Gerenciar Usuários</h2>

      {/* FORM DE CRIAÇÃO */}
      <form onSubmit={criarUsuario} className="space-y-3 mb-6">
        <input
          type="text"
          placeholder="Novo usuário"
          value={novoUsername}
          onChange={(e) => setNovoUsername(e.target.value)}
          className="border p-2 w-full"
        />

        <input
          type="password"
          placeholder="Senha"
          value={novaSenha}
          onChange={(e) => setNovaSenha(e.target.value)}
          className="border p-2 w-full"
        />

        <select
          value={novaRole}
          onChange={(e) => setNovaRole(e.target.value)}
          className="border p-2 w-full"
        >
          <option value="funcionario">Funcionário</option>
          <option value="gerente">Gerente</option>
        </select>

        <button className="bg-blue-600 text-white px-4 py-2 rounded w-full">
          Criar usuário
        </button>
      </form>

      {/* LISTA DE USUÁRIOS */}
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Usuário</th>
            <th className="p-2 border">Cargo</th>
            <th className="p-2 border">Ações</th>
          </tr>
        </thead>

        <tbody>
          {usuarios.map((u) => (
            <tr key={u.id}>
              <td className="p-2 border">{u.username}</td>
              <td className="p-2 border">{u.role}</td>
              <td className="p-2 border text-center">
                <button
                  className="bg-red-600 text-white px-3 py-1 rounded"
                  onClick={() => deletar(u.id)}
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
