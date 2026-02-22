<template>
    <div class="overflow-x-auto mt-6 pb-4">
        <div class="flex gap-6 min-w-max">
            <div
            v-for="room in rooms"
            :key="room.id"
            class="card w-72 shrink-0 bg-base-100 shadow-xl border p-4 transition-all duration-300
            hover:-translate-y-1 hover:shadow-xl"
            :class="statusConfig[room.status].border"
            >
            <figure>
            <img
                :src="room.image"
                :alt="room.name"
                class="w-full h-40 object-cover rounded-lg"
            />
            </figure>
            <div class="card-body">
                <h2 class="card-title">{{ room.name }}</h2>
                <p v-if="room.status === 'available'">{{ room.level }}</p>
                <p v-else-if="room.status === 'booked'">Until: {{ room.until }}</p>
                <p v-else-if="room.status === 'inuse'">Active Time: {{ room.activeTime }}</p>
                <p v-else-if="room.status === 'broken'">Note: {{ room.note }}</p>
                <p>Pax: {{ room.pax }}</p>
                <div class="card-actions justify-end">
                    <span class="badge" :class="statusConfig[room.status].badgeColor">
                        {{ statusConfig[room.status].badge }}
                    </span>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>
<script setup>
//dummy data
const rooms = [
    {
        id: 1,
        name: 'CSB100',
        level: 'Level 1, East',
        until: '4:00 PM',
        activeTime: '2h 30m',
        note: null,
        pax: 12,
        status: 'available',
        image: 'https://media.discordapp.net/attachments/1471409777664987177/1473289327122583553/IMG_6809.jpg?ex=699b99db&is=699a485b&hm=f3f0f85ce89d224e0340a434c934a24844f62bef6cbd51b41b2411a47fe29971&=&format=webp&width=725&height=544'
    },
    {
        id: 2,
        name: 'CSB201',
        level: 'Level 2, West',
        until: '4:30 PM',
        activeTime: '1h 12m',
        note: null,
        pax: 8,
        status: 'booked',
        image: 'https://media.discordapp.net/attachments/1471409777664987177/1474281379431977030/IMG_6847.jpg?ex=699bea07&is=699a9887&hm=b0d7a697e97ffe05d8d30a1bb07b8839e4b4eecd7606213bed01b2d0a0f1c68b&=&format=webp&width=725&height=544'
    },
    {
        id: 3,
        name: 'CSB301',
        level: 'Level 3, East',
        until: null,
        activeTime: '3h 45m',
        note: null,
        pax: 20,
        status: 'inuse',
        image: 'https://media.discordapp.net/attachments/1471409777664987177/1474303771977842698/IMG_6884.jpg?ex=699bfee2&is=699aad62&hm=c8d0f125b4cd3dc645793f117d3b3da99639fded12e84135149e6f78f44172f4&=&format=webp&width=725&height=544'
    },
    {
        id: 4,
        name: 'CSB307',
        level: 'Level 3, West',
        until: null,
        activeTime: null,
        note: 'Under Repair',
        pax: 1,
        status: 'broken',
        image: 'https://media.discordapp.net/attachments/1471409777664987177/1474310454082801666/20260220_142417.jpg?ex=699c051b&is=699ab39b&hm=e30a3e38a33bf5e866cc6b233a0e5e660a0e874141e47bb0289d9ac9718bdee3&=&format=webp&width=725&height=544'
    },
    {
        id: 5,
        name: 'CSB308',
        level: 'Level 3, West',
        until: null,
        activeTime: null,
        note: 'Under Repair',
        pax: 1,
        status: 'broken',
        image: 'https://media.discordapp.net/attachments/1471409777664987177/1474282529660993656/IMG_6870.jpg?ex=699beb19&is=699a9999&hm=5221e433c3bba27a0b288a5ef87ab491926e1857f52de2bfe35882c770208a58&=&format=webp&width=725&height=544'
    }
]
const statusConfig = {
    available: {
        badge: 'AVAILABLE',
        badgeColor: 'bg-green-500',
        border: 'border-green-500',
        action: null
    },
    booked: {
        badge: 'BOOKED',
        badgeColor: 'bg-yellow-400 text-black',
        border: 'border-yellow-500',
        action: null
    },
    inuse: {
        badge: 'IN USE',
        badgeColor: 'bg-orange-500',
        border: 'border-orange-500',
        action: 'Release'
    },
    broken: {
        badge: 'BROKEN',
        badgeColor: 'bg-gray-400',
        border: 'border-gray-500',
        action: 'Re-Activate'
    }
}
</script>