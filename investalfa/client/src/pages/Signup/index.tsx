import styles from "./styles.module.scss";
import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { isExpired } from "react-jwt";
import { Spinner, Button } from "grommet";
import { AuthLayout } from "../../components/AuthLayout";
import api from "../../services/api";
import { AxiosError, AxiosResponse } from "axios";

export const Signup = () => {
  let navigate = useNavigate();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

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
      .post("/users/", {
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password,
      })
      .then(({ data }: AxiosResponse) => {
        navigate("/signin");
      })
      .catch((error: AxiosError) => {
        setIsLoading(false);
        setError(JSON.stringify(error.response?.data));
      });
  }

  return (
    <main className={styles.signin}>
      <AuthLayout>
        <form onSubmit={(e) => handleSubmit(e)}>
          <h1>Criar conta</h1>
          <input
            placeholder="Primeiro nome"
            type="text"
            className={error == "" ? "" : styles.error}
            disabled={isLoading}
            required
            value={firstName}
            onChange={(event) => {
              setError("");
              setFirstName(event.target.value);
            }}
          />
          <input
            placeholder="Sobrenome"
            type="text"
            className={error == "" ? "" : styles.error}
            disabled={isLoading}
            required
            value={lastName}
            onChange={(event) => {
              setError("");
              setLastName(event.target.value);
            }}
          />
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
          <div className={styles.swap}>
            <Link to="/signin">Entrar</Link>
          </div>
          <Button
            {...buttonProps}
            primary
            type="submit"
            label="Cadstrar"
            reverse
          />
        </form>
      </AuthLayout>
    </main>
  );
};
