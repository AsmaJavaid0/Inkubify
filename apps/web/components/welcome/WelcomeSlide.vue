<script setup lang="ts">
interface Props {
  title: string
  description: string
  stepIndex: number
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-4 text-center">
    <div
      class="mx-auto inline-flex h-12 w-12 items-center justify-center rounded-card border border-gold-500/40 bg-gold-500/15 text-lg font-bold text-gold-500"
      aria-hidden="true"
    >
      0{{ stepIndex + 1 }}
    </div>
    <h1 class="text-2xl font-bold tracking-tight text-snow-100">
      {{ title }}
    </h1>
    <p class="mx-auto max-w-sm text-sm leading-relaxed text-snow-muted">
      {{ description }}
    </p>
  </div>
</template>
