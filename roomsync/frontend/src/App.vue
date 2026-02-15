<script setup>
</script>
<template>
  <div>
    <nav class="navbar">
      <router-link to="/">Dashboard</router-link> |
      <router-link to="/calendar">Calendar</router-link> |
      <router-link to="/myResevation">UserStatus</router-link> |
    </nav>
    <!-- Render the appropriate component for the current route -->
    <router-view />
  </div>
</template>
<style>
* {
  font-family: 'Kanit', sans-serif;
}
</style>
<style scoped>
nav {
  margin-top: 1em;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>