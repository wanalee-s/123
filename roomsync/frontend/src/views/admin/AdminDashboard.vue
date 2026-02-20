<script setup>
// import AdminLayout from '@/layouts/AdminLayout.vue'
import {ref, onMounted} from 'vue'
import { getDashboardSummary, getRecentReservations } from "@/services/adminService";

const dashboardSummary = ref(null)
const recentReservations = ref([])
onMounted(async () => { //คือการใช้ onMounted เพื่อเรียกข้อมูลเมื่อ component ถูก mount ขึ้นมา
    try {
        const summaryResponse = await getDashboardSummary();
        dashboardSummary.value = summaryResponse.data;

        const reservationsResponse = await getRecentReservations();
        recentReservations.value = reservationsResponse.data;
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
    }
})
</script>

<template>
    <AdminLayout>
        <h1 class="text-3xl font-bold  mb-6">Admin Dashboard</h1>
        <p>Welcome to the admin dashboard!</p>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
            <div class="bg-white shadow rounded-2xl p-4">
                <h2 class="text-lg font-semibold text-primary mb-2">Total Users</h2>
                <p class="text-2xl text-primary">{{ dashboardSummary?.total_users || 0 }}</p>
            </div>
            <div class="bg-white shadow rounded-2xl p-4">
                <h2 class="text-lg font-semibold text-primary mb-2">Total Rooms</h2>
                <p class="text-2xl text-primary">{{ dashboardSummary?.total_rooms || 0 }}</p>
            </div>
            <div class="bg-white shadow rounded-2xl p-4">
                <h2 class="text-lg font-semibold text-primary mb-2">Total Reservations</h2>
                <p class="text-2xl text-primary">{{ dashboardSummary?.total_reservations || 0 }}</p>
            </div>
            <div class="bg-white shadow rounded-2xl p-4">
                <h2 class="text-lg font-semibold text-primary mb-2">Pending Approvals</h2>
                <p class="text-2xl text-primary">{{ dashboardSummary?.pending_approvals || 0 }}</p>
            </div>
        </div>
    </AdminLayout>
</template>
