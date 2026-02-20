<script setup>
import Sidebar from '@/components/admin/Sidebar.vue'
import router from '../router';
</script>

<template>
    <div class="drawer">

    <!-- toggle -->
    <input id="drawer" type="checkbox" class="drawer-toggle" />

    <!-- Content -->
    <div class="drawer-content flex flex-col">

        <!-- Navbar -->
        <div class="navbar bg-base-100 shadow-sm">
            <div class="navbar-start">
            <label for="drawer">
                <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" /> </svg>
                </div>
            </label>
            </div>

            <div class="navbar-center">
                <div class="absolute left-0 w-full text-center pointer-events-none">
                    <span class="text-xl font-bold">
                    <!-- Dynamic title based on route -->
                    <div v-if="router.currentRoute.value.name === 'AdminDashboard'">
                        Dashboard
                    </div>
                    <div v-else-if="router.currentRoute.value.name === 'AdminRoleApprove'">
                        Role Approvals
                    </div>
                    </span>
                </div>
            </div>
            <div class="navbar-end flex items-center gap-3 pr-5">
                <!-- Search Button -->
                <div>
                    <input type="text" placeholder="Search rooms or Booking" class="input input-bordered w-24 md:w-auto">
                </div>
                <!-- Notification Button -->
                <div class="">
                    <button class="btn btn-ghost btn-circle">
                        <div class="indicator">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /> </svg>
                            <span class="badge badge-xs badge-primary indicator-item"></span>
                        </div>
                    </button>
                </div>
                <!-- User Avatar -->
                <div class="dropdown dropdown-end">
                    <label tabindex="0" class="btn btn-ghost btn-circle avatar">
                        <div class="w-10 rounded-full">
                            <img src="https://placeimg.com/80/80/people" />
                        </div>
                    </label>
                    <ul tabindex="0" class="mt-3 p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
                        <li>
                            <a class="justify-between">
                                Profile
                                <span class="badge">New</span>
                            </a>
                        </li>
                        <li><a>Settings</a></li>
                        <li><a>Logout</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Page Content -->
        <div class="p-10">
            <router-view />
        </div>

        </div>

        <!-- Sidebar Component -->
        <Sidebar />

    </div>
</template>
