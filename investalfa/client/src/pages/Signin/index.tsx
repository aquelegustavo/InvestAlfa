import styles from "./signin.module.scss";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { isExpired } from "react-jwt";
import { Spinner, Button } from "grommet";
import { AuthLayout } from "../../components/AuthLayout";
import api from "../../services/api";
import { AxiosError, AxiosResponse } from "axios";

export const Signin = () => {
  let navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token && !isExpired(token)) {
      navigate("/");
    }
  }, []);

  let buttonProps = {};

  if (isLoading) {
    buttonProps = {
      icon: <Spinner size="xsmall" />,
      reverse: true,
      disabled: true,
    };
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    api
      .post("/auth/token/", {
        username: email,
        password: password,
      })
      .then(({ data }: AxiosResponse) => {
        setIsLoading(false);
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        navigate("/");
      })
      .catch((error: AxiosError) => {
        setIsLoading(false);
        setError("Usuário ou senhas incorretos.");
        console.error(error);
      });
  }

  return (
    <main className={styles.signin}>
      <AuthLayout>
        <form onSubmit={(e) => handleSubmit(e)}>
          <h1>Bem vindo de volta!</h1>
          <input
            placeholder="Email"
            type="email"
            className={error == "" ? "" : styles.error}
            disabled={isLoading}
            required
            value={email}
            onChange={(event) => {
              setError("");
              setEmail(event.target.value);
            }}
          />
          <input
            placeholder="Senha"
            type="password"
            className={error == "" ? "" : styles.error}
            disabled={isLoading}
            required
            value={password}
            onChange={(event) => {
              setError("");
              setPassword(event.target.value);
            }}
          />
          <p className={styles.errorLabel}>{error}</p>
          <Button
            {...buttonProps}
            primary
            type="submit"
            label="Entrar"
            reverse
          />
        </form>
      </AuthLayout>
    </main>
  );
};
