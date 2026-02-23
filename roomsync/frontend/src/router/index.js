import { createRouter, createWebHistory } from 'vue-router'

import AppLayout from '@/layouts/AppLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

import Dashboard from '@/components/Dashboard.vue'
import Calendar from '@/components/Calendar.vue'
import UserStatus from '@/components/UserStatus.vue'

const routes = [
  // USER AREA
  {
    path: '/user',
    component: AppLayout,
    children: [
      { path: '', name: 'Dashboard', component: Dashboard },
      { path: 'calendar', name: 'Calendar', component: Calendar },
      { path: 'myReservation', name: 'UserStatus', component: UserStatus },
    ],
  },

  // AUTH AREA
  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'Signin',
        component: () => import('@/views/Signin.vue'),
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
        component: () => import('@/views/Signup.vue'),
      },
    ],
  },
  {
    path: '/signup/form',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'SignupForm',
        component: () => import('@/views/formsignup.vue'),
      },
    ],
  },

  // ADMIN AREA
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/AdminDashboard.vue'),
      },
      {
        path: 'roleApprove',
        name: 'AdminRoleApprove',
        component: () => import('@/views/admin/AdminRoleApprove.vue'),
      },
      {
        path: 'roomManage',
        name: 'AdminRoomManage',
        component: () => import('@/views/admin/AdminRoomManage.vue'),
      }
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
