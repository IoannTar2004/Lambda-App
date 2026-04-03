import axios from "axios"
import humps from 'humps'

const api = axios.create({
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  }
});

api.interceptors.response.use(
  response => {

    if (response.data) {
      response.data = humps.camelizeKeys(response.data);
    }
    return response;
  },
  error => Promise.reject(error)
);

api.interceptors.request.use(
  config => {

    if (config.data instanceof FormData) {
      return config;
    }

    if (config.data) {
      config.data = humps.decamelizeKeys(config.data);
    }
    if (config.params) {
      config.params = humps.decamelizeKeys(config.params);
    }
    return config;
  },
  error => Promise.reject(error)
);

export const httpRequest = (method, url, payload={}, headers={}, asParams=false) => {
  const token = localStorage.getItem('accessToken')

  const config = {
    method: method,
    url: url,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...headers
    }
  }

  if (method === HTTPMethods.GET || asParams)
    config.params = payload
  else
    config.data = payload

  return api.request(config)
}

export const httpRequestFormData = (url, payload={}, headers={}) => {
  const token = localStorage.getItem('accessToken')
  const formData = new FormData()

  for (let key in payload) {
    const snakeKey = humps.decamelizeKeys({ [key]: null }); // преобразуем только ключ
    const actualKey = Object.keys(snakeKey)[0];
    formData.append(actualKey, payload[key]);
  }
  return api.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...headers
    }
  })
}

export const printError = (err) => {
  console.error(err.response)
}

export const HTTPMethods = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  PATCH: "PATCH",
  DELETE: "DELETE"
}