<script setup lang="ts">
import FormField from '~/components/ui/FormField.vue'

export interface ChipOption {
  value: string
  label: string
}

interface Props {
  id: string
  label: string
  modelValue: string | string[] | null | undefined
  options: ChipOption[]
  multiple?: boolean
  hint?: string
  error?: string
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  multiple: false,
  hint: '',
  error: '',
  required: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string | string[]]
}>()

function isSelected(val: string): boolean {
  if (props.multiple) {
    return Array.isArray(props.modelValue) && props.modelValue.includes(val)
  }
  return props.modelValue === val
}

function toggle(val: string) {
  if (props.multiple) {
    const current = Array.isArray(props.modelValue) ? [...props.modelValue] : []
    const idx = current.indexOf(val)
    if (idx >= 0) {
      current.splice(idx, 1)
    } else {
      current.push(val)
    }
    emit('update:modelValue', current)
  } else {
    emit('update:modelValue', val)
  }
}
</script>

<template>
  <FormField
    :id="props.id"
    :label="props.label"
    :hint="props.hint"
    :error="props.error"
    :required="props.required"
  >
    <div
      :id="props.id"
      role="group"
      :aria-label="props.label"
      class="flex flex-wrap gap-2"
    >
      <button
        v-for="opt in props.options"
        :key="opt.value"
        type="button"
        :aria-pressed="isSelected(opt.value)"
        class="rounded-[10px] border px-3.5 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold-500"
        :class="
          isSelected(opt.value)
            ? 'border-gold-500 bg-gold-500/15 text-gold-500'
            : 'border-navy-border bg-navy-700 text-snow-100 hover:border-snow-100/35'
        "
        @click="toggle(opt.value)"
      >
        {{ opt.label }}
      </button>
    </div>
  </FormField>
</template>
