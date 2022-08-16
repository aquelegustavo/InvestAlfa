import { AxiosError, AxiosResponse } from "axios";
import { useState, useEffect } from "react";
import { decodeToken } from "react-jwt";
import api from "../services/api";

type User = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  last_login: Date | null;
  is_active: boolean;
  is_staff: boolean;
  date_joined: Date;
} | null;

type DecodedToken = {
  uid: string;
};

export function useUser() {
  const [user, setUser] = useState(null as User);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token && !user) {
      let decodedToken = decodeToken(token) as DecodedToken;
      api
        .get(`/users/${decodedToken["uid"]}/`)
        .then(({ data }: AxiosResponse) => {
          setUser(data);
        })
        .catch((error: AxiosError) => {
          console.error(error);
        });
    }
  }, []);

  return user;
}
