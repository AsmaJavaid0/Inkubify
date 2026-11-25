<script setup lang="ts">
interface Props {
  id: string
  modelValue: boolean
  error?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  error: '',
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()
</script>

<template>
  <div class="space-y-1">
    <label
      :for="props.id"
      class="flex cursor-pointer items-start gap-3 text-sm text-snow-100"
      :class="{ 'cursor-not-allowed opacity-60': props.disabled }"
    >
      <input
        :id="props.id"
        type="checkbox"
        :checked="props.modelValue"
        :disabled="props.disabled"
        :aria-invalid="Boolean(props.error) || undefined"
        class="mt-0.5 h-4 w-4 shrink-0 rounded border-navy-border bg-navy-700 text-gold-500 accent-[#C19829] focus:ring-2 focus:ring-gold-500"
        @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
      >
      <span class="leading-snug">
        <slot />
      </span>
    </label>
    <p v-if="props.error" role="alert" class="text-xs font-medium text-danger">
      {{ props.error }}
    </p>
  </div>
</template>
