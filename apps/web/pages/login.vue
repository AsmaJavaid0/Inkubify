<script setup lang="ts">
import LoginForm from '~/components/auth/LoginForm.vue'

definePageMeta({ layout: 'auth' })
</script>

<template>
  <div class="space-y-6">
    <div class="space-y-1.5 text-center">
      <h1 class="text-2xl font-bold tracking-tight text-snow-100">
        Welcome back
      </h1>
      <p class="text-sm text-snow-muted">
        Log in to continue your Inkubify journey
      </p>
    </div>

    <LoginForm />

    <p class="text-center text-sm text-snow-muted">
      New to Inkubify?
      <NuxtLink to="/signup" class="font-semibold text-gold-500 hover:underline">
        Create an account
      </NuxtLink>
    </p>
  </div>
</template>
