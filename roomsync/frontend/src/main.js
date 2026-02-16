import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './assets/css/style.css'
import App from './App.vue'
import router from './router'


const app = createApp(App);
app.use(createPinia()); // Add Pinia
app.use(router);
app.mount("#app");