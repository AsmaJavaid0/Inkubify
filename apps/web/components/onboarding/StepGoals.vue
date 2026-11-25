<script setup lang="ts">
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseChipSelect from '~/components/ui/BaseChipSelect.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BaseSelect from '~/components/ui/BaseSelect.vue'
import {
  INTERESTED_IN_OPTIONS,
  PRIMARY_GOAL_OPTIONS,
  WEEKLY_HOURS_OPTIONS,
} from '~/constants/options'
import { stepGoalsSchema } from '~/schemas/profile'
import { useOnboardingStore } from '~/stores/onboarding'
import { useProfileStore } from '~/stores/profile'
import { parseApiError } from '~/utils/errors'

interface Props {
  mode?: 'wizard' | 'edit'
}

const props = withDefaults(defineProps<Props>(), { mode: 'wizard' })
const emit = defineEmits<{ next: []; back: [] }>()

const onboarding = useOnboardingStore()
const profileStore = useProfileStore()
const toast = useToast()

const draft = onboarding.draft
const errors = reactive<Record<string, string>>({})
const serverError = ref('')
const saving = ref(false)

async function handleSave() {
  serverError.value = ''
  for (const k of Object.keys(errors)) Reflect.deleteProperty(errors, k)

  const parsed = stepGoalsSchema.safeParse({
    primary_goal: draft.primary_goal,
    weekly_hours: draft.weekly_hours,
    interested_in: draft.interested_in,
    instagram_url: draft.instagram_url?.trim() || null,
    linkedin_url: draft.linkedin_url?.trim() || null,
  })

  if (!parsed.success) {
    for (const issue of parsed.error.issues) {
      const k = String(issue.path[0] ?? '')
      if (k && !errors[k]) errors[k] = issue.message
    }
    return
  }

  saving.value = true
  try {
    const payload: Record<string, unknown> = {
      primary_goal: parsed.data.primary_goal,
      weekly_hours: parsed.data.weekly_hours,
      interested_in: parsed.data.interested_in,
      instagram_url: parsed.data.instagram_url ?? null,
      linkedin_url: parsed.data.linkedin_url ?? null,
    }
    if (props.mode === 'wizard') {
      payload.onboarding_step = 5
    }
    const updated = await profileStore.patchProfile(payload)
    draft.instagram_url = updated.instagram_url ?? ''
    draft.linkedin_url = updated.linkedin_url ?? ''
    if (props.mode === 'wizard') {
      emit('next')
    } else {
      toast.success('Goals & availability saved')
    }
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
  <form class="space-y-5" novalidate @submit.prevent="handleSave">
    <div
      v-if="serverError"
      role="alert"
      class="rounded-input border border-danger/50 bg-danger/10 px-3.5 py-2.5 text-sm text-danger"
    >
      {{ serverError }}
    </div>

    <BaseChipSelect
      id="goals-primary"
      v-model="draft.primary_goal"
      label="Primary goal"
      :options="PRIMARY_GOAL_OPTIONS"
      required
      :error="errors.primary_goal"
    />

    <BaseSelect
      id="goals-weekly-hours"
      v-model="draft.weekly_hours"
      label="Weekly time available"
      placeholder="Select hours per week"
      :options="WEEKLY_HOURS_OPTIONS"
      required
      :error="errors.weekly_hours"
    />

    <BaseChipSelect
      id="goals-interested-in"
      v-model="draft.interested_in"
      label="Interested in (optional)"
      :options="INTERESTED_IN_OPTIONS"
      multiple
      hint="Just a hint — you will choose your actual business focus in the next phase"
      :error="errors.interested_in"
    />

    <div class="grid gap-4 sm:grid-cols-2">
      <BaseInput
        id="goals-instagram"
        v-model="draft.instagram_url"
        label="Instagram"
        placeholder="@username or profile URL"
        hint="Optional"
        :error="errors.instagram_url"
      />

      <BaseInput
        id="goals-linkedin"
        v-model="draft.linkedin_url"
        type="url"
        label="LinkedIn"
        placeholder="https://linkedin.com/in/your-name"
        hint="Optional"
        :error="errors.linkedin_url"
      />
    </div>

    <div class="flex items-center justify-between pt-2">
      <BaseButton
        v-if="props.mode === 'wizard'"
        type="button"
        variant="secondary"
        :disabled="saving"
        @click="emit('back')"
      >
        Back
      </BaseButton>
      <div v-else />

      <BaseButton type="submit" variant="primary" size="md" :loading="saving">
        {{ props.mode === 'wizard' ? 'Review profile' : 'Save goals' }}
      </BaseButton>
    </div>
  </form>
</template>
