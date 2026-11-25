<script setup lang="ts">
import { Search, X } from 'lucide-vue-next'
import { PROFICIENCY_OPTIONS } from '~/constants/options'
import type { Proficiency, SkillCatalogItem } from '~/types/api'

export interface SelectedSkillItem {
  skill_id: number
  proficiency: Proficiency
}

interface Props {
  catalog: SkillCatalogItem[]
  modelValue: SelectedSkillItem[]
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  error: '',
})

const emit = defineEmits<{
  'update:modelValue': [value: SelectedSkillItem[]]
}>()

const searchQuery = ref('')

const selectedMap = computed(() => {
  const map = new Map<number, Proficiency>()
  for (const item of props.modelValue) {
    map.set(item.skill_id, item.proficiency)
  }
  return map
})

const catalogById = computed(() => {
  const map = new Map<number, SkillCatalogItem>()
  for (const item of props.catalog) {
    map.set(item.id, item)
  }
  return map
})

const filteredGroups = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  const groups = new Map<string, SkillCatalogItem[]>()

  for (const skill of props.catalog) {
    if (
      q &&
      !skill.name.toLowerCase().includes(q) &&
      !skill.category.toLowerCase().includes(q)
    ) {
      continue
    }
    const list = groups.get(skill.category) ?? []
    list.push(skill)
    groups.set(skill.category, list)
  }

  return Array.from(groups.entries()).map(([category, items]) => ({ category, items }))
})

function toggleSkill(skillId: number) {
  const next = [...props.modelValue]
  const idx = next.findIndex((s) => s.skill_id === skillId)
  if (idx >= 0) {
    next.splice(idx, 1)
    emit('update:modelValue', next)
    return
  }
  if (next.length >= 10) return
  next.push({ skill_id: skillId, proficiency: 'intermediate' })
  emit('update:modelValue', next)
}

function setProficiency(skillId: number, proficiency: Proficiency) {
  const next = props.modelValue.map((item) =>
    item.skill_id === skillId ? { ...item, proficiency } : item,
  )
  emit('update:modelValue', next)
}
</script>

<template>
  <div class="space-y-5">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <p class="text-xs text-snow-muted">
        Select 1 to 10 skills and set your proficiency for each.
      </p>
      <span
        class="rounded-full border border-navy-border bg-navy-900/60 px-2.5 py-0.5 text-xs font-medium"
        :class="props.modelValue.length >= 10 ? 'text-warning' : 'text-gold-500'"
      >
        {{ props.modelValue.length }} / 10 selected
      </span>
    </div>

    <div class="relative">
      <Search
        class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-snow-muted"
        aria-hidden="true"
      />
      <input
        v-model="searchQuery"
        type="search"
        aria-label="Search skills"
        placeholder="Search skills (e.g. Meta Ads, Web Development, Finance)..."
        class="w-full rounded-input border border-navy-border bg-navy-900/50 py-2.5 pl-10 pr-4 text-sm text-snow-100 placeholder-snow-100/40 focus:outline-none focus:ring-2 focus:ring-gold-500"
      >
    </div>

    <p v-if="props.error" role="alert" class="text-xs font-medium text-danger">
      {{ props.error }}
    </p>

    <!-- Selected skills with proficiency segmented controls -->
    <div
      v-if="props.modelValue.length > 0"
      class="space-y-2.5 rounded-input border border-gold-500/30 bg-navy-900/40 p-4"
    >
      <h3 class="text-xs font-semibold uppercase tracking-wider text-gold-500">
        Selected skills &amp; proficiency
      </h3>
      <div
        v-for="item in props.modelValue"
        :key="item.skill_id"
        class="flex flex-col gap-2 rounded-input border border-navy-border bg-navy-700 p-3 sm:flex-row sm:items-center sm:justify-between"
      >
        <div class="flex items-center justify-between gap-2">
          <span class="text-sm font-medium text-snow-100">
            {{ catalogById.get(item.skill_id)?.name ?? `Skill #${item.skill_id}` }}
          </span>
          <button
            type="button"
            :aria-label="`Remove ${catalogById.get(item.skill_id)?.name ?? 'skill'}`"
            class="rounded p-1 text-snow-muted hover:text-danger sm:hidden"
            @click="toggleSkill(item.skill_id)"
          >
            <X class="h-4 w-4" aria-hidden="true" />
          </button>
        </div>

        <div class="flex items-center gap-2">
          <div
            role="group"
            :aria-label="`Proficiency for ${catalogById.get(item.skill_id)?.name ?? 'skill'}`"
            class="inline-flex rounded-[10px] border border-navy-border bg-navy-900/60 p-0.5"
          >
            <button
              v-for="opt in PROFICIENCY_OPTIONS"
              :key="opt.value"
              type="button"
              :aria-pressed="item.proficiency === opt.value"
              class="rounded-[8px] px-2.5 py-1 text-xs font-medium transition-colors"
              :class="
                item.proficiency === opt.value
                  ? 'bg-gold-500 text-navy-900 font-semibold'
                  : 'text-snow-muted hover:text-snow-100'
              "
              @click="setProficiency(item.skill_id, opt.value)"
            >
              {{ opt.label }}
            </button>
          </div>

          <button
            type="button"
            :aria-label="`Remove ${catalogById.get(item.skill_id)?.name ?? 'skill'}`"
            class="hidden rounded p-1 text-snow-muted hover:text-danger sm:inline-flex"
            @click="toggleSkill(item.skill_id)"
          >
            <X class="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>

    <!-- Grouped catalog chips -->
    <div class="space-y-4">
      <div
        v-for="group in filteredGroups"
        :key="group.category"
        class="space-y-2"
      >
        <h3 class="text-xs font-semibold uppercase tracking-wider text-snow-muted">
          {{ group.category }}
        </h3>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="skill in group.items"
            :key="skill.id"
            type="button"
            :aria-pressed="selectedMap.has(skill.id)"
            :disabled="!selectedMap.has(skill.id) && props.modelValue.length >= 10"
            class="rounded-[10px] border px-3 py-1.5 text-xs font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-45"
            :class="
              selectedMap.has(skill.id)
                ? 'border-gold-500 bg-gold-500/15 text-gold-500'
                : 'border-navy-border bg-navy-700 text-snow-100 hover:border-snow-100/35'
            "
            @click="toggleSkill(skill.id)"
          >
            {{ skill.name }}
          </button>
        </div>
      </div>

      <p
        v-if="filteredGroups.length === 0"
        class="py-4 text-center text-sm text-snow-muted"
      >
        No matching skills found for "{{ searchQuery }}".
      </p>
    </div>
  </div>
</template>
