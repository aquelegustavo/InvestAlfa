import axios, {
  AxiosError,
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
} from "axios";
import { isExpired } from "react-jwt";

const onRequest = async (config: AxiosRequestConfig) => {
  let accessToken = localStorage.getItem("access_token");
  console.log(config);
  if (config.url?.includes("/auth")) {
    return config;
  }

  if (isExpired(accessToken as string)) {
    accessToken = await reloadTokens();
  }
  if (config.headers) {
    config.headers["Authorization"] = `Bearer ${accessToken}`;
  }

  return config;
};

const onRequestError = (error: AxiosError): Promise<AxiosError> => {
  return Promise.reject(error);
};

const reloadTokens = async () => {
  const refreshToken = localStorage.getItem("refresh_token");

  try {
    const response = await axios.post(`/api/auth/token/refresh/`, {
      refresh: refreshToken,
    });

    const { access, refresh } = response.data;

    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);

    return access;
  } catch (_error) {
    return Promise.reject(_error);
  }
};

export const setupInterceptorsTo = (
  axiosInstance: AxiosInstance
): AxiosInstance => {
  axiosInstance.interceptors.request.use(onRequest, onRequestError);
  return axiosInstance;
};

const api = setupInterceptorsTo(
  axios.create({
    baseURL: "/api",
    headers: {
      "Content-Type": "application/json",
    },
  })
);

export default api;
