<template>
    <div class="navbar bg-base-100 shadow-sm text-content px-6">
        <div class="absolute left-1/2 -translate-x-1/2">
            <span class="btn btn-ghost text-xl">RoomSync</span>
        </div>
        <!-- <div class="navbar-end">
            <v-icon name="mdi-account" class="text-2xl"></v-icon>
        </div> -->
    </div>
    <div class="min-h-screen flex items-center justify-center bg-base-200">
        <router-view />
    </div>
</template>
