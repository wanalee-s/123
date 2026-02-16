import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../components/Dashboard.vue'; // Replace with your desired home component
import Calendar from '../components/Calendar.vue';
import UserStatus from "../components/UserStatus.vue";

const routes = [
  // { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/calendar', name: 'Calendar', component: Calendar },
  { path: "/myResevation", name: "UserStatus", component: UserStatus },
  { path: '/', name: 'Login', component: () => import('../views/Login.vue') },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;