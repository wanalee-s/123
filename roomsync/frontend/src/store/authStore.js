import { defineStore } from "pinia";
import { getUser, saveToken, logout } from "@/services/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: getUser(),
  }),
  actions: {
    updateUser() {
      this.user = getUser();
    },
    login(token) {
      saveToken(token); // Saves to cookie
      this.updateUser();
    },
    logout() {
      logout();
      this.user = null;
    },
  },
});