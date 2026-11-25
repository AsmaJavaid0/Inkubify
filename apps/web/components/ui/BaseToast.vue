<script setup lang="ts">
import { X } from 'lucide-vue-next'
import type { ToastMessage } from '~/composables/useToast'

const { toasts, remove } = useToast()

const typeClasses: Record<ToastMessage['type'], string> = {
  success: 'border-success/40 bg-navy-700 text-snow-100',
  error: 'border-danger/50 bg-navy-700 text-snow-100',
  warning: 'border-warning/40 bg-navy-700 text-snow-100',
  info: 'border-gold-500/40 bg-navy-700 text-snow-100',
}
</script>

<template>
  <div
    aria-live="polite"
    class="pointer-events-none fixed bottom-4 right-4 z-50 flex w-full max-w-sm flex-col gap-2 px-4 sm:px-0"
  >
    <div
      v-for="item in toasts"
      :key="item.id"
      role="status"
      class="pointer-events-auto flex items-start justify-between gap-3 rounded-input border px-4 py-3 text-sm shadow-lg"
      :class="typeClasses[item.type as ToastMessage['type']]"
    >
      <p class="leading-snug">{{ item.text }}</p>
      <button
        type="button"
        aria-label="Dismiss notification"
        class="shrink-0 rounded p-0.5 text-snow-muted hover:text-snow-100"
        @click="remove(item.id)"
      >
        <X class="h-4 w-4" aria-hidden="true" />
      </button>
    </div>
  </div>
</template>
