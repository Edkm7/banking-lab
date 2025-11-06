import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build', // build final pour Nginx
  },
  server: {
    port: 5173, // dev server (pas utilisé en prod)
    proxy: {
      '/auth': 'http://auth-service:8080',
      '/users': 'http://accounts-service:8081',
      '/accounts': 'http://accounts-service:8081',
      '/reports': 'http://reports-service:8082'
    }
  }
});
