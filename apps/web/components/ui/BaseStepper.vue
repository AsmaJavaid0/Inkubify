<script setup lang="ts">
import { Check } from 'lucide-vue-next'

export interface StepItem {
  number: number
  title: string
  shortTitle?: string
}

interface Props {
  steps: readonly StepItem[]
  currentStep: number
  maxCompletedStep: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  select: [stepNumber: number]
}>()

function isClickable(stepNumber: number): boolean {
  return stepNumber <= props.maxCompletedStep || stepNumber < props.currentStep
}
</script>

<template>
  <nav aria-label="Onboarding progress" class="w-full">
    <ol class="flex items-center justify-between gap-2">
      <li
        v-for="(step, idx) in props.steps"
        :key="step.number"
        class="flex flex-1 items-center"
      >
        <button
          type="button"
          :disabled="!isClickable(step.number) && step.number !== props.currentStep"
          :aria-current="step.number === props.currentStep ? 'step' : undefined"
          class="group flex items-center gap-2 text-left disabled:cursor-default"
          @click="isClickable(step.number) ? emit('select', step.number) : undefined"
        >
          <span
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border text-xs font-bold transition-colors"
            :class="
              step.number === props.currentStep
                ? 'border-gold-500 bg-gold-500 text-navy-900'
                : step.number < props.currentStep || step.number <= props.maxCompletedStep
                  ? 'border-gold-500/60 bg-gold-500/15 text-gold-500'
                  : 'border-navy-border bg-navy-700 text-snow-muted'
            "
          >
            <Check
              v-if="step.number < props.currentStep"
              class="h-4 w-4"
              aria-hidden="true"
            />
            <span v-else>{{ step.number }}</span>
          </span>
          <span
            class="hidden text-xs font-medium sm:inline"
            :class="
              step.number === props.currentStep
                ? 'text-gold-500'
                : step.number < props.currentStep
                  ? 'text-snow-100'
                  : 'text-snow-muted'
            "
          >
            {{ step.shortTitle || step.title }}
          </span>
        </button>

        <div
          v-if="idx < props.steps.length - 1"
          class="mx-2 h-0.5 flex-1 rounded-full"
          :class="step.number < props.currentStep ? 'bg-gold-500/60' : 'bg-navy-border'"
          aria-hidden="true"
        />
      </li>
    </ol>
  </nav>
</template>
