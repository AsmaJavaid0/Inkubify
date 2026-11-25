<script setup lang="ts">
import { Check, Loader2, X } from 'lucide-vue-next'
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseCheckbox from '~/components/ui/BaseCheckbox.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BasePasswordInput from '~/components/ui/BasePasswordInput.vue'
import BasePhoneInput from '~/components/ui/BasePhoneInput.vue'
import BaseSelect from '~/components/ui/BaseSelect.vue'
import PasswordStrength from '~/components/auth/PasswordStrength.vue'
import { signUpSchema } from '~/schemas/auth'

const { signUp } = useAuthActions()
const { status: usernameStatus, message: usernameHint, check: checkUsername } = useUsernameCheck()

const form = reactive({
  full_name: '',
  username: '',
  email: '',
  phone: '',
  country_code: 'PK',
  password: '',
  confirm_password: '',
  accept_terms: false,
})

const touched = reactive<Record<string, boolean>>({})
const errors = reactive<Record<string, string>>({})
const formError = ref('')
const submitting = ref(false)

const fullNameRef = ref<{ focus: () => void } | null>(null)
const usernameRef = ref<{ focus: () => void } | null>(null)
const emailRef = ref<{ focus: () => void } | null>(null)
const phoneRef = ref<{ focus: () => void } | null>(null)
const passwordRef = ref<{ focus: () => void } | null>(null)
const confirmPasswordRef = ref<{ focus: () => void } | null>(null)

function validateField(field: keyof typeof form) {
  touched[field] = true
  const parsed = signUpSchema.safeParse({ ...form, country_code: 'PK' })
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

function handleUsernameInput(val: string) {
  form.username = val.toLowerCase()
  checkUsername(form.username)
  if (touched.username) validateField('username')
}

const isFormValid = computed(() => {
  const parsed = signUpSchema.safeParse({ ...form, country_code: 'PK' })
  if (!parsed.success) return false
  return usernameStatus.value !== 'taken' && usernameStatus.value !== 'invalid'
})

function focusFirstInvalid() {
  const order: Array<[string, { focus: () => void } | null]> = [
    ['full_name', fullNameRef.value],
    ['username', usernameRef.value],
    ['email', emailRef.value],
    ['phone', phoneRef.value],
    ['password', passwordRef.value],
    ['confirm_password', confirmPasswordRef.value],
  ]
  for (const [key, comp] of order) {
    if (errors[key]) {
      comp?.focus()
      break
    }
  }
}

async function handleSubmit() {
  formError.value = ''
  const parsed = signUpSchema.safeParse({ ...form, country_code: 'PK' })

  if (!parsed.success) {
    for (const key of Object.keys(form)) {
      touched[key] = true
      Reflect.deleteProperty(errors, key)
    }
    for (const issue of parsed.error.issues) {
      const k = String(issue.path[0] ?? '')
      if (k && !errors[k]) errors[k] = issue.message
    }
    focusFirstInvalid()
    return
  }

  if (usernameStatus.value === 'taken') {
    errors.username = 'This username is already taken'
    usernameRef.value?.focus()
    return
  }

  submitting.value = true
  try {
    await signUp({
      email: parsed.data.email,
      password: parsed.data.password,
      username: parsed.data.username,
      full_name: parsed.data.full_name,
      phone: parsed.data.phone,
    })
    sessionStorage.setItem('inkubify_pending_email', parsed.data.email)
    await navigateTo('/verify-email')
  } catch (err: unknown) {
    formError.value = err instanceof Error ? err.message : 'Unable to create account'
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
      class="rounded-input border border-danger/50 bg-danger/10 px-3.5 py-2.5 text-sm text-danger"
    >
      {{ formError }}
    </div>

    <BaseInput
      id="signup-full-name"
      ref="fullNameRef"
      v-model="form.full_name"
      label="Full name"
      placeholder="e.g. Ayesha Siddiqui"
      autocomplete="name"
      required
      :error="errors.full_name"
      @blur="validateField('full_name')"
    />

    <BaseInput
      id="signup-username"
      ref="usernameRef"
      :model-value="form.username"
      label="Username"
      placeholder="e.g. ayesha_founder"
      autocomplete="username"
      required
      :hint="
        usernameStatus === 'available'
          ? 'Username is available'
          : '3–20 lowercase letters, numbers, or underscores'
      "
      :error="
        errors.username ||
          (usernameStatus === 'taken' || usernameStatus === 'invalid' ? usernameHint : '')
      "
      @update:model-value="handleUsernameInput"
      @blur="validateField('username')"
    >
      <template #trailing>
        <Loader2
          v-if="usernameStatus === 'checking'"
          class="h-4 w-4 animate-spin text-snow-muted"
          aria-hidden="true"
        />
        <Check
          v-else-if="usernameStatus === 'available'"
          class="h-4 w-4 text-success"
          aria-label="Username available"
        />
        <X
          v-else-if="usernameStatus === 'taken' || usernameStatus === 'invalid'"
          class="h-4 w-4 text-danger"
          aria-label="Username unavailable"
        />
      </template>
    </BaseInput>

    <BaseInput
      id="signup-email"
      ref="emailRef"
      v-model="form.email"
      type="email"
      label="Email address"
      placeholder="you@example.com"
      autocomplete="email"
      required
      :error="errors.email"
      @blur="validateField('email')"
    />

    <BasePhoneInput
      id="signup-phone"
      ref="phoneRef"
      v-model="form.phone"
      label="Mobile number"
      required
      :error="errors.phone"
      @blur="validateField('phone')"
    />

    <BaseSelect
      id="signup-country"
      model-value="PK"
      label="Country"
      :options="[{ value: 'PK', label: 'Pakistan (PK)' }]"
      disabled
      required
      hint="Inkubify currently serves Pakistan only"
    />

    <div class="space-y-1">
      <BasePasswordInput
        id="signup-password"
        ref="passwordRef"
        v-model="form.password"
        label="Password"
        placeholder="Create a strong password"
        autocomplete="new-password"
        required
        :error="errors.password"
        @blur="validateField('password')"
      />
      <PasswordStrength :password="form.password" />
    </div>

    <BasePasswordInput
      id="signup-confirm-password"
      ref="confirmPasswordRef"
      v-model="form.confirm_password"
      label="Confirm password"
      placeholder="Re-enter your password"
      autocomplete="new-password"
      required
      :error="errors.confirm_password"
      @blur="validateField('confirm_password')"
    />

    <BaseCheckbox
      id="signup-terms"
      v-model="form.accept_terms"
      :error="errors.accept_terms"
    >
      I agree to Inkubify's
      <NuxtLink to="/terms" class="font-medium text-gold-500 underline-offset-2 hover:underline">
        Terms of Service
      </NuxtLink>
      and
      <NuxtLink to="/privacy" class="font-medium text-gold-500 underline-offset-2 hover:underline">
        Privacy Policy
      </NuxtLink>.
    </BaseCheckbox>

    <BaseButton
      type="submit"
      variant="primary"
      size="lg"
      block
      :loading="submitting"
      :disabled="!isFormValid || submitting"
    >
      Create account
    </BaseButton>
  </form>
</template>
