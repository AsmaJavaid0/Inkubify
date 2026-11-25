import { parseApiError } from '~/utils/errors'

export function useApi() {
  const config = useRuntimeConfig()
  const supabase = useSupabaseClient()

  async function getAccessToken(forceRefresh = false): Promise<string | null> {
    if (forceRefresh) {
      const { data } = await supabase.auth.refreshSession()
      return data.session?.access_token ?? null
    }
    const { data } = await supabase.auth.getSession()
    return data.session?.access_token ?? null
  }

  async function request<T>(
    path: string,
    options: Parameters<typeof $fetch<T>>[1] = {},
    requiresAuth = true,
  ): Promise<T> {
    const baseURL = config.public.apiBaseUrl as string

    const doFetch = async (token: string | null) => {
      const headers: Record<string, string> = {
        ...(options.headers as Record<string, string> | undefined),
      }
      if (token) {
        headers.Authorization = `Bearer ${token}`
      }
      return await $fetch<T>(path, {
        baseURL,
        ...options,
        headers,
      })
    }

    try {
      const token = requiresAuth ? await getAccessToken(false) : null
      return await doFetch(token)
    } catch (err: unknown) {
      const parsed = parseApiError(err)
      if (requiresAuth && parsed.status === 401) {
        const refreshed = await getAccessToken(true)
        if (refreshed) {
          try {
            return await doFetch(refreshed)
          } catch (retryErr: unknown) {
            throw parseApiError(retryErr)
          }
        }
      }
      throw parsed
    }
  }

  return { request }
}
