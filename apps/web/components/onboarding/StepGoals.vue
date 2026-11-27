<script setup lang="ts">
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BaseSelect from '~/components/ui/BaseSelect.vue'
import BaseTextarea from '~/components/ui/BaseTextarea.vue'
import SearchableMultiSelect from '~/components/ui/SearchableMultiSelect.vue'
import {
  AVAILABLE_RESOURCE_OPTIONS, BUSINESS_CATEGORY_OPTIONS, BUSINESS_TIMELINE_OPTIONS,
  ECOMMERCE_MODEL_OPTIONS, RESOURCE_INFO_OPTIONS, TARGET_AUDIENCE_OPTIONS,
  TECHNOLOGY_MODEL_OPTIONS,
} from '~/constants/options'
import { stepGoalsSchema } from '~/schemas/profile'
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
const serverError = ref('')
const saving = ref(false)
const businessModelOptions = computed(() => {
  if (draft.business_category === 'ecommerce') return ECOMMERCE_MODEL_OPTIONS
  if (draft.business_category === 'technology_based') return TECHNOLOGY_MODEL_OPTIONS
  return []
})
function handleCategoryChange(value: string) {
  draft.business_category = value as 'ecommerce' | 'technology_based' | ''
  if (!businessModelOptions.value.some((option) => option.value === draft.business_model)) draft.business_model = ''
  delete errors.business_category
  delete errors.business_model
}
async function handleSave() {
  serverError.value = ''
  for (const key of Object.keys(errors)) delete errors[key]
  const parsed = stepGoalsSchema.safeParse({
    business_category: draft.business_category, business_model: draft.business_model,
    target_audience: draft.target_audience, primary_goal: draft.primary_goal,
    expected_business_timeline: draft.expected_business_timeline,
    available_budget_pkr: draft.available_budget_pkr, available_resources: draft.available_resources,
    team_members: draft.team_members, resource_info: draft.resource_info,
  })
  if (!parsed.success) {
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? '')
      if (key && !errors[key]) errors[key] = issue.message
    }
    return
  }
  saving.value = true
  try {
    const payload: Record<string, unknown> = {
      business_category: parsed.data.business_category, business_model: parsed.data.business_model,
      target_audience: parsed.data.target_audience, primary_goal: parsed.data.primary_goal,
      expected_business_timeline: parsed.data.expected_business_timeline,
      available_budget_pkr: parsed.data.available_budget_pkr,
      available_resources: parsed.data.available_resources, team_members: parsed.data.team_members,
      resource_info: parsed.data.resource_info,
    }
    if (props.mode === 'wizard') payload.onboarding_step = 5
    await profileStore.patchProfile(payload)
    if (props.mode === 'wizard') emit('next')
    else toast.success('Business interests and resources saved')
  } catch (err: unknown) {
    const apiErr = parseApiError(err)
    Object.assign(errors, apiErr.fields)
    serverError.value = apiErr.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="space-y-6" novalidate @submit.prevent="handleSave">
    <div v-if="serverError" role="alert" class="rounded-input border border-danger/50 bg-danger/10 px-3.5 py-2.5 text-sm text-danger">{{ serverError }}</div>
    <section class="space-y-4">
      <h3 class="text-sm font-semibold text-gold-500">Business Interests</h3>
      <div class="grid gap-4 sm:grid-cols-2">
        <BaseSelect id="business-category" :model-value="draft.business_category" label="Business category" :options="BUSINESS_CATEGORY_OPTIONS" placeholder="Select a category" required :error="errors.business_category" @update:model-value="handleCategoryChange" />
        <BaseSelect id="business-model" v-model="draft.business_model" label="Business model" :options="businessModelOptions" placeholder="Select a model" :disabled="!draft.business_category" required :error="errors.business_model" />
      </div>
      <SearchableMultiSelect id="target-audience" v-model="draft.target_audience" label="Target audience" :options="TARGET_AUDIENCE_OPTIONS" placeholder="Search target audiences..." hint="Select all audiences relevant to your idea." />
      <BaseTextarea id="business-goal" v-model="draft.primary_goal" label="Primary goal" placeholder="Describe what you want to build, the problem you want to solve, and what you hope to achieve..." :maxlength="500" required :error="errors.primary_goal" />
      <BaseSelect id="business-timeline" v-model="draft.expected_business_timeline" label="Expected business timeline" :options="BUSINESS_TIMELINE_OPTIONS" placeholder="When do you plan to start?" required :error="errors.expected_business_timeline" />
    </section>
    <section class="space-y-4 border-t border-navy-border pt-5">
      <h3 class="text-sm font-semibold text-gold-500">Financial &amp; Resource Information</h3>
      <div class="grid gap-4 sm:grid-cols-2">
        <BaseInput id="available-budget" v-model="draft.available_budget_pkr" type="number" min="0" max="1000000000000" label="Available budget (PKR) placeholder="e.g. 100000" :error="errors.available_budget_pkr" />
        <BaseInput id="team-members" v-model="draft.team_members" type="number" label="Current team members" placeholder="Enter number (0 if solo)" :error="errors.team_members" />
      </div>
      <SearchableMultiSelect id="available-resources" v-model="draft.available_resources" label="Available resources" :options="AVAILABLE_RESOURCE_OPTIONS" placeholder="Search available resources..." />
      <SearchableMultiSelect id="resource-info" v-model="draft.resource_info" label="Financial support / resource information" :options="RESOURCE_INFO_OPTIONS" placeholder="Search funding or support sources..." hint="Select all sources currently available to you." />
    </section>
    <div class="flex items-center justify-between pt-2">
      <BaseButton v-if="props.mode === 'wizard'" type="button" variant="secondary" :disabled="saving" @click="emit('back')">Back</BaseButton>
      <div v-else />
      <BaseButton type="submit" variant="primary" size="md" :loading="saving">{{ props.mode === 'wizard' ? 'Review profile' : 'Save business & resources' }}</BaseButton>
    </div>
  </form>
</template>
