import axios from "axios";
import VueCookies from "vue-cookies";
import { jwtDecode } from "jwt-decode";

const API_URL =
  import.meta.env.VITE_API_BASE_URL;

// Ensure Axios sends cookies with every request
axios.defaults.withCredentials = true;

// Axios interceptor to include X-CSRF-Token header
axios.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token && ["POST", "PUT", "DELETE"].includes(config.method.toUpperCase())) {
      const decoded = jwtDecode(token);
      config.headers["X-CSRF-Token"] = decoded.csrf_token; // Decode JWT for CSRF
    }
    // No Authorization header needed since JWT is in cookie
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Login with Google OAuth
export async function loginWithGoogle() {
  window.location.href = `${API_URL}/login`;
}
export async function loginWithGithub() {
  window.location.href = `${API_URL}/login/github`;
}
export async function loginWithEmail(email, password) {
  try {
    const response = await axios.post(`${API_URL}/login/email`, { email, password });
    return response.data; // Expecting { success: true } and JWT in cookie
  } catch (error) {
    console.error("Login error:", error);
    throw error;
  }
}

// Fetch Profile (JWT sent via cookie)
export async function getProfile() {
  try {
    const response = await axios.get(`${API_URL}/profile`);
    return response.data;
  } catch (error) {
    console.error("Auth error:", error);
    return null;
  }
}

// JWT Handling - Store & Retrieve Token in Cookies
export function getToken() {
  return VueCookies.get("jwt");
}

export function saveToken(token) {
  VueCookies.set("jwt", token, "1d", "/", "", false, "Lax"); // Non-HttpOnly cookie
}

export function removeToken() {
  VueCookies.remove("jwt");
}

// Decode JWT to Get User Info
export function getUser() {
  const token = VueCookies.get("jwt");
  if (token) {
    try {
      return jwtDecode(token); // Returns { sub, email, name, csrf_token, ... }
    } catch (error) {
      removeToken();
      return null;
    }
  }
  return null;
}

// Logout & Clear JWT
export function logout() {
  removeToken();
  window.location.reload(); // Optional
}