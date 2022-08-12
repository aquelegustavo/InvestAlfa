import axios from "axios";

type Header = {
  Authorization: string;
};
function setHeaders() {
  let headers = {} as Header;
  const token = localStorage.getItem("token");

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return headers;
}

export const api = axios.create({
  baseURL: "/api",
  headers: setHeaders(),
});
