<script setup lang="ts">
import AppLogo from '~/components/brand/AppLogo.vue'
import BaseButton from '~/components/ui/BaseButton.vue'

const { signOut } = useAuthActions()
const toast = useToast()
const signingOut = ref(false)

async function handleSignOut() {
  signingOut.value = true
  try {
    toast.info('Your progress is saved. Log back in anytime to continue.')
    await signOut()
  } finally {
    signingOut.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen flex-col bg-navy-900 text-snow-100">
    <header class="border-b border-navy-border">
      <div class="mx-auto flex max-w-[720px] items-center justify-between px-4 py-3.5 sm:px-6">
        <AppLogo size="sm" />
        <BaseButton
          variant="ghost"
          size="sm"
          :loading="signingOut"
          @click="handleSignOut"
        >
          Save &amp; continue later
        </BaseButton>
      </div>
    </header>

    <main class="mx-auto w-full max-w-[720px] flex-1 px-4 py-6 sm:px-6 sm:py-8">
      <slot />
    </main>
  </div>
</template>
