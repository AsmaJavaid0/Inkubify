import { useProfileStore } from '~/stores/profile'
import { useOnboardingStore } from '~/stores/onboarding'
import { mapAuthErrorMessage } from '~/utils/errors'
import { normalizePakistaniPhone } from '~/utils/phone'

export function useAuthActions() {
  const supabase = useSupabaseClient()
  const config = useRuntimeConfig()
  const profileStore = useProfileStore()
  const onboardingStore = useOnboardingStore()
  const { request } = useApi()

  async function signUp(input: {
    email: string
    password: string
    username: string
    full_name: string
    phone: string
  }) {
    const e164 = normalizePakistaniPhone(input.phone)
    if (!e164) {
      throw new Error('Please enter a valid Pakistani mobile number.')
    }
    const siteUrl = (config.public.siteUrl as string).replace(/\/$/, '')
    const { data, error } = await supabase.auth.signUp({
      email: input.email.trim().toLowerCase(),
      password: input.password,
      options: {
        emailRedirectTo: `${siteUrl}/auth/confirm`,
        data: {
          username: input.username.trim().toLowerCase(),
          full_name: input.full_name.trim().replace(/\s+/g, ' '),
          phone: e164,
          country_code: 'PK',
        },
      },
    })
    if (error) {
      throw new Error(mapAuthErrorMessage(error))
    }
    return data
  }

  async function resendVerification(email: string) {
    const siteUrl = (config.public.siteUrl as string).replace(/\/$/, '')
    const { error } = await supabase.auth.resend({
      type: 'signup',
      email: email.trim().toLowerCase(),
      options: {
        emailRedirectTo: `${siteUrl}/auth/confirm`,
      },
    })
    if (error) {
      throw new Error(mapAuthErrorMessage(error))
    }
  }

  async function signIn(username: string, password: string) {
    const result = await request<{
      access_token: string
      refresh_token: string
    }>('/auth/login', {
      method: 'POST',
      body: { username: username.trim().toLowerCase(), password },
    }, false)
    const { data, error } = await supabase.auth.setSession({
      access_token: result.access_token,
      refresh_token: result.refresh_token,
    })
    if (error) throw new Error(mapAuthErrorMessage(error))
    return data
  }

  async function requestPasswordReset(email: string) {
    const siteUrl = (config.public.siteUrl as string).replace(/\/$/, '')
    const { error } = await supabase.auth.resetPasswordForEmail(
      email.trim().toLowerCase(),
      {
        redirectTo: `${siteUrl}/reset-password`,
      },
    )
    if (error) {
      throw new Error(mapAuthErrorMessage(error))
    }
  }

  async function updatePassword(newPassword: string) {
    const { error } = await supabase.auth.updateUser({
      password: newPassword,
    })
    if (error) {
      throw new Error(mapAuthErrorMessage(error))
    }
  }

  async function signOut() {
    await supabase.auth.signOut()
    profileStore.reset()
    onboardingStore.reset()
    await navigateTo('/login')
  }

  return {
    signUp,
    resendVerification,
    signIn,
    requestPasswordReset,
    updatePassword,
    signOut,
  }
}
