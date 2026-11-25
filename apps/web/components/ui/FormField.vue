<script setup lang="ts">
interface Props {
  id: string
  label: string
  hint?: string
  error?: string
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  hint: '',
  error: '',
  required: false,
})

const describedBy = computed(() => {
  const ids: string[] = []
  if (props.hint) ids.push(`${props.id}-hint`)
  if (props.error) ids.push(`${props.id}-error`)
  return ids.length ? ids.join(' ') : undefined
})
</script>

<template>
  <div class="space-y-1.5">
    <label
      :for="props.id"
      class="block text-sm font-medium text-snow-100"
    >
      {{ props.label }}
      <span v-if="props.required" class="text-gold-500" aria-hidden="true">*</span>
    </label>

    <slot :described-by="describedBy" :has-error="Boolean(props.error)" />

    <div class="min-h-[1.25rem]">
      <p
        v-if="props.error"
        :id="`${props.id}-error`"
        role="alert"
        class="text-xs font-medium text-danger"
      >
        {{ props.error }}
      </p>
      <p
        v-else-if="props.hint"
        :id="`${props.id}-hint`"
        class="text-xs text-snow-muted"
      >
        {{ props.hint }}
      </p>
    </div>
  </div>
</template>
