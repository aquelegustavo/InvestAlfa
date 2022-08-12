import styles from "./styles.module.scss";

import { useEffect, useState } from "react";
import { Layout } from "../../components/Layout";
import api from "../../services/api";

export const Dashboard = () => {
  type Company = {
    name: string;
    code: string;
    last_quote: number;
  };

  const [companies, setCompanies] = useState([] as Company[]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    updateUi();
  }, []);

  function updateUi() {
    setIsLoading(true);

    api
      .get("/companies/")
      .then(({ data }) => {
        setCompanies(data);
        setIsLoading(false);
      })
      .catch((error) => {
        setError(error);
        setIsLoading(false);
      });
  }
  return (
    <div className={styles.dashboard}>
      <Layout hero>
        <ul className={styles.companies}>
          {companies.map((company, index) => (
            <li key={index}>
              <h3>{company.name}</h3>
              <p>{company.code}</p>
              <p>{company.last_quote} BRL</p>
            </li>
          ))}
        </ul>
      </Layout>
    </div>
  );
};
