<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import { useProfileStore } from '~/stores/profile'

definePageMeta({ layout: 'auth' })

const route = useRoute()
const supabase = useSupabaseClient()
const user = useSupabaseUser()
const profileStore = useProfileStore()
const { resendVerification } = useAuthActions()
const toast = useToast()

const status = ref<'verifying' | 'error'>('verifying')
const errorMessage = ref('')
const resendEmail = ref('')
const resending = ref(false)

onMounted(async () => {
  resendEmail.value = sessionStorage.getItem('inkubify_pending_email') || ''

  try {
    const tokenHash = route.query.token_hash as string | undefined
    const type = route.query.type as string | undefined
    const code = route.query.code as string | undefined
    const urlError = route.query.error_description as string | undefined

    if (urlError) {
      throw new Error(urlError)
    }

    if (tokenHash && type) {
      const { error } = await supabase.auth.verifyOtp({
        token_hash: tokenHash,
        type: type as 'signup' | 'recovery' | 'email',
      })
      if (error) throw error
    } else if (code) {
      const { error } = await supabase.auth.exchangeCodeForSession(code)
      if (error) throw error
    } else {
      // Allow @nuxtjs/supabase hash/session listener to settle briefly
      await new Promise((resolve) => setTimeout(resolve, 400))
    }

    const { data: sessionData } = await supabase.auth.getSession()
    if (!sessionData.session && !user.value) {
      throw new Error('This verification link is invalid or has expired.')
    }

    sessionStorage.removeItem('inkubify_pending_email')
    const profile = await profileStore.fetchProfile(true)
    if (profile?.onboarding.status === 'completed') {
      await navigateTo('/dashboard', { replace: true })
    } else {
      await navigateTo('/onboarding/profile', { replace: true })
    }
  } catch (err: unknown) {
    status.value = 'error'
    errorMessage.value =
      err instanceof Error
        ? err.message
        : 'This verification link is invalid or has expired.'
  }
})

async function handleResend() {
  if (!resendEmail.value.trim()) return
  resending.value = true
  try {
    await resendVerification(resendEmail.value)
    toast.success('A new verification link has been sent.')
  } catch (err: unknown) {
    errorMessage.value = err instanceof Error ? err.message : 'Unable to resend link.'
  } finally {
    resending.value = false
  }
}
</script>

<template>
  <div class="space-y-6 text-center">
    <template v-if="status === 'verifying'">
      <Loader2 class="mx-auto h-10 w-10 animate-spin text-gold-500" aria-hidden="true" />
      <div class="space-y-1">
        <h1 class="text-xl font-bold text-snow-100">Confirming your email...</h1>
        <p class="text-sm text-snow-muted">Just a moment while we set up your session.</p>
      </div>
    </template>

    <template v-else>
      <div class="space-y-2">
        <h1 class="text-xl font-bold text-snow-100">Verification link expired or invalid</h1>
        <p class="text-sm text-danger">{{ errorMessage }}</p>
      </div>

      <div class="space-y-3 text-left">
        <BaseInput
          id="confirm-resend-email"
          v-model="resendEmail"
          type="email"
          label="Email address"
          placeholder="you@example.com"
        />
        <BaseButton
          variant="primary"
          size="md"
          block
          :loading="resending"
          :disabled="!resendEmail.trim()"
          @click="handleResend"
        >
          Resend verification email
        </BaseButton>
        <BaseButton variant="secondary" size="md" block @click="navigateTo('/login')">
          Go to log in
        </BaseButton>
      </div>
    </template>
  </div>
</template>
