<script setup lang="ts">
import AppLogo from '~/components/brand/AppLogo.vue'
import BaseButton from '~/components/ui/BaseButton.vue'

const user = useSupabaseUser()
const { signOut } = useAuthActions()
const signingOut = ref(false)

async function handleSignOut() {
  signingOut.value = true
  try {
    await signOut()
  } finally {
    signingOut.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen flex-col bg-navy-900 text-snow-100">
    <header class="border-b border-navy-border bg-navy-900/90 backdrop-blur">
      <div class="mx-auto flex max-w-4xl items-center justify-between px-4 py-3.5 sm:px-6">
        <NuxtLink to="/dashboard" aria-label="Inkubify home">
          <AppLogo size="sm" />
        </NuxtLink>

        <nav v-if="user" class="flex items-center gap-3">
          <NuxtLink
            to="/dashboard"
            class="rounded-btn px-3 py-1.5 text-sm font-medium text-snow-muted transition-colors hover:text-snow-100"
            active-class="!text-gold-500"
          >
            Dashboard
          </NuxtLink>
          <NuxtLink
            to="/profile"
            class="rounded-btn px-3 py-1.5 text-sm font-medium text-snow-muted transition-colors hover:text-snow-100"
            active-class="!text-gold-500"
          >
            Profile
          </NuxtLink>
          <BaseButton
            variant="secondary"
            size="sm"
            :loading="signingOut"
            @click="handleSignOut"
          >
            Log out
          </BaseButton>
        </nav>
      </div>
    </header>

    <main class="mx-auto w-full max-w-4xl flex-1 px-4 py-8 sm:px-6">
      <slot />
    </main>
  </div>
</template>
