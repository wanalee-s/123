<template>
    <div class="min-h-screen flex items-center justify-center bg-base-200">
        <div class="card w-96 bg-base-100 shadow-xl">
        <div class="card-body text-center">
            <h1 class="card-title justify-center">ยินดีต้อนรับสู่ RoomSync</h1>
            <h3 class="card-title justify-center"> Verify your identity</h3>
            <p>Please log in with your Google account to continue.</p>
            <div class="card-actions justify-center">
            <button @click="googleLogin" class="btn btn-primary">Login with Google</button>
            </div>

        </div>
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
        auth.login(token);
        window.history.replaceState({}, document.title, "/");
      }
    }

    saveTokenFromUrl();
    return { auth, googleLogin: loginWithGoogle };
  },
};
</script>
