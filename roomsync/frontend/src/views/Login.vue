<template>
  <div>
    <div v-if="!auth.user">
      <h2>Login with Google</h2>
      <button @click="googleLogin">Login</button>
    </div>
    <div v-if="auth.user">
      <h3>Welcome, {{ auth.user.name }}</h3>
      <p>Email: {{ auth.user.email }}</p>
      <button @click="auth.logout">Logout</button>
    </div>
  </div>
</template>
<script>
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle } from "@/services/auth";

export default {
  setup() {
    const auth = useAuthStore();

    function saveTokenFromUrl() {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get("token");
      if (token) {
        auth.login(token); // Saves to cookie
        window.history.replaceState({}, document.title, "/");
      }
    }

    saveTokenFromUrl();
    return { auth, googleLogin: loginWithGoogle };
  },
};
</script>