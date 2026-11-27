<script setup lang="ts">
import FormField from '~/components/ui/FormField.vue'

interface Props {
  id: string
  label: string
  modelValue: string | null | undefined
  type?: 'text' | 'email' | 'date' | 'url' | 'number'
  placeholder?: string
  hint?: string
  error?: string
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  autocomplete?: string
  maxlength?: number
  max?: string
  min?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  hint: '',
  error: '',
  required: false,
  disabled: false,
  readonly: false,
  autocomplete: undefined,
  maxlength: undefined,
  max: undefined,
  min: undefined,
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
      <div class="relative flex items-center">
        <input
          :id="props.id"
          ref="inputRef"
          :type="props.type"
          :value="props.modelValue ?? ''"
          :placeholder="props.placeholder"
          :disabled="props.disabled"
          :readonly="props.readonly"
          :required="props.required"
          :autocomplete="props.autocomplete"
          :maxlength="props.maxlength"
          :min="props.min"
          :max="props.max"
          :aria-invalid="hasError || undefined"
          :aria-describedby="describedBy"
          class="w-full rounded-input border bg-navy-700 px-3.5 py-2.5 text-sm text-snow-100 placeholder-snow-100/40 transition-colors focus:outline-none focus:ring-2 focus:ring-gold-500 disabled:cursor-not-allowed disabled:opacity-60 read-only:opacity-75"
          :class="hasError ? 'border-danger' : 'border-navy-border hover:border-snow-100/30'"
          @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
          @blur="emit('blur', $event)"
        >
        <div v-if="$slots.trailing" class="absolute right-3 flex items-center">
          <slot name="trailing" />
        </div>
      </div>
    </template>
  </FormField>
</template>
