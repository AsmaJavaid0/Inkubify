const PK_E164_REGEX = /^\+923\d{9}$/

/**
 * Normalise Pakistani mobile phone inputs (`03XXXXXXXXX`, `3XXXXXXXXX`, `+923XXXXXXXXX`,
 * `923XXXXXXXXX`, with optional spaces or hyphens) to E.164 `+923XXXXXXXXX`.
 * Returns null if the input is not a valid Pakistani mobile number.
 */
export function normalizePakistaniPhone(raw: string): string | null {
  const digitsAndPlus = raw.replace(/[\s\-()]/g, '')
  let candidate = digitsAndPlus

  if (candidate.startsWith('0092')) {
    candidate = `+92${candidate.slice(4)}`
  } else if (candidate.startsWith('92') && !candidate.startsWith('+')) {
    candidate = `+${candidate}`
  } else if (candidate.startsWith('03') && candidate.length === 11) {
    candidate = `+92${candidate.slice(1)}`
  } else if (candidate.startsWith('3') && candidate.length === 10) {
    candidate = `+92${candidate}`
  }

  return PK_E164_REGEX.test(candidate) ? candidate : null
}

/**
 * Format a +923XXXXXXXXX number cleanly for display as `03XX XXXXXXX` or `+92 3XX XXXXXXX`.
 */
export function formatPakistaniPhoneDisplay(e164: string): string {
  if (!PK_E164_REGEX.test(e164)) return e164
  return `+92 ${e164.slice(3, 6)} ${e164.slice(6)}`
}

export function maskEmail(email: string): string {
  const [local, domain] = email.split('@')
  if (!local || !domain) return email
  if (local.length <= 2) return `${local[0] ?? '*'}***@${domain}`
  return `${local.slice(0, 2)}${'*'.repeat(Math.min(5, local.length - 2))}@${domain}`
}
