import { useProfileStore } from '~/stores/profile'

const PUBLIC_PATHS = new Set([
  '/',
  '/welcome',
  '/signup',
  '/login',
  '/verify-email',
  '/forgot-password',
  '/reset-password',
  '/auth/confirm',
  '/terms',
  '/privacy',
])

const SHARED_AUTHENTICATED_PATHS = new Set([
  '/',
  '/auth/confirm',
  '/reset-password',
  '/terms',
  '/privacy',
])

export default defineNuxtRouteMiddleware(async (to) => {
  // Never run guard checks on server during initial SSR if session is client-driven,
  // unless @nuxtjs/supabase already hydrated the user cookie.
  const path = to.path.replace(/\/+$/, '') || '/'

  if (import.meta.dev && path === '/_kit') {
    return
  }

  const user = useSupabaseUser()

  if (!user.value) {
    if (PUBLIC_PATHS.has(path)) {
      return
    }
    return navigateTo('/login')
  }

  // Signed in: check email verification
  const isVerified = Boolean(user.value.email_confirmed_at || user.value.confirmed_at)
  if (!isVerified) {
    if (path === '/verify-email' || path === '/auth/confirm' || path === '/terms' || path === '/privacy') {
      return
    }
    return navigateTo('/verify-email')
  }

  if (SHARED_AUTHENTICATED_PATHS.has(path)) {
    return
  }

  const profileStore = useProfileStore()
  const profile = await profileStore.fetchProfile()

  // If profile could not be fetched yet (e.g. offline/API down), allow current onboarding/dashboard
  // page to render its error & retry UI cleanly rather than looping redirects.
  if (!profile) {
    if (path === '/onboarding/profile' || path === '/dashboard' || path === '/profile') {
      return
    }
    return navigateTo('/onboarding/profile')
  }

  if (profile.onboarding.status !== 'completed') {
    if (path === '/onboarding/profile') {
      return
    }
    return navigateTo('/onboarding/profile')
  }

  // Onboarding completed
  if (path === '/dashboard' || path === '/profile') {
    return
  }
  return navigateTo('/dashboard')
})
