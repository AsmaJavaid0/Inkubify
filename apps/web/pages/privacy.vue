<script setup lang="ts">
definePageMeta({ layout: 'auth' })
</script>

<template>
  <div class="space-y-4">
    <h1 class="text-2xl font-bold text-snow-100">Privacy Policy</h1>
    <p class="text-sm leading-relaxed text-snow-muted">
      You stay in control of your founder data. Account credentials and profile information are
      protected with Row Level Security and used solely to personalize your Inkubify experience.
    </p>
    <p class="text-sm leading-relaxed text-snow-muted">
      Full privacy disclosures will be published prior to public launch.
    </p>
    <NuxtLink to="/signup" class="inline-block text-sm font-semibold text-gold-500 hover:underline">
      ← Back to sign up
    </NuxtLink>
  </div>
</template>
