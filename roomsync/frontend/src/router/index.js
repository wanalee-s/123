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
        name: 'Signin',
        component: () => import('../views/Signin.vue'),
      },
    ],
  },
  {
    path: '/signup',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'Signup',
        component: () => import('../views/Signup.vue'),
      }]
  },
  {
    path: '/admin/Dashboard',
    component: () => import('../views/AdminDashboardView.vue'), // สร้าง layout ใหม่สำหรับ admin
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('../views/AdminDashboardView.vue'),
      }]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
