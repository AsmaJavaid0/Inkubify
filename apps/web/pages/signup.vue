<script setup lang="ts">
import SignUpForm from '~/components/auth/SignUpForm.vue'

definePageMeta({ layout: 'auth' })
</script>

<template>
  <div class="space-y-6">
    <div class="space-y-1.5 text-center">
      <h1 class="text-2xl font-bold tracking-tight text-snow-100">
        Create your founder account
      </h1>
      <p class="text-sm text-snow-muted">
        Start building your roadmap for Pakistan
      </p>
    </div>

    <SignUpForm />

    <p class="text-center text-sm text-snow-muted">
      Already have an account?
      <NuxtLink to="/login" class="font-semibold text-gold-500 hover:underline">
        Log in
      </NuxtLink>
    </p>
  </div>
</template>
