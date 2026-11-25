<script setup lang="ts">
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import { forgotPasswordSchema } from '~/schemas/auth'

definePageMeta({ layout: 'auth' })

const { requestPasswordReset } = useAuthActions()

const email = ref('')
const error = ref('')
const submitted = ref(false)
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  const parsed = forgotPasswordSchema.safeParse({ email: email.value })
  if (!parsed.success) {
    error.value = parsed.error.issues[0]?.message ?? 'Please enter a valid email'
    return
  }

  loading.value = true
  try {
    await requestPasswordReset(parsed.data.email)
  } catch {
    // Intentionally show the same generic confirmation to prevent email enumeration (§6.5)
  } finally {
    loading.value = false
    submitted.value = true
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="space-y-1.5 text-center">
      <h1 class="text-2xl font-bold tracking-tight text-snow-100">
        Forgot password
      </h1>
      <p class="text-sm text-snow-muted">
        Enter your email and we will send you a reset link
      </p>
    </div>

    <div
      v-if="submitted"
      role="status"
      class="space-y-4 rounded-input border border-gold-500/40 bg-gold-500/10 p-4 text-center text-sm text-snow-100"
    >
      <p>If that email exists, we sent a password reset link. Please check your inbox.</p>
      <BaseButton variant="secondary" size="md" block @click="navigateTo('/login')">
        Back to log in
      </BaseButton>
    </div>

    <form v-else class="space-y-4" novalidate @submit.prevent="handleSubmit">
      <BaseInput
        id="forgot-email"
        v-model="email"
        type="email"
        label="Email address"
        placeholder="you@example.com"
        autocomplete="email"
        required
        :error="error"
      />

      <BaseButton type="submit" variant="primary" size="lg" block :loading="loading">
        Send reset link
      </BaseButton>

      <p class="text-center text-sm text-snow-muted">
        <NuxtLink to="/login" class="font-medium text-gold-500 hover:underline">
          Back to log in
        </NuxtLink>
      </p>
    </form>
  </div>
</template>
