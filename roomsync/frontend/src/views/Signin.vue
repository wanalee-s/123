<template>
    <router-link to="/signup" class="btn btn-primary absolute top-3 right-4">
            Register
    </router-link>
    <div class="min-h-screen flex items-center justify-center bg-base-200">
        <div class="card w-120 bg-base-100 shadow-xl">
        <div class="card-body text-center">
            <h1 class="card-title text-3xl font-bold justify-center mt-5">Welcome back</h1>
            <p>Please log in with your Google or Github account to continue.</p>
            <div class="card-actions mt-6">
              <button class="btn w-full bg-white text-black border-[#e5e5e5] hover:bg-gray-100" @click="googleLogin">
                <svg aria-label="Google logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><g><path d="m0 0H512V512H0" fill="#fff"></path><path fill="#34a853" d="M153 292c30 82 118 95 171 60h62v48A192 192 0 0190 341"></path><path fill="#4285f4" d="m386 400a140 175 0 0053-179H260v74h102q-7 37-38 57"></path><path fill="#fbbc02" d="m90 341a208 200 0 010-171l63 49q-12 37 0 73"></path><path fill="#ea4335" d="m153 219c22-69 116-109 179-50l55-54c-78-75-230-72-297 55"></path></g></svg>
                Login with Google
              </button>
            </div>
            <div class="card-actions">
              <button class="btn w-full bg-black text-white border-black hover:bg-gray-800" @click="githubLogin">
                <svg aria-label="GitHub logo" width="16" height="16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="white" d="M12,2A10,10 0 0,0 2,12C2,16.42 4.87,20.17 8.84,21.5C9.34,21.58 9.5,21.27 9.5,21C9.5,20.77 9.5,20.14 9.5,19.31C6.73,19.91 6.14,17.97 6.14,17.97C5.68,16.81 5.03,16.5 5.03,16.5C4.12,15.88 5.1,15.9 5.1,15.9C6.1,15.97 6.63,16.93 6.63,16.93C7.5,18.45 8.97,18 9.54,17.76C9.63,17.11 9.89,16.67 10.17,16.42C7.95,16.17 5.62,15.31 5.62,11.5C5.62,10.39 6,9.5 6.65,8.79C6.55,8.54 6.2,7.5 6.75,6.15C6.75,6.15 7.59,5.88 9.5,7.17C10.29,6.95 11.15,6.84 12,6.84C12.85,6.84 13.71,6.95 14.5,7.17C16.41,5.88 17.25,6.15 17.25,6.15C17.8,7.5 17.45,8.54 17.35,8.79C18,9.5 18.38,10.39 18.38,11.5C18.38,15.32 16.04,16.16 13.81,16.41C14.17,16.72 14.5,17.33 14.5,18.26C14.5,19.6 14.5,20.68 14.5,21C14.5,21.27 14.66,21.59 15.17,21.5C19.14,20.16 22,16.42 22,12A10,10 0 0,0 12,2Z"></path></svg>
                Login with GitHub
              </button>
            </div>
            <div class="flex items-center my-6">
              <div class="flex-grow h-px bg-gray-300"></div>
              <div class="mx-4 text-gray-500">or</div>
              <div class="flex-grow h-px bg-gray-300"></div>
            </div>
            <div class="flex flex-col w-full gap-2">
              <label class="label">Email</label>
              <label class="input validator w-full flex items-center gap-2" for="email">
              <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <g
                  stroke-linejoin="round"
                  stroke-linecap="round"
                  stroke-width="2.5"
                  fill="none"
                  stroke="currentColor"
                >
                  <rect width="20" height="16" x="2" y="4" rx="2"></rect>
                  <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
                </g>
              </svg>
              <input type="email" placeholder="mail@site.com" required />
            </label>
            <div class="validator-hint hidden text-left mt-1">Required</div>
            </div>
            <div class="flex flex-col w-full gap-2">
              <label class="label">Password</label>
              <label class="input validator w-full flex items-center gap-2" for="password">
                <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <g
                    stroke-linejoin="round"
                    stroke-linecap="round"
                    stroke-width="2.5"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
                    ></path>
                    <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
                  </g>
                </svg>
                <input
                  type="password"
                  required
                  placeholder="Password"
                  minlength="8"
                  pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                  title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
                />
              </label>
              <p class="validator-hint hidden w-full text-left">
                Must be more than 8 characters, including
                <br />At least one number <br />At least one lowercase letter <br />At least one uppercase letter
              </p>
            </div>
              <div class="flex items-center mt-4 col-auto">
              <input type="checkbox" id="remember" class="mr-2" />
              <label for="remember" class="text-sm text-gray-600">Remember me</label>
            </div>
            <button class="btn btn-primary w-full mb-4 mt-4"> Sign In</button> <!-- #TODO: ตรวจสอบการล็อกอิน เมื่อตรงกับที่มีให้ไปหาถัดไป-->
            <div class="text-sm">
              Don't have an account?
              <router-link to="/signup" class="text-primary hover:underline">Sign up</router-link>
            </div>
        </div>
        </div>


    </div>
</template>

<script>
import { useAuthStore } from "@/store/authStore";
import { loginWithGoogle } from "@/services/auth";
import { loginWithGithub } from "@/services/auth";

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
    return { auth, googleLogin: loginWithGoogle, githubLogin: loginWithGithub };
  },
};
</script>
