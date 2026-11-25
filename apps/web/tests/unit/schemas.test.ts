import { describe, expect, it } from 'vitest'
import { signUpSchema } from '~/schemas/auth'
import { stepGoalsSchema, stepPersonalSchema, stepSkillsSchema } from '~/schemas/profile'

describe('auth schemas', () => {
  it('validates and normalizes valid signup payload', () => {
    const res = signUpSchema.safeParse({
      full_name: '  Asma   Khan ',
      username: 'Asma_Founder',
      email: 'ASMA@Example.com ',
      phone: '03001234567',
      country_code: 'PK',
      password: 'Password1',
      confirm_password: 'Password1',
      accept_terms: true,
    })
    expect(res.success).toBe(true)
    if (res.success) {
      expect(res.data.full_name).toBe('Asma Khan')
      expect(res.data.username).toBe('asma_founder')
      expect(res.data.email).toBe('asma@example.com')
    }
  })

  it('rejects reserved username and mismatched password', () => {
    const res = signUpSchema.safeParse({
      full_name: 'Asma Khan',
      username: 'admin',
      email: 'asma@example.com',
      phone: '03001234567',
      country_code: 'PK',
      password: 'Password1',
      confirm_password: 'Password2',
      accept_terms: true,
    })
    expect(res.success).toBe(false)
  })
})

describe('profile wizard schemas', () => {
  it('rejects under-18 date of birth and province/city mismatch', () => {
    const today = new Date()
    const underage = `${today.getUTCFullYear() - 16}-01-01`
    const res = stepPersonalSchema.safeParse({
      date_of_birth: underage,
      province: 'Sindh',
      city: 'Lahore',
      preferred_language: 'en',
    })
    expect(res.success).toBe(false)
    if (!res.success) {
      const paths = res.error.issues.map((i) => i.path[0])
      expect(paths).toContain('date_of_birth')
      expect(paths).toContain('city')
    }
  })

  it('requires 1 to 10 skills', () => {
    expect(stepSkillsSchema.safeParse({ skills: [] }).success).toBe(false)
    expect(
      stepSkillsSchema.safeParse({
        skills: [{ skill_id: 1, proficiency: 'intermediate' }],
      }).success,
    ).toBe(true)
  })

  it('validates instagram handle and linkedin URL', () => {
    const ok = stepGoalsSchema.safeParse({
      primary_goal: 'full_time_business',
      weekly_hours: '10_20',
      interested_in: ['ecommerce'],
      instagram_url: '@inkubify.pk',
      linkedin_url: 'https://www.linkedin.com/in/asma',
    })
    expect(ok.success).toBe(true)

    const bad = stepGoalsSchema.safeParse({
      primary_goal: 'full_time_business',
      weekly_hours: '10_20',
      linkedin_url: 'https://twitter.com/asma',
    })
    expect(bad.success).toBe(false)
  })
})
