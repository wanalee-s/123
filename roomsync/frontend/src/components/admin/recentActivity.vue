<template>
    <div class="card body bg-white shadow-md mt-10">
        <div class="card-body p-6">
            <div class="w-full">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3"> <!-- อยุ่คนละฝั่ง-->
                    <h2 class="text-3xl font-bold mb-4">Recent Reservation Activity</h2>
                    <div class="flex gap-2 w-full sm:w-auto">
                        <button class="p-3 rounded-2xl border border-base-300
                                    bg-base-100
                                    shadow-sm hover:shadow-md
                                    hover:-translate-y-0.5
                                    transition-all duration-200">Export CSV</button>
                        <button class="p-3 rounded-2xl border border-base-300
                                        bg-base-100
                                        shadow-sm hover:shadow-md
                                        hover:-translate-y-0.5
                                        transition-all duration-200">
                            <!-- icon filter -->
                            <svg xmlns="http://www.w3.org/2000/svg"
                                class="h-5 w-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M3 6h18M6 12h12M10 18h4" />
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table class="table w-full">
                        <thead>
                            <tr>
                                <th>Room Name</th>
                                <th>User</th>
                                <th>Duration</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Dummy data for recent activity -->
                            <tr v-for="(activity, index) in recentActivities" :key="index">
                                <td>{{ activity.roomName }}</td>
                                <td>
                                    <div class="flex items-center gap-3">
                                    <div class="avatar">
                                        <div class="w-10 rounded-full">
                                        <img
                                            :src="activity.image || defaultAvatar"
                                            :alt="activity.user"
                                        />
                                        </div>
                                    </div>
                                    <div>
                                        <div class="font-semibold">
                                        {{ activity.user }}
                                        </div>
                                        <div class="text-sm text-gray-500">{{ activity.role }}</div>
                                    </div>
                                    </div>
                                </td>
                                <td>{{ activity.time }}</td>
                                <td class="text-green-500"><span class="badge" :class="statusConfig[activity.status].badgeColor">
                        {{ statusConfig[activity.status].badge }}
                    </span></td>
                                <td>{{ activity.action }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
const recentActivities = [
    {
        roomName: 'CSB100',
        user: 'Tontan kitty',
        role: 'student',
        image: 'https://media.discordapp.net/attachments/1331135357877489664/1475104740152180736/2.jpeg?ex=699c45d8&is=699af458&hm=e83ddb9a3ab2b9fe5fffebd7cb654484c0320ed02e1495d34fc202186bb2c401&=&format=webp&width=356&height=350',
        time: '2 hours',
        status: 'Completed',
        action: 'ชมรมวิชาการ'
    },
    {
        roomName: 'CSB201',
        user: 'Jane Smith',
        role: 'student',
        image: 'https://media.discordapp.net/attachments/1331135357877489664/1475104740152180736/2.jpeg?ex=699c45d8&is=699af458&hm=e83ddb9a3ab2b9fe5fffebd7cb654484c0320ed02e1495d34fc202186bb2c401&=&format=webp&width=356&height=350',
        time: '1 hour 30 minutes',
        status: 'In Progress',
        action: 'View Details'
    },
    {
        roomName: 'CSB301',
        user: 'Bob Johnson',
        role: 'teacher',
        image: 'https://media.discordapp.net/attachments/1331135357877489664/1475104740152180736/2.jpeg?ex=699c45d8&is=699af458&hm=e83ddb9a3ab2b9fe5fffebd7cb654484c0320ed02e1495d34fc202186bb2c401&=&format=webp&width=356&height=350',
        time: '3 hours',
        status: 'Completed',
        action: 'ติว coding'
    },
    {
        roomName: 'CSB307',
        user: 'admin06',
        role: 'admin',
        image: 'https://media.discordapp.net/attachments/1331135357877489664/1475104740152180736/2.jpeg?ex=699c45d8&is=699af458&hm=e83ddb9a3ab2b9fe5fffebd7cb654484c0320ed02e1495d34fc202186bb2c401&=&format=webp&width=356&height=350',
        time: '45 minutes',
        status: 'Completed',
        action: 'ประชุมกรรมการรุ่น'
    }
]
const statusConfig = {
    'Completed': { badge: 'Completed', badgeColor: 'badge-success' },
    'In Progress': { badge: 'In Progress', badgeColor: 'badge-warning' },
    'Cancelled': { badge: 'Cancelled', badgeColor: 'badge-error' }
}

</script>