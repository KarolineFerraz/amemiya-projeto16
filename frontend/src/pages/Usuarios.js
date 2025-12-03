import { useEffect, useState } from "react";
import { api } from "../api";

export default function Usuarios({ token }) {
  const [usuarios, setUsuarios] = useState([]);
  const [novoUsername, setNovoUsername] = useState("");
  const [novaSenha, setNovaSenha] = useState("");
  const [novaRole, setNovaRole] = useState("funcionario");

  async function carregar() {
    try {
      const data = await api.listarUsuarios(token);
      setUsuarios(data.usuarios || []);
    } catch (err) {
      console.error(err);
      alert("Erro ao carregar usuários.");
    }
  }

  useEffect(()=>{ carregar(); }, [token]);

  async function criarUsuario(e) {
    e.preventDefault();
    try {
      await api.criarUsuario(token, { username: novoUsername, password: novaSenha, role: novaRole });
      alert("Usuário criado!");
      setNovoUsername(""); setNovaSenha(""); setNovaRole("funcionario");
      carregar();
    } catch (err) {
      console.error(err);
      alert("Erro ao criar usuário.");
    }
  }

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

  return (
    <div>
      <h2>Gerenciar Usuários</h2>
      <form onSubmit={criarUsuario}>
        <input value={novoUsername} onChange={(e)=>setNovoUsername(e.target.value)} placeholder="Novo usuário" />
        <input value={novaSenha} onChange={(e)=>setNovaSenha(e.target.value)} placeholder="Senha" />
        <select value={novaRole} onChange={(e)=>setNovaRole(e.target.value)}>
          <option value="funcionario">Funcionário</option>
          <option value="gerente">Gerente</option>
        </select>
        <button>Criar</button>
      </form>

      <table>
        <thead><tr><th>Usuário</th><th>Cargo</th><th>Ações</th></tr></thead>
        <tbody>
          {usuarios.map(u => (
            <tr key={u.id}>
              <td>{u.username}</td>
              <td>{u.role}</td>
              <td><button onClick={()=>deletar(u.id)}>Excluir</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
