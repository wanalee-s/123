import { createRouter, createWebHistory } from 'vue-router'

import AppLayout from '@/layouts/AppLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

import Dashboard from '../components/Dashboard.vue'
import Calendar from '../components/Calendar.vue'
import UserStatus from '../components/UserStatus.vue'

const routes = [
  {
    path: '/user',
    component: AppLayout,
    children: [
      { path: '', name: 'Dashboard', component: Dashboard },
      { path: 'calendar', name: 'Calendar', component: Calendar },
      { path: 'myResevation', name: 'UserStatus', component: UserStatus },
    ],
  },
  //แยกหน้า login ออกมาเป็น layout ใหม่ เพื่อเปลี่ยนแปลง navbar
  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'firstpage',
        component: () => import('../views/Firstpage.vue'),
      },
    ],
  },
  {
    path: '/login',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'Login',
        component: () => import('../views/Login.vue'),
      }]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
