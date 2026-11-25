<script setup lang="ts">
interface Props {
  password: string
}

const props = defineProps<Props>()

interface CheckItem {
  label: string
  met: boolean
}

const checks = computed<CheckItem[]>(() => [
  { label: '8+ characters', met: props.password.length >= 8 },
  { label: 'Lowercase letter', met: /[a-z]/.test(props.password) },
  { label: 'Uppercase letter', met: /[A-Z]/.test(props.password) },
  { label: 'Number', met: /\d/.test(props.password) },
])

const score = computed(() => checks.value.filter((c: CheckItem) => c.met).length)

const strengthLabel = computed(() => {
  if (!props.password) return ''
  if (score.value <= 1) return 'Weak'
  if (score.value <= 3) return 'Fair'
  return 'Strong'
})

const barColor = computed(() => {
  if (score.value <= 1) return 'bg-danger'
  if (score.value <= 3) return 'bg-warning'
  return 'bg-success'
})
</script>

<template>
  <div v-if="props.password" class="space-y-2 pt-1" aria-live="polite">
    <div class="flex items-center justify-between text-xs">
      <span class="text-snow-muted">Password strength</span>
      <span
        class="font-semibold"
        :class="
          score <= 1
            ? 'text-danger'
            : score <= 3
              ? 'text-warning'
              : 'text-success'
        "
      >
        {{ strengthLabel }}
      </span>
    </div>

    <div class="grid grid-cols-4 gap-1.5" aria-hidden="true">
      <div
        v-for="idx in 4"
        :key="idx"
        class="h-1.5 rounded-full transition-colors"
        :class="idx <= score ? barColor : 'bg-navy-900/60'"
      />
    </div>

    <ul class="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
      <li
        v-for="item in checks"
        :key="item.label"
        class="flex items-center gap-1.5"
        :class="item.met ? 'text-success' : 'text-snow-muted'"
      >
        <span aria-hidden="true">{{ item.met ? '✓' : '•' }}</span>
        <span>{{ item.label }}</span>
      </li>
    </ul>
  </div>
</template>
