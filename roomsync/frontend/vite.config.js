import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';
import tailwindcss from '@tailwindcss/vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: { // dev
    host: '0.0.0.0', // Allows Vite to listen on all interfaces
    port: 8080, // Ensure the port matches the one in your Dockerfile
    // watch: {
    //   usePolling: true
    // }
  },

})