// filepath: /Users/florian/Documents/Code/Visual  Studio Code/UNamur/Bloc3 /Projets/Projet-Individuel/SMS-01/project/vitest.config.js
import { defineConfig } from 'vitest/config';
import { fileURLToPath, URL } from 'url';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
  },
  resolve: {
    alias: {
      $lib: fileURLToPath(new URL('./src/lib', import.meta.url))
    },
  },
});