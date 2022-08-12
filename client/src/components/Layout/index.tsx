import { Header } from "../Header";
import { Hero } from "../Hero";
import styles from "./styles.module.scss";

type LayoutProps = {
  children: JSX.Element | JSX.Element[];
  hero?: boolean;
};

export const Layout = ({ children, hero }: LayoutProps) => {
  return (
    <>
      <Header />
      {hero ? <Hero /> : null}
      <main className={styles.layout}>{children}</main>
    </>
  );
};
