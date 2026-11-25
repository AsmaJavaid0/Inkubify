<script setup lang="ts">
definePageMeta({ layout: 'auth' })
</script>

<template>
  <div class="space-y-4">
    <h1 class="text-2xl font-bold text-snow-100">Terms of Service</h1>
    <p class="text-sm leading-relaxed text-snow-muted">
      Inkubify provides structured founder guidance and roadmap planning tools for entrepreneurs
      in Pakistan. Inkubify does not guarantee business or financial outcomes and is not a funding
      platform.
    </p>
    <p class="text-sm leading-relaxed text-snow-muted">
      Full legal terms will be published prior to public launch.
    </p>
    <NuxtLink to="/signup" class="inline-block text-sm font-semibold text-gold-500 hover:underline">
      ← Back to sign up
    </NuxtLink>
  </div>
</template>
