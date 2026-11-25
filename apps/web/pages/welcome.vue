<script setup lang="ts">
import AppLogo from '~/components/brand/AppLogo.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import WelcomeSlide from '~/components/welcome/WelcomeSlide.vue'
import { WELCOME_SLIDES } from '~/constants/options'

definePageMeta({ layout: false })

const currentIndex = ref(0)
const isLast = computed(() => currentIndex.value === WELCOME_SLIDES.length - 1)
const currentSlide = computed(() => WELCOME_SLIDES[currentIndex.value]!)

onMounted(() => {
  localStorage.setItem('inkubify_visited', '1')
})

function nextSlide() {
  if (!isLast.value) {
    currentIndex.value++
  }
}

async function skip() {
  await navigateTo('/signup')
}
</script>

<template>
  <main class="flex min-h-screen flex-col items-center justify-between bg-navy-900 px-4 py-8 text-snow-100">
    <header class="flex w-full max-w-[480px] items-center justify-between">
      <AppLogo size="sm" />
      <BaseButton v-if="!isLast" variant="ghost" size="sm" @click="skip">
        Skip
      </BaseButton>
    </header>

    <section class="w-full max-w-[480px] rounded-card border border-navy-border bg-navy-700 p-8 shadow-xl">
      <WelcomeSlide
        :title="currentSlide.title"
        :description="currentSlide.description"
        :step-index="currentIndex"
      />

      <div class="mt-8 flex items-center justify-center gap-2" role="tablist" aria-label="Welcome slides">
        <button
          v-for="(slide, idx) in WELCOME_SLIDES"
          :key="slide.title"
          type="button"
          role="tab"
          :aria-selected="idx === currentIndex"
          :aria-label="`Slide ${idx + 1}: ${slide.title}`"
          class="h-2 rounded-full transition-all"
          :class="idx === currentIndex ? 'w-7 bg-gold-500' : 'w-2 bg-snow-100/25 hover:bg-snow-100/45'"
          @click="currentIndex = idx"
        />
      </div>

      <div class="mt-8 space-y-3">
        <template v-if="isLast">
          <BaseButton variant="primary" size="lg" block @click="navigateTo('/signup')">
            Get started
          </BaseButton>
          <BaseButton variant="secondary" size="md" block @click="navigateTo('/login')">
            I already have an account
          </BaseButton>
        </template>
        <template v-else>
          <BaseButton variant="primary" size="lg" block @click="nextSlide">
            Next
          </BaseButton>
        </template>
      </div>
    </section>

    <footer class="text-xs text-snow-muted">
      Ideas → Plans → Reality
    </footer>
  </main>
</template>
