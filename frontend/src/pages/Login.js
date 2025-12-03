import { useState } from "react";
import { api } from "../api";

export default function Login({ setToken, setUsuario }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function entrar(e) {
    e.preventDefault();

    try {
      const data = await api.login(username, password);

      if (!data.token) {
        alert("Usuário ou senha inválidos");
        return;
      }

      // Salva token e usuário
      localStorage.setItem("token", data.token);
      localStorage.setItem("usuario", JSON.stringify(data.usuario));

      setToken(data.token);
      setUsuario(data.usuario);

    } catch (err) {
      console.error(err);
      alert("Erro ao conectar ao servidor");
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">

        {/* Logo */}
        <img src="/logo.png" alt="Logo" className="login-logo" />

        <h2>Sistema de Calibrações</h2>

        <form onSubmit={entrar}>
          <input
            type="text"
            placeholder="Usuário"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Entrar</button>
        </form>

      </div>
    </div>
  );
}
