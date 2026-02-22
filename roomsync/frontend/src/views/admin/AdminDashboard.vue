<template>
    <AdminLayout>
        <!-- <h1 class="text-3xl font-bold  mb-6 text-center">Admin Dashboard</h1> -->
        <p class="text-xl font-semibold">Welcome back,here's what's happening today.</p>
        <div class="grid grid-cols-12 gap-6 mt-6">
            <div class="col-span-4">
                <div class="card bg-base-200 shadow-md p-4">
                    <div class="card-body">
                        <div class="flex items-center justify-between">
                            <h1 class="card-title text-2xl">Daily Overview Rate</h1>
                            <span class="badge badge-lg badge-success">TODAY</span>
                        </div>
                    </div>
                    <!--#TODO: Dynamic-->
                    <div class="flex justify-center">
                        <div class="radial-progress text-primary text-2xl" style="--value:70; --size:12rem; --thickness: 2rem;" aria-valuenow="70" role="progressbar">70%</div>
                    </div>
                    <div class="card-body">
                        <p class="text-center text-sm text-gray-500">Compared to last week: +5%</p>
                    </div>
                    <div class="grid grid-cols-2 gap-2 mt-1">
                        <div class="col-span-1">
                            <div class="card-body">
                                <p class="text-4xl font-bold text-center">12</p>
                                <p class="text-center text-sm text-gray-500">Total Rooms</p>
                            </div>
                        </div>
                        <div class="col-span-1">
                            <div class="card-body">
                                <p class="text-4xl font-bold text-center">8</p>
                                <p class="text-center text-sm text-gray-500">Booked Rooms</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!--#TODO : Dynamic-->
            <div class="col-span-8">
                <div class="card bg-base-200 shadow-md p-4">
                    <div class="card-body">
                        <div class="flex items-center justify-between">
                            <h1 class="card-title text-2xl">Most Reserved Rooms</h1>
                            <span class="badge badge-lg badge-success">THIS WEEKS</span>
                        </div>
                        <div class="flex flex-col mt-4 space-y-4">
                            <!--เอาแค่ 6 อันแรก-->
                            <div>
                                <div v-for="(item, index) in displayedRooms" :key="index" class="w-full">
                                    <div>
                                        <div class="flex justify-between text-sm mb-2">
                                            <span class="font-medium">{{ item.roomName }}</span>
                                            <span class="text-base-content/60">{{ item.percentage }}%</span>
                                        </div>
                                        <progress class="progress progress-primary w-full" :value="item.percentage" max="100"></progress>
                                    </div>
                                </div>
                            </div>
                            <!--Toggle Button-->
                            <div class="flex justify-center mt-2">
                                <button @click="openModal" class="btn btn-sm btn-outline">
                                    {{ showAll ? 'Show Less' : 'Show All' }}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Room Status Overview-->
        <roomoverview />
        <!-- recent resrtvation activuty-->
        <recentActivity />
        <div class="grid grid-cols-4 gap-6 mt-10">
        </div>
    </AdminLayout>
    <dialog class="modal" :class="{'modal-open': showModal}">
        <form method="dialog" class="modal-box">
            <h3 class="font-bold text-lg">Most Reserved Rooms - This Week</h3>
            <div class="flex flex-col mt-4 space-y-4">
                <div v-for="(item, index) in mostReservedRooms" :key="index" class="w-full">
                    <div>
                        <div class="flex justify-between text-sm mb-2">
                            <span class="font-medium">{{ item.roomName }}</span>
                            <span class="text-base-content/60">{{ item.percentage }}%</span>
                        </div>
                        <progress class="progress progress-primary w-full" :value="item.percentage" max="100"></progress>
                    </div>
                </div>
            </div>
            <!--click button to close-->
            <div class="modal-action">
                <button @click="closeModal" class="btn">Close</button>
            </div>
        </form>
        <!--click outside to close-->
        <form method="dialog" class="modal-backdrop">
            <button @click="closeModal">close</button>
        </form>
    </dialog>
</template>
<script setup>
import roomoverview from '@/components/admin/roomstatus.vue'
import recentActivity from '@/components/admin/recentActivity.vue'
// import AdminLayout from '@/layouts/AdminLayout.vue'
import {ref, onMounted, computed} from 'vue'
import { getDashboardSummary, getRecentReservations } from "@/services/adminService";
// dummy data
const mostReservedRooms = ref([
    { roomName: 'CSB100', percentage: 65 },
    { roomName: 'CSB201', percentage: 50 },
    { roomName: 'CSB202', percentage: 40 },
    { roomName: 'CSB203', percentage: 30 },
    { roomName: 'CSB204', percentage: 20 },
    { roomName: 'CSB205', percentage: 10 },
    { roomName: 'CSB301', percentage: 65 },
    { roomName: 'CSB302', percentage: 50 },
    { roomName: 'CSB303', percentage: 40 },
    { roomName: 'CSB304', percentage: 30 },
    { roomName: 'CSB305', percentage: 20 },
    { roomName: 'CSB306', percentage: 10 },
])
const showModal = ref(false)
const openModal = () => {
    showModal.value = !showModal.value
}
const closeModal = () => {
    showModal.value = false
}
const showAll = ref(false)
const displayedRooms = computed(() => {
    return showAll.value ? mostReservedRooms.value : mostReservedRooms.value.slice(0, 6)
})
</script>