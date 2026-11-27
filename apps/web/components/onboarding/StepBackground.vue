<script setup lang="ts">
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseChipSelect from '~/components/ui/BaseChipSelect.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BaseSelect from '~/components/ui/BaseSelect.vue'
import {
  EDUCATION_OPTIONS,
  OCCUPATION_OPTIONS,
  PRIOR_BUSINESS_OPTIONS,
} from '~/constants/options'
import { stepBackgroundSchema } from '~/schemas/profile'
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

  const parsed = stepBackgroundSchema.safeParse({
    education_level: draft.education_level,
    field_of_study: draft.field_of_study?.trim() || null,
    occupation_status: draft.occupation_status,
    prior_business: draft.prior_business,
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
      education_level: parsed.data.education_level,
      field_of_study: parsed.data.field_of_study || null,
      occupation_status: parsed.data.occupation_status,
      prior_business: parsed.data.prior_business,
    }
    if (props.mode === 'wizard') {
      payload.onboarding_step = 3
    }
    await profileStore.patchProfile(payload)
    if (props.mode === 'wizard') {
      emit('next')
    } else {
      toast.success('Background details saved')
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

    <div class="grid gap-4 sm:grid-cols-2">
      <BaseSelect
        id="bg-education"
        v-model="draft.education_level"
        label="Education level"
        placeholder="Select education level"
        :options="EDUCATION_OPTIONS"
        required
        :error="errors.education_level"
      />

      <BaseInput
        id="bg-field-of-study"
        v-model="draft.field_of_study"
        label="Field of study"
        placeholder="e.g. Computer Science, Commerce"
        hint="Optional (2–80 characters)"
        :error="errors.field_of_study"
      />
    </div>

    <BaseChipSelect
      id="bg-occupation"
      v-model="draft.occupation_status"
      label="Current status"
      :options="OCCUPATION_OPTIONS"
      required
      :error="errors.occupation_status"
    />

    <BaseSelect
      id="bg-work-exp"
      v-model="draft.work_experience"
      label="Work experience"
      placeholder="Select work experience"
      :options="WORK_EXPERIENCE_OPTIONS"
      required
      :error="errors.work_experience"
    />

    <BaseChipSelect
      id="bg-prior-business"
      v-model="draft.prior_business"
      label="Prior business experience"
      :options="PRIOR_BUSINESS_OPTIONS"
      required
      :error="errors.prior_business"
    />

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
        {{ props.mode === 'wizard' ? 'Save & continue' : 'Save background' }}
      </BaseButton>
    </div>
  </form>
</template>
