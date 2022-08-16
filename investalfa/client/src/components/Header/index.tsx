import styles from "./styles.module.scss";

export const Header = () => {
  return (
    <div>
      <header className={styles.header}>
        <h1>IvestAlfa</h1>
        <div className={styles.divider}></div>
        <div className={styles.profile}>
          <img src="https://cataas.com/cat?size=200" />
        </div>
      </header>
    </div>
  );
};
