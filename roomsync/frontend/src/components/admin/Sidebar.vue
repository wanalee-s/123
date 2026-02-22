<script>
import { ref, onMounted } from 'vue'
import { getMyProfile } from '../../services/adminService';
const userProfile = ref(null)
onMounted(async () => {
    try {
        const response = await getMyProfile();
        userProfile.value = response.data;
    } catch (error) {
        console.error('Error fetching user profile:', error);
    }
})
</script>
<template>
    <div class="drawer-side">
        <label for="drawer" class="drawer-overlay"></label>

        <ul class="menu p-4 w-80 h-full bg-base-200 text-base-content flex flex-col gap-2 text-lg">

        <!-- Profile -->
        <div class="p-4">
            <div class="flex items-center gap-4">
            <div class="avatar">
                <div class="w-12 rounded-full">
                <img src="#" />
                </div>
            </div>
            <div>
                <p class="font-bold">{{ userProfile?.name || "Admin Name" }}</p>
                <p class="text-sm opacity-50">{{ userProfile?.email || "admin@roomsync.com" }}</p>
            </div>
            </div>
        </div>

        <!-- Menu -->
        <li><a href="/admin/">Dashboard</a></li>
        <li><a href="/admin/roomManage">Room Management</a></li>
        <li><a href="#">Booking Management</a></li> <!--รวม Approve ห้อง-->
        <li><a href="/admin/roleApprove">Role Management</a></li>
        <li><a href="#">Settings</a></li>
        </ul>

        <!--logout-->
        <div class="absolute bottom-0 w-80 p-4">
            <button class="btn btn-error w-full">Logout</button>
        </div>
    </div>
</template>
