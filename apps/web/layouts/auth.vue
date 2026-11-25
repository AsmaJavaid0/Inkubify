<script setup lang="ts">
import AppLogo from '~/components/brand/AppLogo.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col items-center justify-center bg-navy-900 px-4 py-10 text-snow-100">
    <div class="mb-6">
      <AppLogo size="lg" />
    </div>

    <main class="w-full max-w-[480px] rounded-card border border-navy-border bg-navy-700 p-6 shadow-xl sm:p-8">
      <slot />
    </main>
  </div>
</template>
