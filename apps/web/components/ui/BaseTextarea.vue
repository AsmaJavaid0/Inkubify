<script setup lang="ts">
import FormField from '~/components/ui/FormField.vue'

interface Props {
  id: string
  label: string
  modelValue: string | null | undefined
  placeholder?: string
  hint?: string
  error?: string
  required?: boolean
  disabled?: boolean
  rows?: number
  maxlength?: number
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '',
  hint: '',
  error: '',
  required: false,
  disabled: false,
  rows: 3,
  maxlength: undefined,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  blur: [event: FocusEvent]
}>()

const currentLength = computed(() => (props.modelValue ?? '').length)
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
      <div class="space-y-1">
        <textarea
          :id="props.id"
          :rows="props.rows"
          :value="props.modelValue ?? ''"
          :placeholder="props.placeholder"
          :disabled="props.disabled"
          :required="props.required"
          :maxlength="props.maxlength"
          :aria-invalid="hasError || undefined"
          :aria-describedby="describedBy"
          class="w-full rounded-input border bg-navy-700 px-3.5 py-2.5 text-sm text-snow-100 placeholder-snow-100/40 transition-colors focus:outline-none focus:ring-2 focus:ring-gold-500 disabled:cursor-not-allowed disabled:opacity-60"
          :class="hasError ? 'border-danger' : 'border-navy-border hover:border-snow-100/30'"
          @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
          @blur="emit('blur', $event)"
        />
        <div
          v-if="props.maxlength"
          class="text-right text-xs text-snow-muted"
          aria-live="polite"
        >
          {{ currentLength }} / {{ props.maxlength }}
        </div>
      </div>
    </template>
  </FormField>
</template>
