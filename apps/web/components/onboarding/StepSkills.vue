<script setup lang="ts">
import SkillPicker from '~/components/onboarding/SkillPicker.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import { stepSkillsSchema } from '~/schemas/profile'
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
const error = ref('')
const saving = ref(false)
const loadingCatalog = ref(false)

onMounted(async () => {
  if (profileStore.skillsCatalog.length === 0) {
    loadingCatalog.value = true
    try {
      await profileStore.fetchSkillsCatalog()
    } finally {
      loadingCatalog.value = false
    }
  }
})

async function handleSave() {
  error.value = ''
  const parsed = stepSkillsSchema.safeParse({ skills: draft.skills })
  if (!parsed.success) {
    error.value = parsed.error.issues[0]?.message ?? 'Please select at least 1 skill'
    return
  }

  saving.value = true
  try {
    await profileStore.replaceSkills(parsed.data.skills)
    if (props.mode === 'wizard') {
      await profileStore.patchProfile({ onboarding_step: 4 })
      emit('next')
    } else {
      toast.success('Skills updated')
    }
  } catch (err: unknown) {
    const apiErr = parseApiError(err)
    error.value = apiErr.fields.skills || apiErr.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="space-y-5" novalidate @submit.prevent="handleSave">
    <div v-if="loadingCatalog" class="py-8 text-center text-sm text-snow-muted">
      Loading skills catalog...
    </div>

    <SkillPicker
      v-else
      v-model="draft.skills"
      :catalog="profileStore.skillsCatalog"
      :error="error"
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
        {{ props.mode === 'wizard' ? 'Save & continue' : 'Save skills' }}
      </BaseButton>
    </div>
  </form>
</template>
