import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:4010';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar auth token
apiClient.interceptors.request.use((config) => {
  // sessionStorage es más seguro que localStorage: no se envía con peticiones HTTP
  // y se borra automáticamente al cerrar el navegador. En desarrollo también lo
  // usamos por consistencia; en producción solo se guarda si VITE_API_URL es HTTPS.
  const token = sessionStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const onLoginPage = window.location.pathname === '/login'
      if (!onLoginPage) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error);
  }
);