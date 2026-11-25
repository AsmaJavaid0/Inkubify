<script setup lang="ts">
import AppLogo from '~/components/brand/AppLogo.vue'
import BaseButton from '~/components/ui/BaseButton.vue'
import BaseCheckbox from '~/components/ui/BaseCheckbox.vue'
import BaseChipSelect from '~/components/ui/BaseChipSelect.vue'
import BaseInput from '~/components/ui/BaseInput.vue'
import BasePasswordInput from '~/components/ui/BasePasswordInput.vue'
import BasePhoneInput from '~/components/ui/BasePhoneInput.vue'
import BaseSelect from '~/components/ui/BaseSelect.vue'
import BaseStepper from '~/components/ui/BaseStepper.vue'
import BaseTextarea from '~/components/ui/BaseTextarea.vue'
import { WIZARD_STEPS } from '~/constants/options'

const sampleText = ref('Sample input')
const samplePassword = ref('Secret123')
const samplePhone = ref('3001234567')
const sampleSelect = ref('Punjab')
const sampleTextarea = ref('Building a tech-enabled brand in Lahore.')
const sampleCheck = ref(true)
const sampleChip = ref('full_time_business')
const toast = useToast()
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-8 py-6">
    <header class="flex items-center justify-between border-b border-navy-border pb-4">
      <div>
        <h1 class="text-2xl font-bold text-snow-100">Inkubify UI Kit (Dev)</h1>
        <p class="text-sm text-snow-muted">Tokens &amp; components from Phase 1 Spec §4</p>
      </div>
      <AppLogo size="md" />
    </header>

    <section class="space-y-3 rounded-card border border-navy-border bg-navy-700 p-6">
      <h2 class="text-lg font-semibold text-snow-100">Buttons</h2>
      <div class="flex flex-wrap gap-3">
        <BaseButton variant="primary">Primary</BaseButton>
        <BaseButton variant="secondary">Secondary</BaseButton>
        <BaseButton variant="ghost">Ghost</BaseButton>
        <BaseButton variant="danger">Danger</BaseButton>
        <BaseButton variant="primary" loading>Loading</BaseButton>
        <BaseButton variant="primary" disabled>Disabled</BaseButton>
        <BaseButton variant="secondary" @click="toast.success('Toast works!')">
          Trigger Toast
        </BaseButton>
      </div>
    </section>

    <section class="space-y-4 rounded-card border border-navy-border bg-navy-700 p-6">
      <h2 class="text-lg font-semibold text-snow-100">Stepper</h2>
      <BaseStepper :steps="WIZARD_STEPS" :current-step="2" :max-completed-step="2" />
    </section>

    <section class="grid gap-4 rounded-card border border-navy-border bg-navy-700 p-6 sm:grid-cols-2">
      <BaseInput id="kit-text" v-model="sampleText" label="Text Input" hint="Helper text" />
      <BaseInput
        id="kit-err"
        model-value="Bad"
        label="Error State"
        error="Must be at least 5 characters"
      />
      <BasePasswordInput id="kit-pw" v-model="samplePassword" label="Password" />
      <BasePhoneInput id="kit-phone" v-model="samplePhone" label="Phone" />
      <BaseSelect
        id="kit-select"
        v-model="sampleSelect"
        label="Province"
        :options="[
          { value: 'Punjab', label: 'Punjab' },
          { value: 'Sindh', label: 'Sindh' },
        ]"
      />
      <BaseChipSelect
        id="kit-chips"
        v-model="sampleChip"
        label="Chip Select"
        :options="[
          { value: 'side_income', label: 'Side Income' },
          { value: 'full_time_business', label: 'Full-Time' },
        ]"
      />
      <div class="sm:col-span-2">
        <BaseTextarea id="kit-bio" v-model="sampleTextarea" label="Bio" :maxlength="280" />
      </div>
      <div class="sm:col-span-2">
        <BaseCheckbox id="kit-chk" v-model="sampleCheck">
          Accept Terms &amp; Privacy
        </BaseCheckbox>
      </div>
    </section>
  </div>
</template>
