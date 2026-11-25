<script setup lang="ts">
import PasswordStrength from '~/components/auth/PasswordStrength.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import BasePasswordInput from '~/components/ui/BasePasswordInput.vue'
import { resetPasswordSchema } from '~/schemas/auth'

definePageMeta({ layout: 'auth' })

const supabase = useSupabaseClient()
const { updatePassword } = useAuthActions()
const toast = useToast()

const form = reactive({
  password: '',
  confirm_password: '',
})
const errors = reactive<Record<string, string>>({})
const formError = ref('')
const loading = ref(false)

async function handleSubmit() {
  formError.value = ''
  const parsed = resetPasswordSchema.safeParse(form)
  if (!parsed.success) {
    for (const key of ['password', 'confirm_password']) Reflect.deleteProperty(errors, key)
    for (const issue of parsed.error.issues) {
      const k = String(issue.path[0] ?? '')
      if (k) errors[k] = issue.message
    }
    return
  }

  loading.value = true
  try {
    await updatePassword(parsed.data.password)
    await supabase.auth.signOut()
    toast.success('Password updated. Please log in with your new password.')
    await navigateTo('/login')
  } catch (err: unknown) {
    formError.value = err instanceof Error ? err.message : 'Unable to reset password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="space-y-1.5 text-center">
      <h1 class="text-2xl font-bold tracking-tight text-snow-100">
        Set a new password
      </h1>
      <p class="text-sm text-snow-muted">
        Choose a strong password for your Inkubify account
      </p>
    </div>

    <form class="space-y-4" novalidate @submit.prevent="handleSubmit">
      <div
        v-if="formError"
        role="alert"
        class="rounded-input border border-danger/50 bg-danger/10 px-3.5 py-2.5 text-sm text-danger"
      >
        {{ formError }}
      </div>

      <div class="space-y-1">
        <BasePasswordInput
          id="reset-password"
          v-model="form.password"
          label="New password"
          autocomplete="new-password"
          required
          :error="errors.password"
        />
        <PasswordStrength :password="form.password" />
      </div>

      <BasePasswordInput
        id="reset-confirm"
        v-model="form.confirm_password"
        label="Confirm new password"
        autocomplete="new-password"
        required
        :error="errors.confirm_password"
      />

      <BaseButton type="submit" variant="primary" size="lg" block :loading="loading">
        Update password
      </BaseButton>
    </form>
  </div>
</template>
