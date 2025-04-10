import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // ← "backend" es el nombre del servicio en docker-compose
});



// Token automático si está logueado
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});


export default api;
