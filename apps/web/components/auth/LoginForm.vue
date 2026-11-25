<script setup lang="ts">
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BasePasswordInput from '~/components/ui/BasePasswordInput.vue'
import { loginSchema } from '~/schemas/auth'
import { useProfileStore } from '~/stores/profile'

const { signIn } = useAuthActions()
const profileStore = useProfileStore()

const form = reactive({
  email: '',
  password: '',
})

const errors = reactive<Record<string, string>>({})
const formError = ref('')
const needsVerification = ref(false)
const submitting = ref(false)

function validateField(field: keyof typeof form) {
  const parsed = loginSchema.safeParse(form)
  if (parsed.success) {
    Reflect.deleteProperty(errors, field)
    return
  }
  const issue = parsed.error.issues.find((i) => i.path[0] === field)
  if (issue) {
    errors[field] = issue.message
  } else {
    Reflect.deleteProperty(errors, field)
  }
}

async function handleSubmit() {
  formError.value = ''
  needsVerification.value = false
  const parsed = loginSchema.safeParse(form)

  if (!parsed.success) {
    for (const issue of parsed.error.issues) {
      const k = String(issue.path[0] ?? '')
      if (k) errors[k] = issue.message
    }
    return
  }

  submitting.value = true
  try {
    await signIn(parsed.data.email, parsed.data.password)
    const profile = await profileStore.fetchProfile(true)
    if (profile?.onboarding.status === 'completed') {
      await navigateTo('/dashboard')
    } else {
      await navigateTo('/onboarding/profile')
    }
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : 'Invalid email or password.'
    formError.value = msg
    if (msg.toLowerCase().includes('verify your email')) {
      needsVerification.value = true
      sessionStorage.setItem('inkubify_pending_email', parsed.data.email)
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form class="space-y-4" novalidate @submit.prevent="handleSubmit">
    <div
      v-if="formError"
      role="alert"
      aria-live="polite"
      class="space-y-2 rounded-input border border-danger/50 bg-danger/10 px-3.5 py-2.5 text-sm text-danger"
    >
      <p>{{ formError }}</p>
      <NuxtLink
        v-if="needsVerification"
        to="/verify-email"
        class="inline-block font-semibold text-gold-500 underline"
      >
        Resend verification email →
      </NuxtLink>
    </div>

    <BaseInput
      id="login-email"
      v-model="form.email"
      type="email"
      label="Email address"
      placeholder="you@example.com"
      autocomplete="email"
      required
      :error="errors.email"
      @blur="validateField('email')"
    />

    <div class="space-y-1">
      <BasePasswordInput
        id="login-password"
        v-model="form.password"
        label="Password"
        placeholder="Enter your password"
        autocomplete="current-password"
        required
        :error="errors.password"
        @blur="validateField('password')"
      />
      <div class="flex justify-end">
        <NuxtLink
          to="/forgot-password"
          class="text-xs font-medium text-gold-500 hover:underline"
        >
          Forgot password?
        </NuxtLink>
      </div>
    </div>

    <BaseButton
      type="submit"
      variant="primary"
      size="lg"
      block
      :loading="submitting"
    >
      Log in
    </BaseButton>
  </form>
</template>
