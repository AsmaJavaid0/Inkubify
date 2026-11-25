<script setup lang="ts">
export interface AppLogoProps {
  size?: 'sm' | 'md' | 'lg' | 'splash'
}

const props = withDefaults(defineProps<AppLogoProps>(), {
  size: 'md',
})

const imageFailed = ref(false)
const logoSrc = '/brand/logo.png'

const sizeClasses: Record<NonNullable<AppLogoProps['size']>, string> = {
  sm: 'h-9 px-2.5 py-1.5 rounded-[10px]',
  md: 'h-12 px-3 py-2 rounded-[12px]',
  lg: 'h-16 px-4 py-2.5 rounded-[14px]',
  splash: 'h-28 px-5 py-3.5 rounded-[16px]',
}

const markSizeClasses: Record<NonNullable<AppLogoProps['size']>, string> = {
  sm: 'h-6 w-6',
  md: 'h-8 w-8',
  lg: 'h-11 w-11',
  splash: 'h-20 w-20',
}
</script>

<template>
  <!-- Logo rendered alone on a snow-100 rounded panel; never text beside it, never in a circle (§4.3) -->
  <div
    class="inline-flex items-center justify-center bg-snow-100 shadow-sm select-none"
    :class="sizeClasses[props.size]"
  >
    <img
      v-if="!imageFailed"
      :src="logoSrc"
      alt="Inkubify"
      class="h-full w-auto object-contain"
      @error="imageFailed = true"
    >
    <!-- Clean vector fallback when /brand/logo.png is pending owner upload -->
    <svg
      v-else
      :class="markSizeClasses[props.size]"
      viewBox="0 0 64 64"
      fill="none"
      role="img"
      aria-label="Inkubify"
    >
      <path
        d="M14 38L32 48L50 38V52L32 61L14 52V38Z"
        fill="#142535"
      />
      <path
        d="M32 48V61M14 38L32 28L50 38"
        stroke="#23384B"
        stroke-width="2"
        stroke-linejoin="round"
      />
      <path
        d="M32 7C24.8 7 19 12.8 19 20C19 24.9 21.7 29.1 25.8 31.3L26.5 35.5H37.5L38.2 31.3C42.3 29.1 45 24.9 45 20C45 12.8 39.2 7 32 7Z"
        fill="#23384B"
      />
      <path
        d="M32 27V14M32 14L27.5 18.5M32 14L36.5 18.5"
        stroke="#C19829"
        stroke-width="3.2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  </div>
</template>
