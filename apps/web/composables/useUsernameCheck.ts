import { usernameSchema } from '~/schemas/auth'
import type { UsernameAvailabilityResponse } from '~/types/api'

export type UsernameCheckStatus = 'idle' | 'checking' | 'available' | 'taken' | 'invalid'

export function useUsernameCheck() {
  const { request } = useApi()
  const status = ref<UsernameCheckStatus>('idle')
  const message = ref<string>('')

  let timer: ReturnType<typeof setTimeout> | null = null
  let latestQuery = ''

  function check(rawUsername: string) {
    if (timer) clearTimeout(timer)
    const normalized = rawUsername.trim().toLowerCase()
    latestQuery = normalized

    if (!normalized) {
      status.value = 'idle'
      message.value = ''
      return
    }

    const parsed = usernameSchema.safeParse(normalized)
    if (!parsed.success) {
      status.value = 'invalid'
      message.value = parsed.error.issues[0]?.message ?? 'Invalid username'
      return
    }

    status.value = 'checking'
    message.value = 'Checking availability...'

    timer = setTimeout(async () => {
      try {
        const res = await request<UsernameAvailabilityResponse>(
          `/usernames/availability?username=${encodeURIComponent(normalized)}`,
          { method: 'GET' },
          false,
        )
        if (latestQuery !== normalized) return
        if (res.available) {
          status.value = 'available'
          message.value = 'Username is available'
        } else {
          status.value = 'taken'
          message.value = 'This username is already taken'
        }
      } catch {
        if (latestQuery !== normalized) return
        status.value = 'idle'
        message.value = ''
      }
    }, 400)
  }

  return {
    status: readonly(status),
    message: readonly(message),
    check,
  }
}
