import type { ApiErrorBody } from '~/types/api'

export class ApiClientError extends Error {
  status: number
  code: string
  fields: Record<string, string>

  constructor(
    status: number,
    code: string,
    message: string,
    fields: Record<string, string> = {},
  ) {
    super(message)
    this.name = 'ApiClientError'
    this.status = status
    this.code = code
    this.fields = fields
  }
}

export function mapAuthErrorMessage(err: unknown): string {
  const rawMessage =
    typeof err === 'object' && err !== null && 'message' in err
      ? String((err as { message: unknown }).message)
      : String(err ?? '')
  const lower = rawMessage.toLowerCase()

  if (lower.includes('database error saving new user')) {
    if (import.meta.dev) {
      console.warn('[auth] Sign-up DB trigger error:', rawMessage)
    }
    return 'That username or phone number is already in use.'
  }
  if (lower.includes('invalid login credentials') || lower.includes('invalid_credentials')) {
    return 'Invalid email or password.'
  }
  if (lower.includes('email not confirmed')) {
    return 'Please verify your email address before logging in.'
  }
  if (lower.includes('user already registered') || lower.includes('already been registered')) {
    return 'If an account with that email exists, please check your inbox or log in.'
  }
  if (lower.includes('password') && (lower.includes('weak') || lower.includes('least'))) {
    return 'Password must be at least 8 characters and include uppercase, lowercase, and a number.'
  }
  if (lower.includes('rate limit') || lower.includes('too many requests') || lower.includes('429')) {
    return 'Too many attempts, please try again in a minute.'
  }
  if (lower.includes('failed to fetch') || lower.includes('network')) {
    return 'You appear to be offline. Please check your internet connection and try again.'
  }
  return 'Something went wrong. Please try again.'
}

export function parseApiError(err: unknown): ApiClientError {
  if (err instanceof ApiClientError) return err

  const fetchErr = err as {
    statusCode?: number
    status?: number
    data?: Partial<ApiErrorBody>
    message?: string
  }
  const status = fetchErr?.statusCode ?? fetchErr?.status ?? 500
  const body = fetchErr?.data?.error
  if (body) {
    return new ApiClientError(
      status,
      body.code || 'server_error',
      body.message || 'Request failed',
      body.fields || {},
    )
  }
  if (status === 429) {
    return new ApiClientError(429, 'rate_limited', 'Too many attempts, please try again in a minute.')
  }
  return new ApiClientError(status, 'server_error', mapAuthErrorMessage(err))
}
