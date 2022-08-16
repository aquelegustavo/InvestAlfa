import styles from "./styles.module.scss";
import { Button, Layer, TextInput } from "grommet";
import { Add } from "grommet-icons";
import { useState } from "react";

export const Dialog = ({ show, setShow }: any) => {
  const [freq, setFreq] = useState("");
  const [min, setMin] = useState("");
  const [max, setMax] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

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
          <form onSubmit={(e) => handleSubmit(e)}>
            <TextInput
              placeholder="Frequência"
              value={freq}
              onChange={(event) => setFreq(event.target.value)}
            />
            <TextInput
              placeholder="Túnel mínimo"
              value={min}
              onChange={(event) => setMin(event.target.value)}
            />
            <TextInput
              placeholder="Túnel máximo"
              value={max}
              onChange={(event) => setMax(event.target.value)}
            />

            <div className={styles.action}>
              <Button label="Fechar" onClick={() => setShow(false)} />
              <Button primary label="Salvar" />
            </div>
          </form>
        </Layer>
      )}
    </>
  );
};
