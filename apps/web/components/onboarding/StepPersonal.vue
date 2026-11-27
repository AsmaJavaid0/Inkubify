<script setup lang="ts">
import BaseAvatarUpload from '~/components/ui/BaseAvatarUpload.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseChipSelect from '~/components/ui/BaseChipSelect.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BaseSelect from '~/components/ui/BaseSelect.vue'
import BaseTextarea from '~/components/ui/BaseTextarea.vue'
import { PROVINCES, PROVINCE_CITIES, type Province } from '~/constants/geo'
import { GENDER_OPTIONS, LANGUAGE_OPTIONS } from '~/constants/options'
import { ageFromDob, stepPersonalSchema } from '~/schemas/profile'
import { useOnboardingStore } from '~/stores/onboarding'
import { useProfileStore } from '~/stores/profile'
import { parseApiError } from '~/utils/errors'

interface Props { mode?: 'wizard' | 'edit' }
const props = withDefaults(defineProps<Props>(), { mode: 'wizard' })
const emit = defineEmits<{ next: [] }>()
const onboarding = useOnboardingStore()
const profileStore = useProfileStore()
const toast = useToast()
const draft = onboarding.draft
const errors = reactive<Record<string, string>>({})
const serverError = ref('')
const saving = ref(false)
const calculatedAge = computed(() => ageFromDob(draft.date_of_birth))
const maxDob = computed(() => {
  const d = new Date()
  d.setFullYear(d.getFullYear() - 18)
  return d.toISOString().slice(0, 10)
})
const provinceOptions = PROVINCES.map((p) => ({ value: p, label: p }))
const selectedCityDropdown = ref('')
const customCity = ref('')
function syncCityFromDraft() {
  const prov = draft.province as Province
  const predefined = prov && PROVINCE_CITIES[prov] ? PROVINCE_CITIES[prov] : []
  if (!draft.city) {
    selectedCityDropdown.value = ''
    customCity.value = ''
  } else if (predefined.includes(draft.city)) {
    selectedCityDropdown.value = draft.city
    customCity.value = ''
  } else {
    selectedCityDropdown.value = '__OTHER__'
    customCity.value = draft.city
  }
}
onMounted(syncCityFromDraft)
watch(() => profileStore.profile?.id, syncCityFromDraft)
const cityOptions = computed(() => {
  const prov = draft.province as Province
  const list = prov && PROVINCE_CITIES[prov] ? PROVINCE_CITIES[prov] : []
  return [...list.map((c) => ({ value: c, label: c })), { value: '__OTHER__', label: 'Other' }]
})
function handleProvinceChange(val: string) {
  draft.province = val
  selectedCityDropdown.value = ''
  customCity.value = ''
  draft.city = ''
  delete errors.province
  delete errors.city
}
function handleCityDropdownChange(val: string) {
  selectedCityDropdown.value = val
  if (val === '__OTHER__') draft.city = customCity.value.trim()
  else {
    customCity.value = ''
    draft.city = val
  }
  delete errors.city
}
function handleCustomCityInput(val: string) {
  customCity.value = val
  draft.city = val.trim()
  delete errors.city
}
async function handleSave() {
  serverError.value = ''
  for (const key of Object.keys(errors)) Reflect.deleteProperty(errors, key)
  const parsed = stepPersonalSchema.safeParse({
    full_name: draft.full_name,
    avatar_url: draft.avatar_url,
    date_of_birth: draft.date_of_birth,
    gender: draft.gender || null,
    address: draft.address.trim() || null,
    province: draft.province,
    city: draft.city,
    bio: draft.bio?.trim() || null,
    preferred_language: draft.preferred_language || 'en',
  })
  if (!parsed.success) {
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? '')
      if (key && !errors[key]) errors[key] = issue.message
    }
    return
  }
  saving.value = true
  try {
    const payload: Record<string, unknown> = {
      full_name: parsed.data.full_name,
      avatar_url: parsed.data.avatar_url ?? null,
      date_of_birth: parsed.data.date_of_birth,
      gender: parsed.data.gender ?? null,
      address: parsed.data.address ?? null,
      province: parsed.data.province,
      city: parsed.data.city,
      bio: parsed.data.bio ?? null,
      preferred_language: parsed.data.preferred_language,
    }
    if (props.mode === 'wizard') payload.onboarding_step = 2
    await profileStore.patchProfile(payload)
    if (props.mode === 'wizard') emit('next')
    else toast.success('Personal information saved')
  } catch (err: unknown) {
    const apiErr = parseApiError(err)
    Object.assign(errors, apiErr.fields)
    serverError.value = apiErr.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="space-y-5" novalidate @submit.prevent="handleSave">
    <div v-if="serverError" role="alert" class="rounded-input border border-danger/50 bg-danger/10 px-3.5 py-2.5 text-sm text-danger">{{ serverError }}</div>
    <BaseAvatarUpload v-model="draft.avatar_url" :full-name="draft.full_name" :user-id="profileStore.profile?.id" :disabled="saving" />
    <div class="grid gap-4 sm:grid-cols-2">
      <BaseInput id="personal-name" v-model="draft.full_name" label="Full name" required :error="errors.full_name" />
      <BaseInput id="personal-username" :model-value="profileStore.profile?.username ? '@' + profileStore.profile.username : ''" label="Username" disabled />
      <BaseInput id="personal-email" :model-value="profileStore.profile?.email ?? ''" label="Email" disabled />
      <BaseInput id="personal-phone" :model-value="profileStore.profile?.phone_e164 ?? ''" label="Phone number" disabled />
      <BaseInput id="personal-country" model-value="Pakistan" label="Country" disabled />
      <BaseInput id="personal-dob" v-model="draft.date_of_birth" type="date" label="Date of birth" min="1930-01-01" :max="maxDob" required :error="errors.date_of_birth" />
    </div>
    <p class="-mt-3 text-xs text-snow-muted">Age: {{ calculatedAge === null ? 'Calculated from your date of birth' : calculatedAge + ' years' }}. You must be at least 18.</p>
    <BaseChipSelect id="personal-gender" v-model="draft.gender" label="Gender" :options="GENDER_OPTIONS" hint="Optional" :error="errors.gender" />
    <BaseInput id="personal-address" v-model="draft.address" label="Street address" placeholder="House, street, area (optional)" :error="errors.address" />
    <div class="grid gap-4 sm:grid-cols-2">
      <BaseSelect id="personal-province" :model-value="draft.province" label="Province / Territory" placeholder="Select province or territory" :options="provinceOptions" required :error="errors.province" @update:model-value="handleProvinceChange" />
      <BaseSelect id="personal-city-select" :model-value="selectedCityDropdown" label="City" placeholder="Select city" :options="cityOptions" :disabled="!draft.province" required :error="selectedCityDropdown !== '__OTHER__' ? errors.city : ''" @update:model-value="handleCityDropdownChange" />
    </div>
    <BaseInput v-if="selectedCityDropdown === '__OTHER__'" id="personal-city-other" :model-value="customCity" label="Enter your city name" placeholder="e.g. Chakwal" required :error="errors.city" @update:model-value="handleCustomCityInput" />
    <BaseChipSelect id="personal-language" v-model="draft.preferred_language" label="Preferred language" :options="LANGUAGE_OPTIONS" required :error="errors.preferred_language" />
    <BaseTextarea id="personal-bio" v-model="draft.bio" label="Short bio" placeholder="Tell us a little about yourself..." :maxlength="280" hint="Optional, up to 280 characters" :error="errors.bio" />
    <div class="flex justify-end pt-2">
      <BaseButton type="submit" variant="primary" size="md" :loading="saving">{{ props.mode === 'wizard' ? 'Save & continue' : 'Save personal information' }}</BaseButton>
    </div>
  </form>
</template>
