<script setup lang="ts">
import AppLogo from '~/components/brand/AppLogo.vue'
import { useProfileStore } from '~/stores/profile'

definePageMeta({ layout: false })

const user = useSupabaseUser()
const profileStore = useProfileStore()

onMounted(async () => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const delayMs = reducedMotion ? 150 : 1500

  await new Promise((resolve) => setTimeout(resolve, delayMs))

  if (!user.value) {
    const hasVisited = localStorage.getItem('inkubify_visited') === '1'
    if (hasVisited) {
      await navigateTo('/login', { replace: true })
    } else {
      localStorage.setItem('inkubify_visited', '1')
      await navigateTo('/welcome', { replace: true })
    }
    return
  }

  const isVerified = Boolean(user.value.email_confirmed_at || user.value.confirmed_at)
  if (!isVerified) {
    await navigateTo('/verify-email', { replace: true })
    return
  }

  const profile = await profileStore.fetchProfile()
  if (profile?.onboarding.status === 'completed') {
    await navigateTo('/dashboard', { replace: true })
  } else {
    await navigateTo('/onboarding/profile', { replace: true })
  }
})
</script>

<template>
  <main class="flex min-h-screen items-center justify-center bg-navy-900 px-6">
    <div class="animate-fade-in">
      <AppLogo size="splash" />
    </div>
  </main>
</template>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.97);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out both;
}
</style>
