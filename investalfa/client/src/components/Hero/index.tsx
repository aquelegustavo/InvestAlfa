import Wave from "react-wavify";
import { useUser } from "../../hooks/useUser";
import styles from "./styles.module.scss";

export const Hero = () => {
  const user = useUser();

  return (
    <div className={styles.hero}>
      <Wave
        className={styles.wave}
        fill="#efefef"
        paused={false}
        options={{
          height: 0.2,
          amplitude: 40,
          speed: 0.1,
          points: 7,
        }}
      />
      <div className={styles.hello}></div>
    </div>
  );
};
