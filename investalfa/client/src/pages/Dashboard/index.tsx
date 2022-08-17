import styles from "./styles.module.scss";
import React, { useEffect, useState } from "react";
import { isExpired } from "react-jwt";
import { Layout } from "../../components/Layout";
import { Charts } from "../../components/Charts";
import api from "../../services/api";
import { useUser } from "../../hooks/useUser";
import { useNavigate } from "react-router-dom";
import { Button, Spinner } from "grommet";
import { Add } from "grommet-icons";
import { Dialog } from "../../components/Dialog";

export const Dashboard = () => {
  const navigate = useNavigate();

  type CompanyType = {
    name: string;
    code: string;
    last_quote: number;
    min_quote: number;
    max_quote: number;
  };

  type MonitoringType = {
    id: string;
    company: string;
    frequency: number;
    tunnel_min: number;
    tunnel_max: number;
  };

  type UserType = {
    uid: string;
  } | null;

  const [monitoring, setMonitoring] = useState([] as MonitoringType[]);
  const [companies, setCompanies] = useState([] as CompanyType[]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(0);
  const [details, setDetails] = useState("");
  const [show, setShow] = useState(false);

  const user: UserType = useUser();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token || isExpired(token)) {
      navigate("/sigin");
    }

    updateUi();
  }, [user]);

  function updateUi() {
    setLoading(0);

    api
      .get("/companies/")
      .then(({ data }) => {
        setCompanies(data);
        setLoading((loading) => loading + 1);
      })
      .catch((error) => {
        setError(error);
        setLoading((loading) => loading + 1);
      });

    if (user) {
      api
        .get(`/users/${user.uid}/monitoring`)
        .then(({ data }) => {
          setMonitoring(data);
          setLoading((loading) => loading + 1);
        })
        .catch((error) => {
          setError(error);
          setLoading((loading) => loading + 1);
        });
    }
    console.log("user", user);
  }

  let userMonitoring = monitoring.map((moni, index) => {
    let company = companies.filter((company) => company.code == moni.company);
    return company[0];
  });

  console.log(userMonitoring);
  console.log("loading", loading);

  function handleLineClick(companyId: string) {
    if (details == companyId) {
      setDetails("");
    } else {
      setDetails(companyId);
    }

    navigate(`#${companyId}`, { replace: true });
  }

  if (loading < 2) {
    return (
      <div className={styles.loading}>
        <Spinner size="medium" />
      </div>
    );
  } else {
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
                    className={details == company.code ? styles.active : ""}
                    id={company.code}
                  >
                    <div
                      className={styles.content}
                      onClick={(e) => handleLineClick(company.code)}
                    >
                      <h3>{company.name}</h3>
                      <p>{company.code}</p>
                      <p>{company.last_quote} BRL</p>
                    </div>
                    {details == company.code ? (
                      <div className={styles.details}>
                        <div className={styles.chart}>
                          <Charts companyId={company.code} />
                        </div>
                        <div className={styles.info}>
                          <div>
                            <p>Monitorando</p>
                          </div>
                        </div>
                      </div>
                    ) : null}
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
                  className={details == company.code ? styles.active : ""}
                  id={company.code}
                >
                  <div
                    className={styles.content}
                    onClick={(e) => handleLineClick(company.code)}
                  >
                    <h3>{company.name}</h3>
                    <p>{company.code}</p>
                    <p>{company.last_quote} BRL</p>
                  </div>

                  {details == company.code ? (
                    <div className={styles.details}>
                      <div className={styles.chart}>
                        <Charts companyId={company.code} />
                      </div>
                      <div className={styles.info}>
                        <Button
                          primary
                          label="Monitorar"
                          icon={<Add />}
                          onClick={() => setShow(true)}
                        />
                        <div>
                          <p>
                            Menor cotação (última semana): {company.min_quote}
                            BRL
                          </p>
                          <p>
                            Maior cotação (última semana): {company.min_quote}
                            BRL
                          </p>
                        </div>
                      </div>
                    </div>
                  ) : null}
                </li>
              ))}
            </ul>
          </section>
        </Layout>
        <Dialog
          companies={companies}
          details={details}
          monitoring={monitoring}
          updateUi={updateUi}
          show={show}
          setShow={setShow}
        />
      </div>
    );
  }
};
