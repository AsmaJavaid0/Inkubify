<script setup lang="ts">
import BaseButton from '~/components/ui/BaseButton.vue'
import { useProfileStore } from '~/stores/profile'

const profileStore = useProfileStore()

onMounted(async () => {
  await profileStore.fetchProfile()
})

const completion = computed(() => profileStore.profile?.profile_completion ?? 0)
</script>

<template>
  <div class="space-y-6">
    <section class="rounded-card border border-navy-border bg-navy-700 p-6 sm:p-8">
      <p class="text-xs font-semibold uppercase tracking-wider text-gold-500">
        Founder Dashboard
      </p>
      <h1 class="mt-1 text-2xl font-bold text-snow-100">
        Welcome, {{ profileStore.firstName }}
      </h1>
      <p class="mt-1 text-sm text-snow-muted">
        Ideas → Plans → Reality
      </p>
    </section>

    <div class="grid gap-6 md:grid-cols-2">
      <section class="flex flex-col justify-between space-y-4 rounded-card border border-navy-border bg-navy-700 p-6">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-snow-100">Founder profile</h2>
            <span class="text-sm font-bold text-gold-500">{{ completion }}%</span>
          </div>
          <div class="h-2 w-full overflow-hidden rounded-full bg-navy-900/70" aria-hidden="true">
            <div
              class="h-full rounded-full bg-gold-500 transition-all"
              :style="{ width: `${completion}%` }"
            />
          </div>
          <p class="text-sm text-snow-muted">
            Keep your skills, background, and availability updated so your future roadmap stays
            tailored to you.
          </p>
        </div>

        <div>
          <BaseButton variant="secondary" size="md" @click="navigateTo('/profile')">
            Edit founder profile
          </BaseButton>
        </div>
      </section>

      <section class="flex flex-col justify-between space-y-4 rounded-card border border-dashed border-navy-border bg-navy-700/60 p-6">
        <div class="space-y-2">
          <span class="inline-block rounded-full bg-gold-500/15 px-2.5 py-0.5 text-xs font-semibold text-gold-500">
            Phase 2
          </span>
          <h2 class="text-lg font-semibold text-snow-100">Business profile coming next</h2>
          <p class="text-sm text-snow-muted">
            Next up: tell Inkubify about the e-commerce or tech business you want to start, your
            budget, and your team to generate your roadmap.
          </p>
        </div>
      </section>
    </div>
  </div>
</template>
