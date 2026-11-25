<script setup lang="ts">
import StepBackground from '~/components/onboarding/StepBackground.vue'
import StepGoals from '~/components/onboarding/StepGoals.vue'
import StepPersonal from '~/components/onboarding/StepPersonal.vue'
import StepReview from '~/components/onboarding/StepReview.vue'
import StepSkills from '~/components/onboarding/StepSkills.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseStepper from '~/components/ui/BaseStepper.vue'
import { WIZARD_STEPS } from '~/constants/options'
import { useOnboardingStore } from '~/stores/onboarding'
import { useProfileStore } from '~/stores/profile'

definePageMeta({ layout: 'onboarding' })

const route = useRoute()
const router = useRouter()
const profileStore = useProfileStore()
const onboarding = useOnboardingStore()

const loadError = ref('')
const loading = ref(true)

async function loadWizardState() {
  loading.value = true
  loadError.value = ''
  try {
    const profile = await profileStore.fetchProfile(true)
    if (!profile) {
      loadError.value = profileStore.error || 'Could not load your profile. Please retry.'
      return
    }
    onboarding.hydrateFromProfile(profile)
    const queryStep = Number(route.query.step)
    const savedStep = Math.min(5, Math.max(1, profile.onboarding.step || 1))
    if (queryStep >= 1 && queryStep <= savedStep) {
      onboarding.currentStep = queryStep
    } else {
      onboarding.currentStep = savedStep
      await router.replace({ query: { step: String(savedStep) } })
    }
  } finally {
    loading.value = false
  }
}

onMounted(loadWizardState)

function goToStep(step: number) {
  const maxAllowed = Math.max(onboarding.currentStep, profileStore.profile?.onboarding.step || 1)
  if (step < 1 || step > 5 || step > maxAllowed) return
  onboarding.currentStep = step
  router.replace({ query: { step: String(step) } })
}

const currentMeta = computed(() => WIZARD_STEPS[onboarding.currentStep - 1]!)
const completionPct = computed(() => profileStore.profile?.profile_completion ?? 0)
const maxCompletedStep = computed(() => profileStore.profile?.onboarding.step ?? 1)
</script>

<template>
  <div class="space-y-6">
    <div v-if="loading" class="rounded-card border border-navy-border bg-navy-700 p-8 text-center text-sm text-snow-muted">
      Loading your founder profile...
    </div>

    <div
      v-else-if="loadError"
      class="space-y-4 rounded-card border border-danger/50 bg-navy-700 p-6 text-center"
    >
      <p class="text-sm text-danger">{{ loadError }}</p>
      <BaseButton variant="primary" @click="loadWizardState">
        Retry
      </BaseButton>
    </div>

    <template v-else>
      <div class="space-y-4 rounded-card border border-navy-border bg-navy-700 p-5 sm:p-6">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-gold-500">
              Step {{ onboarding.currentStep }} of 5
            </p>
            <h1 class="text-xl font-bold text-snow-100">
              {{ currentMeta.title }}
            </h1>
          </div>

          <div class="text-right">
            <p class="text-xs text-snow-muted">Profile completion</p>
            <p class="text-sm font-bold text-gold-500">{{ completionPct }}%</p>
          </div>
        </div>

        <div class="h-1.5 w-full overflow-hidden rounded-full bg-navy-900/70" aria-hidden="true">
          <div
            class="h-full rounded-full bg-gold-500 transition-all"
            :style="{ width: `${completionPct}%` }"
          />
        </div>

        <BaseStepper
          :steps="WIZARD_STEPS"
          :current-step="onboarding.currentStep"
          :max-completed-step="maxCompletedStep"
          @select="goToStep"
        />
      </div>

      <div class="rounded-card border border-navy-border bg-navy-700 p-6 sm:p-8">
        <StepPersonal v-if="onboarding.currentStep === 1" @next="goToStep(2)" />
        <StepBackground
          v-else-if="onboarding.currentStep === 2"
          @back="goToStep(1)"
          @next="goToStep(3)"
        />
        <StepSkills
          v-else-if="onboarding.currentStep === 3"
          @back="goToStep(2)"
          @next="goToStep(4)"
        />
        <StepGoals
          v-else-if="onboarding.currentStep === 4"
          @back="goToStep(3)"
          @next="goToStep(5)"
        />
        <StepReview
          v-else
          @back="goToStep(4)"
          @edit-step="goToStep"
        />
      </div>
    </template>
  </div>
</template>
