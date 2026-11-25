<script setup lang="ts">
import { CheckCircle2, Pencil } from 'lucide-vue-next'
import BaseButton from '~/components/ui/BaseButton.vue'
import {
  EDUCATION_OPTIONS,
  GENDER_OPTIONS,
  INTERESTED_IN_OPTIONS,
  LANGUAGE_OPTIONS,
  OCCUPATION_OPTIONS,
  PRIMARY_GOAL_OPTIONS,
  PRIOR_BUSINESS_OPTIONS,
  PROFICIENCY_OPTIONS,
  WEEKLY_HOURS_OPTIONS,
  WORK_EXPERIENCE_OPTIONS,
} from '~/constants/options'
import { useProfileStore } from '~/stores/profile'
import { parseApiError } from '~/utils/errors'

const emit = defineEmits<{
  editStep: [step: number]
  back: []
}>()

const profileStore = useProfileStore()
const finishing = ref(false)
const completed = ref(false)
const errorMsg = ref('')
const fieldErrors = ref<Record<string, string>>({})

const p = computed(() => profileStore.profile)

function labelFor(options: readonly { value: string; label: string }[], value: string | null | undefined) {
  if (!value) return '—'
  return options.find((o) => o.value === value)?.label ?? value
}

async function handleFinish() {
  errorMsg.value = ''
  fieldErrors.value = {}
  finishing.value = true
  try {
    await profileStore.completeOnboarding()
    completed.value = true
  } catch (err: unknown) {
    const apiErr = parseApiError(err)
    errorMsg.value = apiErr.message
    fieldErrors.value = apiErr.fields
  } finally {
    finishing.value = false
  }
}
</script>

