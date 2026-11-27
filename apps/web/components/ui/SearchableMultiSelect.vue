<script setup lang="ts">
import { computed, ref } from 'vue'
import BaseInput from '~/components/ui/BaseInput.vue'
interface Option { value: string; label: string }
const props = withDefaults(defineProps<{
  id: string; label: string; modelValue: string[]; options: Option[]
  placeholder?: string; hint?: string; error?: string
}>(), { placeholder: 'Search options...', hint: '', error: '' })
const emit = defineEmits<{ 'update:modelValue': [value: string[]] }>()
const query = ref('')
const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return props.options.filter((option) =>
    (!q || option.label.toLowerCase().includes(q)) && !props.modelValue.includes(option.value),
  )
})
const selected = computed(() => props.options.filter((option) => props.modelValue.includes(option.value)))
function toggle(value: string) {
  const next = [...props.modelValue]
  const index = next.indexOf(value)
  if (index >= 0) next.splice(index, 1)
  else next.push(value)
  emit('update:modelValue', next)
}
</script>
<template>
  <div class="space-y-2">
    <p class="text-sm font-medium text-snow-100">{{ props.label }}</p>
    <BaseInput :id="props.id + '-search'" v-model="query" label="Search options" :placeholder="props.placeholder" />
    <div v-if="selected.length" class="flex flex-wrap gap-2">
      <button v-for="item in selected" :key="item.value" type="button" class="rounded-full border border-gold-500/40 bg-gold-500/10 px-3 py-1 text-xs text-gold-500" @click="toggle(item.value)">{{ item.label }} ×</button>
    </div>
    <div class="max-h-36 space-y-1 overflow-y-auto rounded-input border border-navy-border bg-navy-900/40 p-2">
      <button v-for="item in filtered" :key="item.value" type="button" class="block w-full rounded px-2.5 py-2 text-left text-sm text-snow-100 hover:bg-navy-700" @click="toggle(item.value)">{{ item.label }}</button>
      <p v-if="!filtered.length" class="px-2 py-2 text-xs text-snow-muted">No matching options.</p>
    </div>
    <p v-if="props.hint" class="text-xs text-snow-muted">{{ props.hint }}</p>
    <p v-if="props.error" role="alert" class="text-xs text-danger">{{ props.error }}</p>
  </div>
</template>
