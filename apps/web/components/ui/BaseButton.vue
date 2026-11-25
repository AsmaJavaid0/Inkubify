<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  type?: 'button' | 'submit' | 'reset'
  loading?: boolean
  disabled?: boolean
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  type: 'button',
  loading: false,
  disabled: false,
  block: false,
})

const variantClasses: Record<NonNullable<Props['variant']>, string> = {
  primary:
    'bg-gold-500 text-navy-900 font-semibold hover:bg-gold-hover disabled:opacity-50',
  secondary:
    'border border-snow-100/20 bg-navy-700 text-snow-100 font-medium hover:border-snow-100/40 disabled:opacity-50',
  ghost:
    'bg-transparent text-snow-100 font-medium hover:bg-snow-100/10 disabled:opacity-40',
  danger:
    'bg-danger text-navy-900 font-semibold hover:opacity-90 disabled:opacity-50',
}

const sizeClasses: Record<NonNullable<Props['size']>, string> = {
  sm: 'h-9 px-3.5 text-sm rounded-[10px]',
  md: 'h-11 px-5 text-sm rounded-[10px]',
  lg: 'h-12 px-6 text-base rounded-[12px]',
}
</script>

<template>
  <button
    :type="props.type"
    :disabled="props.disabled || props.loading"
    :aria-busy="props.loading"
    class="inline-flex items-center justify-center gap-2 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold-500 focus-visible:ring-offset-2 focus-visible:ring-offset-navy-900 disabled:cursor-not-allowed"
    :class="[
      variantClasses[props.variant],
      sizeClasses[props.size],
      props.block ? 'w-full' : '',
    ]"
  >
    <svg
      v-if="props.loading"
      class="h-4 w-4 animate-spin"
      viewBox="0 0 24 24"
      fill="none"
      aria-hidden="true"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="3"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v3a5 5 0 00-5 5H4z"
      />
    </svg>
    <slot />
  </button>
</template>