<template>
  <div v-if="completed" class="space-y-6 py-6 text-center">
    <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-card bg-success/15 text-success">
      <CheckCircle2 class="h-8 w-8" aria-hidden="true" />
    </div>
    <div class="space-y-2">
      <h2 class="text-2xl font-bold text-snow-100">Your founder profile is ready</h2>
      <p class="mx-auto max-w-md text-sm text-snow-muted">
        Everything is saved. Next, you can head to your dashboard and prepare for your business
        profile setup.
      </p>
    </div>
    <BaseButton variant="primary" size="lg" @click="navigateTo('/dashboard')">
      Go to dashboard
    </BaseButton>
  </div>

  <div v-else-if="p" class="space-y-5">
    <div
      v-if="errorMsg"
      role="alert"
      class="space-y-2 rounded-input border border-danger/50 bg-danger/10 p-3.5 text-sm text-danger"
    >
      <p class="font-medium">{{ errorMsg }}</p>
      <ul v-if="Object.keys(fieldErrors).length" class="list-disc pl-5 text-xs">
        <li v-for="(msg, field) in fieldErrors" :key="field">
          {{ field }}: {{ msg }}
        </li>
      </ul>
    </div>

    <!-- Step 1 summary -->
    <section class="rounded-input border border-navy-border bg-navy-900/40 p-4">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-sm font-semibold text-gold-500">1. Personal</h3>
        <button
          type="button"
          class="inline-flex items-center gap-1 text-xs font-medium text-snow-muted hover:text-gold-500"
          @click="emit('editStep', 1)"
        >
          <Pencil class="h-3.5 w-3.5" aria-hidden="true" />
          Edit
        </button>
      </div>
      <dl class="grid gap-2 text-sm sm:grid-cols-2">
        <div>
          <dt class="text-xs text-snow-muted">Date of birth</dt>
          <dd>{{ p.date_of_birth || '—' }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Location</dt>
          <dd>{{ p.city && p.province ? `${p.city}, ${p.province}` : '—' }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Gender</dt>
          <dd>{{ labelFor(GENDER_OPTIONS, p.gender) }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Preferred language</dt>
          <dd>{{ labelFor(LANGUAGE_OPTIONS, p.preferred_language) }}</dd>
        </div>
        <div class="sm:col-span-2">
          <dt class="text-xs text-snow-muted">Bio</dt>
          <dd>{{ p.bio || '—' }}</dd>
        </div>
      </dl>
    </section>

    <!-- Step 2 summary -->
    <section class="rounded-input border border-navy-border bg-navy-900/40 p-4">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-sm font-semibold text-gold-500">2. Background</h3>
        <button
          type="button"
          class="inline-flex items-center gap-1 text-xs font-medium text-snow-muted hover:text-gold-500"
          @click="emit('editStep', 2)"
        >
          <Pencil class="h-3.5 w-3.5" aria-hidden="true" />
          Edit
        </button>
      </div>
      <dl class="grid gap-2 text-sm sm:grid-cols-2">
        <div>
          <dt class="text-xs text-snow-muted">Education</dt>
          <dd>{{ labelFor(EDUCATION_OPTIONS, p.education_level) }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Field of study</dt>
          <dd>{{ p.field_of_study || '—' }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Current status</dt>
          <dd>{{ labelFor(OCCUPATION_OPTIONS, p.occupation_status) }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Work experience</dt>
          <dd>{{ labelFor(WORK_EXPERIENCE_OPTIONS, p.work_experience) }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Prior business</dt>
          <dd>{{ labelFor(PRIOR_BUSINESS_OPTIONS, p.prior_business) }}</dd>
        </div>
      </dl>
    </section>

    <!-- Step 3 summary -->
    <section class="rounded-input border border-navy-border bg-navy-900/40 p-4">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-sm font-semibold text-gold-500">3. Skills &amp; Expertise</h3>
        <button
          type="button"
          class="inline-flex items-center gap-1 text-xs font-medium text-snow-muted hover:text-gold-500"
          @click="emit('editStep', 3)"
        >
          <Pencil class="h-3.5 w-3.5" aria-hidden="true" />
          Edit
        </button>
      </div>
      <div v-if="p.skills.length" class="flex flex-wrap gap-2">
        <span
          v-for="s in p.skills"
          :key="s.skill_id"
          class="rounded-[10px] border border-navy-border bg-navy-700 px-3 py-1.5 text-xs"
        >
          {{ s.name }}
          <span class="text-gold-500">· {{ labelFor(PROFICIENCY_OPTIONS, s.proficiency) }}</span>
        </span>
      </div>
      <p v-else class="text-sm text-snow-muted">No skills selected yet.</p>
    </section>

    <!-- Step 4 summary -->
    <section class="rounded-input border border-navy-border bg-navy-900/40 p-4">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-sm font-semibold text-gold-500">4. Goals &amp; Availability</h3>
        <button
          type="button"
          class="inline-flex items-center gap-1 text-xs font-medium text-snow-muted hover:text-gold-500"
          @click="emit('editStep', 4)"
        >
          <Pencil class="h-3.5 w-3.5" aria-hidden="true" />
          Edit
        </button>
      </div>
      <dl class="grid gap-2 text-sm sm:grid-cols-2">
        <div>
          <dt class="text-xs text-snow-muted">Primary goal</dt>
          <dd>{{ labelFor(PRIMARY_GOAL_OPTIONS, p.primary_goal) }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Weekly time available</dt>
          <dd>{{ labelFor(WEEKLY_HOURS_OPTIONS, p.weekly_hours) }}</dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Interested in</dt>
          <dd>
            {{
              p.interested_in.length
                ? p.interested_in
                    .map((i: string) => labelFor(INTERESTED_IN_OPTIONS, i))
                    .join(', ')
                : '—'
            }}
          </dd>
        </div>
        <div>
          <dt class="text-xs text-snow-muted">Social links</dt>
          <dd class="truncate">
            {{ [p.instagram_url, p.linkedin_url].filter(Boolean).join(' · ') || '—' }}
          </dd>
        </div>
      </dl>
    </section>

    <div class="flex items-center justify-between pt-2">
      <BaseButton type="button" variant="secondary" :disabled="finishing" @click="emit('back')">
        Back
      </BaseButton>
      <BaseButton type="button" variant="primary" size="lg" :loading="finishing" @click="handleFinish">
        Finish setup
      </BaseButton>
    </div>
  </div>
</template>
