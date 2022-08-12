import styles from "./styles.module.scss";

type AuthLayoutProps = {
  children: JSX.Element;
};

export const AuthLayout = ({ children }: AuthLayoutProps) => {
  return (
    <main className={styles.layout}>
      <section>{children}</section>
    </main>
  );
};
