import styles from "./styles.module.scss";
import React, { useEffect, useState } from "react";
import { Layout } from "../../components/Layout";
import { Charts } from "../../components/Charts";
import api from "../../services/api";
import { useNavigate } from "react-router-dom";

export const Dashboard = () => {
  const navigate = useNavigate();

  type Company = {
    name: string;
    code: string;
    last_quote: number;
  };

  const [companies, setCompanies] = useState([] as Company[]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chart, setChart] = useState("");

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

  function handleLineClick(companyId: string) {
    setChart(companyId);
    navigate(`#${companyId}`, { replace: true });
  }

  return (
    <div className={styles.dashboard}>
      <Layout hero>
        <ul className={styles.companies}>
          {companies.map((company, index) => (
            <li
              key={index}
              className={chart == company.code ? styles.active : ""}
              onClick={(e) => handleLineClick(company.code)}
              id={company.code}
            >
              <div className={styles.content}>
                <h3>{company.name}</h3>
                <p>{company.code}</p>
                <p>{company.last_quote} BRL</p>
              </div>
              <div className={styles.chart}>
                {chart == company.code ? (
                  <Charts companyId={company.code} />
                ) : null}
              </div>
            </li>
          ))}
        </ul>
      </Layout>
    </div>
  );
};
