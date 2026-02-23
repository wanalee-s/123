<template>
    <!-- Room Status Overview-->
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mt-10">
            <div class="flex-1">
                <h1 class="text-3xl font-bold">Room Status Overview</h1>
                <div v-if="error" class="alert alert-error mt-4">
                    {{ error }}
                </div>
                <div class="flex flex-wrap gap-6">
                    <div
                        v-for="status in statusesWithCounts"
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
            <div class="w-full lg:w-auto">
                <button class="btn btn-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                    Register New Item
                </button>
            </div>
        </div>
        <Roomcard />
</template>
<script setup>
import { computed, ref, onMounted } from 'vue'
import api from '@/services/api.js'
import Roomcard from './roomcard.vue'

const statuses = ref([])
const error = ref(null)

const statusConfig = {
        available: { label: 'Available', color: 'status-success' },
        booked: { label: 'Booked', color: 'status-error' },
        inuse: { label: 'In Use', color: 'status-warning' },
        broken: { label: 'Broken', color: 'status-neutral' }
}

onMounted(async () => {
    try {
        const response = await api.get('/api/v1/rooms/status')
        statuses.value = response.data
    } catch (err) {
        error.value = `Failed to fetch data: ${err.response?.data?.detail || err.message}`
        console.error('API Error:', err)
    }
})

const statusesWithCounts = computed(() => {
        return Object.entries(statusConfig).map(([key, cfg]) => ({
                label: cfg.label,
                color: cfg.color,
        count: statuses.value[key] || 0
        }))
})
</script>