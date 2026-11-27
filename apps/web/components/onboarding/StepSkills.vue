<script setup lang="ts">
import SkillPicker from '~/components/onboarding/SkillPicker.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BaseSelect from '~/components/ui/BaseSelect.vue'
import BaseTextarea from '~/components/ui/BaseTextarea.vue'
import { AVAILABILITY_OPTIONS } from '~/constants/options'
import { stepSkillsSchema } from '~/schemas/profile'
import { useOnboardingStore } from '~/stores/onboarding'
import { useProfileStore } from '~/stores/profile'
import { parseApiError } from '~/utils/errors'

interface Props { mode?: 'wizard' | 'edit' }
const props = withDefaults(defineProps<Props>(), { mode: 'wizard' })
const emit = defineEmits<{ next: []; back: [] }>()
const onboarding = useOnboardingStore()
const profileStore = useProfileStore()
const toast = useToast()
const draft = onboarding.draft
const errors = reactive<Record<string, string>>({})
const error = ref('')
const saving = ref(false)
const loadingCatalog = ref(false)

onMounted(async () => {
  if (profileStore.skillsCatalog.length === 0) {
    loadingCatalog.value = true
    try { await profileStore.fetchSkillsCatalog() }
    finally { loadingCatalog.value = false }
  }
})

async function handleSave() {
  error.value = ''
  for (const key of Object.keys(errors)) delete errors[key]
  const parsed = stepSkillsSchema.safeParse({
    skills: draft.skills,
    other_skills: draft.other_skills,
    experience_level: draft.experience_level,
    experience_years: draft.experience_years,
    portfolio_url: draft.portfolio_url,
    linkedin_url: draft.linkedin_url,
    github_url: draft.github_url,
    availability: draft.availability,
  })
  if (!parsed.success) {
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? '')
      if (key && !errors[key]) errors[key] = issue.message
    }
    error.value = errors.skills || 'Please review the highlighted fields'
    return
  }
  saving.value = true
  try {
    await profileStore.replaceSkills(parsed.data.skills)
    const payload: Record<string, unknown> = {
      other_skills: parsed.data.other_skills || null,
      experience_level: parsed.data.experience_level,
      experience_years: parsed.data.experience_years,
      portfolio_url: parsed.data.portfolio_url || null,
      linkedin_url: parsed.data.linkedin_url || null,
      github_url: parsed.data.github_url || null,
      availability: parsed.data.availability,
    }
    if (props.mode === 'wizard') payload.onboarding_step = 4
    await profileStore.patchProfile(payload)
    if (props.mode === 'wizard') emit('next')
    else toast.success('Skills and expertise saved')
  } catch (err: unknown) {
    const apiErr = parseApiError(err)
    Object.assign(errors, apiErr.fields)
    error.value = apiErr.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="space-y-5" novalidate @submit.prevent="handleSave">
    <div v-if="loadingCatalog" class="py-8 text-center text-sm text-snow-muted">Loading skills catalog...</div>
    <SkillPicker v-else v-model="draft.skills" :catalog="profileStore.skillsCatalog" :error="errors.skills || error" />
    <BaseTextarea id="skills-other" v-model="draft.other_skills" label="Other skills" placeholder="Add skills not listed above, separated by commas..." :maxlength="1000" hint="Optional" :error="errors.other_skills" />
    <div class="grid gap-4 sm:grid-cols-2">
      <BaseSelect id="skills-level" v-model="draft.experience_level" label="Overall experience level" :options="[{value:'beginner',label:'Beginner'},{value:'intermediate',label:'Intermediate'},{value:'advanced',label:'Advanced'}]" placeholder="Select experience level" required :error="errors.experience_level" />
      <BaseInput id="skills-years" v-model="draft.experience_years" type="number" label="Years of experience" placeholder="e.g. 2" :error="errors.experience_years" />
    </div>
    <div class="grid gap-4 sm:grid-cols-2">
      <BaseInput id="skills-portfolio" v-model="draft.portfolio_url" type="url" label="Portfolio URL" placeholder="https://yourportfolio.com" :error="errors.portfolio_url" />
      <BaseInput id="skills-linkedin" v-model="draft.linkedin_url" type="url" label="LinkedIn profile" placeholder="https://linkedin.com/in/your-name" :error="errors.linkedin_url" />
      <BaseInput id="skills-github" v-model="draft.github_url" type="url" label="GitHub profile" placeholder="https://github.com/username" :error="errors.github_url" />
      <BaseSelect id="skills-availability" v-model="draft.availability" label="Availability" :options="AVAILABILITY_OPTIONS" placeholder="Select your availability" required :error="errors.availability" />
    </div>
    <div class="flex items-center justify-between pt-2">
      <BaseButton v-if="props.mode === 'wizard'" type="button" variant="secondary" :disabled="saving" @click="emit('back')">Back</BaseButton>
      <div v-else />
      <BaseButton type="submit" variant="primary" size="md" :loading="saving">{{ props.mode === 'wizard' ? 'Save & continue' : 'Save skills & expertise' }}</BaseButton>
    </div>
  </form>
</template>
