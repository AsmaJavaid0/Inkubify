<script setup lang="ts">
import { ChevronDown } from 'lucide-vue-next'
import FormField from '~/components/ui/FormField.vue'

export interface SelectOption {
  value: string
  label: string
}

interface Props {
  id: string
  label: string
  modelValue: string | null | undefined
  options: SelectOption[]
  placeholder?: string
  hint?: string
  error?: string
  required?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Select an option',
  hint: '',
  error: '',
  required: false,
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  blur: [event: FocusEvent]
}>()

const selectRef = ref<HTMLSelectElement | null>(null)
defineExpose({ focus: () => selectRef.value?.focus() })
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
      <div class="relative">
        <select
          :id="props.id"
          ref="selectRef"
          :value="props.modelValue ?? ''"
          :disabled="props.disabled"
          :required="props.required"
          :aria-invalid="hasError || undefined"
          :aria-describedby="describedBy"
          class="w-full appearance-none rounded-input border bg-navy-700 py-2.5 pl-3.5 pr-10 text-sm text-snow-100 transition-colors focus:outline-none focus:ring-2 focus:ring-gold-500 disabled:cursor-not-allowed disabled:opacity-60"
          :class="[
            hasError ? 'border-danger' : 'border-navy-border hover:border-snow-100/30',
            !props.modelValue ? 'text-snow-100/50' : '',
          ]"
          @change="emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
          @blur="emit('blur', $event)"
        >
          <option value="" disabled class="bg-navy-900 text-snow-100/60">
            {{ props.placeholder }}
          </option>
          <option
            v-for="opt in props.options"
            :key="opt.value"
            :value="opt.value"
            class="bg-navy-900 text-snow-100"
          >
            {{ opt.label }}
          </option>
        </select>
        <ChevronDown
          class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-snow-muted"
          aria-hidden="true"
        />
      </div>
    </template>
  </FormField>
</template>
