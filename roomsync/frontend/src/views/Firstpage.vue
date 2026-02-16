<template>
    <div class="min-h-screen flex flex-col items-center justify-center bg-base-200">
    <h1 class="text-6xl font-bold">
        Welcome to <span class="text-primary">RoomSync</span>
    </h1>
    <div class="mt-12">
        <router-link
        to="/login"
        class="flex flex-col items-center group">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-10 h-10 text-primary animate-bounce group-hover:animate-none transition">
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19.5 8.25 12 15.75 4.5 8.25"
            />
        </svg>
        <span class="mt-2 text-sm opacity-70 group-hover:opacity-100 transition">
            Get Started
        </span>
        </router-link>
    </div>
    </div>
</template>
