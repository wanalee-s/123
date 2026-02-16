<template>
    <!-- <div class="navbar bg-primary text-primary-content px-6">
        <div class="flex-1">
            <span class="text-xl font-bold">RoomSync</span>
        </div>
        <div class="flex-none gap-2">
            <router-link to="/" class="btn btn-ghost btn-sm">login</router-link>
        </div>
    </div> -->
    <div class="min-h-screen flex items-center justify-center bg-base-200">
        <router-view />
    </div>
    <!-- เปลี่ยน ธีม-->
    <div class="absolute top-4 right-10"> <!-- บนขวา-->
        <label className="flex cursor-pointer gap-2">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round">
            <circle cx="12" cy="12" r="5" />
            <path
            d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
        </svg>
        <input type="checkbox" value="synthwave" className="toggle theme-controller" />
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
        </label>
    </div>
</template>
