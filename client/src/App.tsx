import "./styles/global.scss";
import { BrowserRouter } from "react-router-dom";
import { AppRoutes } from "./routes";
import { Grommet } from "grommet";

const theme = {
  global: {
    colors: {
      brand: "#eeaeca",
    },
  },
};

function App() {
  return (
    <Grommet theme={theme}>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </Grommet>
  );
}

export default App;
