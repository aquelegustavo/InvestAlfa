import styles from "./styles.module.scss";
import React, { useEffect, useState } from "react";
import { isExpired } from "react-jwt";
import { Layout } from "../../components/Layout";
import { Charts } from "../../components/Charts";
import api from "../../services/api";
import { useUser } from "../../hooks/useUser";
import { useNavigate } from "react-router-dom";
import { Button } from "grommet";
import { Add } from "grommet-icons";
import { Dialog } from "../../components/Dialog";

export const Dashboard = () => {
  const navigate = useNavigate();

  type CompanyType = {
    name: string;
    code: string;
    last_quote: number;
  };

  type MonitoringType = {
    company: string;
  };

  type UserType = {
    uid: string;
  } | null;

  const [monitoring, setMonitoring] = useState([] as MonitoringType[]);
  const [companies, setCompanies] = useState([] as CompanyType[]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chart, setChart] = useState("");
  const [show, setShow] = useState(false);

  const user: UserType = useUser();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token && !isExpired(token)) {
      navigate("/");
    }

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

    if (user) {
      api
        .get(`/users/${user.uid}/monitoring`)
        .then(({ data }) => {
          setMonitoring(data);
          setIsLoading(false);
        })
        .catch((error) => {
          setError(error);
          setIsLoading(false);
        });
    } else {
      navigate("/");
    }
  }

  let userMonitoring = monitoring.map((moni, index) => {
    let company = companies.filter((company) => company.code == moni.company);
    return company[0];
  });

  function handleLineClick(companyId: string) {
    setChart(companyId);
    navigate(`#${companyId}`, { replace: true });
  }

  return (
    <div className={styles.dashboard}>
      <Layout hero>
        {userMonitoring.length > 0 ? (
          <section>
            <h2 className={styles.title}>Suas empresas monitoradas</h2>
            <ul className={styles.companies}>
              {userMonitoring.map((company, index) => (
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
                  <div className={styles.details}>
                    {chart == company.code ? (
                      <Charts companyId={company.code} />
                    ) : null}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        ) : (
          <></>
        )}

        <section>
          <h2 className={styles.title}>Todas as empresas</h2>
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
                <div className={styles.details}>
                  {chart == company.code ? (
                    <>
                      <div>
                        <Button
                          primary
                          label="Monitorar"
                          icon={<Add />}
                          onClick={() => setShow(true)}
                        />
                      </div>
                      <Charts companyId={company.code} />
                    </>
                  ) : null}
                </div>
              </li>
            ))}
          </ul>
        </section>
      </Layout>
      <Dialog show={show} setShow={setShow} />
    </div>
  );
};
