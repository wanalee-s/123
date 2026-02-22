<template>
    <!-- Room Status Overview-->
        <div class="grid grid-cols-4 gap-6 mt-10">
            <div class="col-span-3">
                <h1 class="text-3xl font-bold">Room Status Overview</h1>
                <div class="flex flex-wrap gap-6">
                    <div
                        v-for="status in statuses"
                        :key="status.label"
                        class="flex items-center gap-2"
                    >
                        <div :class="`status ${status.color}`"></div>
                        <span class="text-sm text-gray-500">
                            {{ status.label }} ({{ status.count || 0 }})
                        </span>
                        </div>
                </div>
            </div>
            <div class="col-span-1 flex justify-end items-center">
                <button class="btn btn-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                    Register New Item
                </button>
            </div>
        </div>
        <roomcard />
</template>
<script setup>
import { computed } from 'vue'
import roomcard from './roomcard.vue'
const availableRooms = 5
const bookedRooms = 3
const maintenanceRooms = 2
const reservedRooms = 1

const statuses = computed(() => [
    { label: 'Available', color: 'status-success', count: availableRooms },
    { label: 'Booked', color: 'status-error', count: bookedRooms },
    { label: 'In Use', color: 'status-warning', count: maintenanceRooms },
    { label: 'Broken', color: 'status-neutral', count: reservedRooms },
])

</script>