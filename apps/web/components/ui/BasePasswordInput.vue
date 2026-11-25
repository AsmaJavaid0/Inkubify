<script setup lang="ts">
import { Eye, EyeOff } from 'lucide-vue-next'
import FormField from '~/components/ui/FormField.vue'

interface Props {
  id: string
  label: string
  modelValue: string
  placeholder?: string
  hint?: string
  error?: string
  required?: boolean
  disabled?: boolean
  autocomplete?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '',
  hint: '',
  error: '',
  required: false,
  disabled: false,
  autocomplete: 'current-password',
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  blur: [event: FocusEvent]
}>()

const showPassword = ref(false)
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
          :type="showPassword ? 'text' : 'password'"
          :value="props.modelValue"
          :placeholder="props.placeholder"
          :disabled="props.disabled"
          :required="props.required"
          :autocomplete="props.autocomplete"
          :aria-invalid="hasError || undefined"
          :aria-describedby="describedBy"
          class="w-full rounded-input border bg-navy-700 py-2.5 pl-3.5 pr-11 text-sm text-snow-100 placeholder-snow-100/40 transition-colors focus:outline-none focus:ring-2 focus:ring-gold-500 disabled:cursor-not-allowed disabled:opacity-60"
          :class="hasError ? 'border-danger' : 'border-navy-border hover:border-snow-100/30'"
          @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
          @blur="emit('blur', $event)"
        >
        <button
          type="button"
          :aria-label="showPassword ? 'Hide password' : 'Show password'"
          class="absolute right-2.5 rounded-md p-1.5 text-snow-muted hover:text-snow-100"
          @click="showPassword = !showPassword"
        >
          <EyeOff v-if="showPassword" class="h-4 w-4" aria-hidden="true" />
          <Eye v-else class="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </template>
  </FormField>
</template>
