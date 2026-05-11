import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite 配置：本地开发时将 API 指向环境变量 VITE_API_BASE（见 .env.example）
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
})
