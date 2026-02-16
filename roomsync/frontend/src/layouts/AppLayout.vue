<template>
    <div class="min-h-screen bg-base-200">

    <div class="navbar bg-primary text-primary-content px-6">
        <div class="flex-1">
            <span class="text-xl font-bold">RoomSync</span>
        </div>
        <div class="flex-none gap-2">
            <router-link to="/" class="btn btn-ghost btn-sm">Dashboard</router-link>
            <router-link to="/calendar" class="btn btn-ghost btn-sm">Calendar</router-link>
        </div>
    </div>

        <div class="p-10">
        <router-view />
        </div>
    </div>
</template>

