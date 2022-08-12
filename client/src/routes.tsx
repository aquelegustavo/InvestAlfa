import { Routes, Route } from "react-router-dom";

import { Dashboard } from "./pages/Dashboard";
import { Signin } from "./pages/Signin";

type PageType = {
  title: string;
  to: string;
  component: JSX.Element;
};

export const pages: PageType[] = [
  { title: "Dashboard", to: "/", component: <Dashboard /> },
  { title: "Login", to: "/signin", component: <Signin /> },
];

export const AppRoutes = () => (
  <Routes>
    {pages.map((page) => (
      <Route key={page.component.key} path={page.to} element={page.component} />
    ))}
  </Routes>
);
