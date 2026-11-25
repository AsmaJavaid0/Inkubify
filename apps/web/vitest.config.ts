import { defineConfig } from 'vitest/config'

const rootDir = decodeURIComponent(
  new URL('.', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'),
)

export default defineConfig({
  resolve: {
    alias: {
      '~': rootDir,
      '@': rootDir,
    },
  },
  test: {
    environment: 'happy-dom',
    include: ['tests/unit/**/*.test.ts'],
  },
})
