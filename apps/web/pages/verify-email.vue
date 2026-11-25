<script setup lang="ts">
import { MailCheck } from 'lucide-vue-next'
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import { maskEmail } from '~/utils/phone'

definePageMeta({ layout: 'auth' })

const user = useSupabaseUser()
const supabase = useSupabaseClient()
const { resendVerification } = useAuthActions()
const toast = useToast()

const email = ref('')
const cooldown = ref(0)
const sending = ref(false)
const errorMsg = ref('')
let interval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  const stored = sessionStorage.getItem('inkubify_pending_email') || user.value?.email || ''
  email.value = stored
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})

const masked = computed(() => (email.value ? maskEmail(email.value) : ''))

function startCooldown() {
  cooldown.value = 60
  if (interval) clearInterval(interval)
  interval = setInterval(() => {
    cooldown.value -= 1
    if (cooldown.value <= 0 && interval) {
      clearInterval(interval)
      interval = null
    }
  }, 1000)
}

async function handleResend() {
  errorMsg.value = ''
  if (!email.value.trim()) {
    errorMsg.value = 'Please enter your email address first.'
    return
  }
  sending.value = true
  try {
    await resendVerification(email.value)
    toast.success('Verification email sent. Please check your inbox.')
    startCooldown()
  } catch (err: unknown) {
    errorMsg.value = err instanceof Error ? err.message : 'Unable to resend verification email.'
  } finally {
    sending.value = false
  }
}

async function useDifferentEmail() {
  sessionStorage.removeItem('inkubify_pending_email')
  if (user.value) {
    await supabase.auth.signOut()
  }
  await navigateTo('/signup')
}
</script>

<template>
  <div class="space-y-6 text-center">
    <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-card bg-gold-500/15 text-gold-500">
      <MailCheck class="h-7 w-7" aria-hidden="true" />
    </div>

    <div class="space-y-2">
      <h1 class="text-2xl font-bold tracking-tight text-snow-100">
        Check your email
      </h1>
      <p class="text-sm leading-relaxed text-snow-muted">
        <template v-if="masked">
          We sent a verification link to <strong class="text-snow-100">{{ masked }}</strong>.
          Open the link to verify your account and continue.
        </template>
        <template v-else>
          We sent a verification link to your email address. Open the link to verify your account.
        </template>
      </p>
    </div>

    <div v-if="!masked" class="text-left">
      <BaseInput
        id="verify-email-input"
        v-model="email"
        type="email"
        label="Email address"
        placeholder="you@example.com"
      />
    </div>

    <p v-if="errorMsg" role="alert" class="text-xs font-medium text-danger">
      {{ errorMsg }}
    </p>

    <div class="space-y-3">
      <BaseButton
        variant="primary"
        size="lg"
        block
        :loading="sending"
        :disabled="cooldown > 0"
        @click="handleResend"
      >
        {{ cooldown > 0 ? `Resend available in ${cooldown}s` : 'Resend verification email' }}
      </BaseButton>

      <BaseButton variant="secondary" size="md" block @click="useDifferentEmail">
        Use a different email
      </BaseButton>
    </div>

    <p class="text-xs text-snow-muted">
      Already confirmed?
      <NuxtLink to="/login" class="font-semibold text-gold-500 hover:underline">
        Log in
      </NuxtLink>
    </p>
  </div>
</template>
