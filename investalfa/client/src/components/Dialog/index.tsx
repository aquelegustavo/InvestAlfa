import styles from "./styles.module.scss";
import { Button, Layer, TextInput, FormField } from "grommet";
import { Add, Trash } from "grommet-icons";
import { Dispatch, SetStateAction, useState } from "react";
import api from "../../services/api";
import { useUser } from "../../hooks/useUser";

type DialogProps = {
  companies: CompanyType[];
  details: string;
  monitoring: MonitoringType[];
  updateUi: () => void;
  show: boolean;
  setShow: Dispatch<SetStateAction<boolean>>;
};
type MonitoringType = {
  id: string;
  company: string;
  frequency: number;
  tunnel_min: number;
  tunnel_max: number;
};

type CompanyType = {
  name: string;
  code: string;
  last_quote: number;
  min_quote: number;
  max_quote: number;
};

export const Dialog = ({
  companies,
  details,
  monitoring,
  updateUi,
  show,
  setShow,
}: DialogProps) => {
  const user = useUser();

  let company = companies.filter((company) => company.code == details);

  let moni = monitoring.filter((moni) => moni.company == details);

  const isUpdate = moni.length > 0;

  const [freq, setFreq] = useState(isUpdate ? moni[0].frequency : "");
  const [min, setMin] = useState(isUpdate ? moni[0].tunnel_min : "");
  const [max, setMax] = useState(isUpdate ? moni[0].tunnel_max : "");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    api
      .request({
        url: `/users/${user?.uid}/monitoring/`,
        method: isUpdate ? "PUT" : "POST",
        data: {
          company: company[0].code,
          frequency: freq,
          tunnel_min: min,
          tunnel_max: max,
        },
      })
      .then(({ data }) => {
        updateUi();
      })
      .catch((error) => {
        alert("Erro ao salvar monitoramento");
      });

    setFreq("");
    setMin("");
    setMax("");
    setShow(false);
  }

  function deleteMonitoring(monitoringId: string) {
    api
      .delete(`/users/${user?.uid}/monitoring/${monitoringId}`)
      .then(({ data }) => {
        updateUi();
      })
      .catch((error) => {
        alert("Erro ao deletar monitoramento");
      });

    setFreq("");
    setMin("");
    setMax("");
    setShow(false);
  }

  return (
    <>
      {show && (
        <Layer
          className={styles.dialog}
          onEsc={() => setShow(false)}
          onClickOutside={() => setShow(false)}
        >
          <h4>Monitorar ativos da(o) {company[0].name}</h4>
          <form onSubmit={(e) => handleSubmit(e)}>
            <FormField label="Frequência (minutos)">
              <TextInput
                type="number"
                min="5"
                max="40"
                required
                value={freq}
                onChange={(event) => setFreq(event.target.value)}
              />
            </FormField>
            <FormField label="Túnel mínimo (BRL)">
              <TextInput
                type="number"
                required
                max={max}
                value={min}
                onChange={(event) => setMin(event.target.value)}
              />
            </FormField>

            <FormField label="Túnel máximo (BRL)">
              <TextInput
                type="number"
                required
                min={min}
                value={max}
                onChange={(event) => setMax(event.target.value)}
              />
            </FormField>
            {isUpdate ? (
              <Button
                label="Deletar"
                icon={<Trash />}
                onClick={() => deleteMonitoring(moni[0].id)}
              />
            ) : null}
            <div className={styles.action}>
              <Button label="Fechar" onClick={() => setShow(false)} />
              <Button primary label="Salvar" type="submit" />
            </div>
          </form>
        </Layer>
      )}
    </>
  );
};
