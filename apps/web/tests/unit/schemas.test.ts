import { describe, expect, it } from 'vitest'
import { loginSchema, signUpSchema } from '~/schemas/auth'
import { stepGoalsSchema, stepPersonalSchema, stepSkillsSchema } from '~/schemas/profile'

describe('auth schemas', () => {
  it('validates and normalizes valid signup payload', () => {
    const res = signUpSchema.safeParse({
      full_name: '  Asma   Khan ', username: 'Asma_Founder', email: 'ASMA@Example.com ',
      phone: '03001234567', country_code: 'PK', password: 'Password1',
      confirm_password: 'Password1', accept_terms: true,
    })
    expect(res.success).toBe(true)
    if (res.success) {
      expect(res.data.full_name).toBe('Asma Khan')
      expect(res.data.username).toBe('asma_founder')
      expect(res.data.email).toBe('asma@example.com')
    }
  })

  it('rejects reserved usernames and mismatched signup passwords', () => {
    const res = signUpSchema.safeParse({
      full_name: 'Asma Khan', username: 'admin', email: 'asma@example.com',
      phone: '03001234567', country_code: 'PK', password: 'Password1',
      confirm_password: 'Password2', accept_terms: true,
    })
    expect(res.success).toBe(false)
  })

  it('requires username rather than email for login', () => {
    expect(loginSchema.safeParse({ username: 'asma_founder', password: 'Password1' }).success).toBe(true)
    expect(loginSchema.safeParse({ email: 'asma@example.com', password: 'Password1' }).success).toBe(false)
  })
})

describe('profile wizard schemas', () => {
  it('rejects under-18 date of birth and province/city mismatch', () => {
    const today = new Date()
    const underage = `${today.getUTCFullYear() - 16}-01-01`
    const res = stepPersonalSchema.safeParse({
      full_name: 'Asma Khan', date_of_birth: underage, province: 'Sindh',
      city: 'Lahore', preferred_language: 'en',
    })
    expect(res.success).toBe(false)
    if (!res.success) {
      const paths = res.error.issues.map((i) => i.path[0])
      expect(paths).toContain('date_of_birth')
      expect(paths).toContain('city')
    }
  })

  it('allows custom skills when no catalog skill is selected', () => {
    const res = stepSkillsSchema.safeParse({
      skills: [], other_skills: 'Photography and copywriting',
      experience_level: 'beginner', experience_years: '', portfolio_url: '',
      linkedin_url: '', github_url: '', availability: 'part_time',
    })
    expect(res.success).toBe(true)
  })

  it('validates category-specific business models and financial inputs', () => {
    const valid = stepGoalsSchema.safeParse({
      business_category: 'ecommerce', business_model: 'dropshipping',
      target_audience: ['individual_consumers'],
      primary_goal: 'Build a differentiated online store',
      expected_business_timeline: '3_6_months', available_budget_pkr: '150000',
      available_resources: ['laptop_computer'], team_members: '1',
      resource_info: ['personal_savings'],
    })
    expect(valid.success).toBe(true)
    const invalid = stepGoalsSchema.safeParse({
      business_category: 'ecommerce', business_model: 'b2c',
      primary_goal: 'Build an online store', expected_business_timeline: '3_6_months',
      available_budget_pkr: '', team_members: '', available_resources: [], resource_info: [],
    })
    expect(invalid.success).toBe(false)
  })
})
