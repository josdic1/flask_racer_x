import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Match the port Vite is running on
    proxy: {
      '/api': {
        target: 'http://localhost:5555', // Match the port Flask is running on
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // Optional: Remove '/api' prefix if needed
      }
    }
  }
})