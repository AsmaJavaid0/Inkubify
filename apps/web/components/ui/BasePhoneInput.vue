<script setup lang="ts">
import FormField from '~/components/ui/FormField.vue'

interface Props {
  id: string
  label: string
  modelValue: string
  hint?: string
  error?: string
  required?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  hint: 'Pakistani mobile number (e.g. 03001234567 or 3001234567)',
  error: '',
  required: false,
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  blur: [event: FocusEvent]
}>()

const inputRef = ref<HTMLInputElement | null>(null)
defineExpose({ focus: () => inputRef.value?.focus() })
</script>

<template>
  <FormField
    :id="props.id"
    :label="props.label"
    :hint="props.hint"
    :error="props.error"
    :required="props.required"
  >
    <template #default="{ describedBy, hasError }">
      <div
        class="flex items-stretch overflow-hidden rounded-input border bg-navy-700 transition-colors focus-within:ring-2 focus-within:ring-gold-500"
        :class="hasError ? 'border-danger' : 'border-navy-border hover:border-snow-100/30'"
      >
        <span
          class="inline-flex items-center border-r border-navy-border bg-navy-900/50 px-3 text-sm font-medium text-snow-100 select-none"
        >
          PK +92
        </span>
        <input
          :id="props.id"
          ref="inputRef"
          type="tel"
          inputmode="tel"
          autocomplete="tel"
          :value="props.modelValue"
          placeholder="300 1234567"
          :disabled="props.disabled"
          :required="props.required"
          :aria-invalid="hasError || undefined"
          :aria-describedby="describedBy"
          class="w-full bg-transparent px-3.5 py-2.5 text-sm text-snow-100 placeholder-snow-100/40 focus:outline-none disabled:cursor-not-allowed disabled:opacity-60"
          @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
          @blur="emit('blur', $event)"
        >
      </div>
    </template>
  </FormField>
</template>
