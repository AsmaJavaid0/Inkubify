<script setup lang="ts">
import StepBackground from '~/components/onboarding/StepBackground.vue'
import StepGoals from '~/components/onboarding/StepGoals.vue'
import StepPersonal from '~/components/onboarding/StepPersonal.vue'
import StepSkills from '~/components/onboarding/StepSkills.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import { useOnboardingStore } from '~/stores/onboarding'
import { useProfileStore } from '~/stores/profile'

const profileStore = useProfileStore()
const onboarding = useOnboardingStore()

const loading = ref(true)
const errorMsg = ref('')

async function loadProfile() {
  loading.value = true
  errorMsg.value = ''
  try {
    const p = await profileStore.fetchProfile(true)
    if (!p) {
      errorMsg.value = profileStore.error || 'Unable to load profile.'
      return
    }
    onboarding.hydrateFromProfile(p)
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold text-snow-100">Founder Profile</h1>
        <p class="text-sm text-snow-muted">
          Username (<span class="font-medium text-snow-100">@{{ profileStore.profile?.username }}</span>)
          and phone number cannot be changed here.
        </p>
      </div>

      <div v-if="profileStore.profile" class="rounded-input border border-navy-border bg-navy-700 px-4 py-2 text-right">
        <p class="text-xs text-snow-muted">Completion</p>
        <p class="text-sm font-bold text-gold-500">{{ profileStore.profile.profile_completion }}%</p>
      </div>
    </div>

    <div v-if="loading" class="rounded-card border border-navy-border bg-navy-700 p-8 text-center text-sm text-snow-muted">
      Loading your profile...
    </div>

    <div v-else-if="errorMsg" class="space-y-3 rounded-card border border-danger/50 bg-navy-700 p-6 text-center">
      <p class="text-sm text-danger">{{ errorMsg }}</p>
      <BaseButton variant="primary" @click="loadProfile">Retry</BaseButton>
    </div>

    <template v-else>
      <section class="space-y-4 rounded-card border border-navy-border bg-navy-700 p-6">
        <h2 class="text-lg font-semibold text-gold-500">Personal details</h2>
        <StepPersonal mode="edit" />
      </section>

      <section class="space-y-4 rounded-card border border-navy-border bg-navy-700 p-6">
        <h2 class="text-lg font-semibold text-gold-500">Education &amp; background</h2>
        <StepBackground mode="edit" />
      </section>

      <section class="space-y-4 rounded-card border border-navy-border bg-navy-700 p-6">
        <h2 class="text-lg font-semibold text-gold-500">Skills &amp; expertise</h2>
        <StepSkills mode="edit" />
      </section>

      <section class="space-y-4 rounded-card border border-navy-border bg-navy-700 p-6">
        <h2 class="text-lg font-semibold text-gold-500">Business interests &amp; resources</h2>
        <StepGoals mode="edit" />
      </section>
    </template>
  </div>
</template>
