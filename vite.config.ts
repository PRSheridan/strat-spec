import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {  // Proxy all requests starting with `/api/`, ALT install flask_CORS
        target: 'http://localhost:5555',  // Flask backend
        changeOrigin: true,
        secure: false,
      },
    },
  },
});



