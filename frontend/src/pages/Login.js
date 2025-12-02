// src/pages/Login.js
import { useState } from "react";

export default function Login({ setToken, setUsuario }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function entrar(e) {
    e.preventDefault();

    try {
      const resp = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await resp.json();

      if (!resp.ok) {
        alert(data.detail || "Usuário ou senha inválidos");
        return;
      }

      // salva no estado e no localStorage para persistir entre reloads
      setToken(data.token);
      setUsuario(data.usuario);
      localStorage.setItem("token", data.token);
      localStorage.setItem("usuario", JSON.stringify(data.usuario));
    } catch (err) {
      console.error("Falha ao buscar", err);
      alert("Falha ao conectar com o servidor");
    }
  }

  return (
    <div className="login-background" style={{ backgroundImage: "url('/logo.png')" }}>
      <div className="login-box">
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
