import { describe, expect, it } from 'vitest'
import { maskEmail, normalizePakistaniPhone } from '~/utils/phone'

describe('normalizePakistaniPhone', () => {
  it('normalizes 03XXXXXXXXX format', () => {
    expect(normalizePakistaniPhone('03001234567')).toBe('+923001234567')
  })

  it('normalizes 3XXXXXXXXX format with spaces or dashes', () => {
    expect(normalizePakistaniPhone('300-123 4567')).toBe('+923001234567')
  })

  it('keeps valid +923XXXXXXXXX', () => {
    expect(normalizePakistaniPhone('+923219876543')).toBe('+923219876543')
  })

  it('rejects non-mobile or invalid lengths', () => {
    expect(normalizePakistaniPhone('02112345678')).toBeNull()
    expect(normalizePakistaniPhone('+14155551234')).toBeNull()
    expect(normalizePakistaniPhone('0300123')).toBeNull()
  })
})

describe('maskEmail', () => {
  it('masks local part safely', () => {
    expect(maskEmail('ayesha@example.com')).toBe('ay****@example.com')
  })
})
