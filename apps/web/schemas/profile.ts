import { z } from 'zod'
import { PROVINCES, PROVINCE_CITIES, type Province } from '~/constants/geo'

const CITY_REGEX = /^[A-Za-z0-9 .'-]{2,60}$/
const FULL_NAME_REGEX = /^[A-Za-zÀ-ÖØ-öø-ÿ .'-]+$/

export function isAtLeast18(dobString: string): boolean {
  const parsed = new Date(`${dobString}T00:00:00Z`)
  if (Number.isNaN(parsed.getTime())) return false
  const today = new Date()
  const yearDiff = today.getUTCFullYear() - parsed.getUTCFullYear()
  const monthDiff = today.getUTCMonth() - parsed.getUTCMonth()
  const dayDiff = today.getUTCDate() - parsed.getUTCDate()
  return yearDiff - (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0) ? 1 : 0) >= 18
}
export function ageFromDob(dobString: string): number | null {
  if (!dobString) return null
  const dob = new Date(`${dobString}T00:00:00Z`)
  if (Number.isNaN(dob.getTime())) return null
  const today = new Date()
  let age = today.getUTCFullYear() - dob.getUTCFullYear()
  if (today.getUTCMonth() < dob.getUTCMonth() ||
      (today.getUTCMonth() === dob.getUTCMonth() && today.getUTCDate() < dob.getUTCDate())) age--
  return age >= 0 ? age : null
}
function validHttpUrl(raw: string): boolean {
  if (!raw.trim()) return true
  try {
    const url = new URL(raw.startsWith('http') ? raw : `https://${raw}`)
    return ['http:', 'https:'].includes(url.protocol) && !!url.hostname
  } catch { return false }
}

export const stepPersonalSchema = z.object({
  full_name: z.string().trim().min(2).max(60).regex(FULL_NAME_REGEX, 'Enter a valid full name'),
  avatar_url: z.string().nullable().optional(),
  date_of_birth: z.string().min(1, 'Date of birth is required')
    .refine((v) => v >= '1930-01-01', 'Date of birth cannot be before 1930')
    .refine((v) => new Date(`${v}T00:00:00Z`) <= new Date(), 'Date of birth cannot be in the future')
    .refine(isAtLeast18, 'You must be at least 18 years old'),
  gender: z.enum(['female', 'male', 'other', 'prefer_not_to_say']).nullable().optional(),
  address: z.string().trim().max(250).nullable().optional(),
  province: z.enum(PROVINCES, { errorMap: () => ({ message: 'Please select a province or territory' }) }),
  city: z.string().trim().min(2, 'Please select or enter your city').max(60)
    .refine((v) => v.toLowerCase() !== 'other', 'Please enter your city name')
    .refine((v) => CITY_REGEX.test(v), 'Please enter a valid city name'),
  bio: z.string().max(280).nullable().optional(),
  preferred_language: z.enum(['en', 'ur']).default('en'),
}).superRefine((data, ctx) => {
  const cityLower = data.city.toLowerCase()
  for (const [prov, cities] of Object.entries(PROVINCE_CITIES) as [Province, readonly string[]][]) {
    if (prov !== data.province && cities.some((c) => c.toLowerCase() === cityLower)) {
      const selected = PROVINCE_CITIES[data.province].some((c) => c.toLowerCase() === cityLower)
      if (!selected) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ['city'], message: `${data.city} does not belong to ${data.province}` })
    }
  }
})

export const stepBackgroundSchema = z.object({
  education_level: z.enum(['matric_olevels', 'intermediate_alevels', 'diploma', 'bachelors', 'masters', 'phd', 'other']),
  field_of_study: z.string().trim().refine((v) => v === '' || (v.length >= 2 && v.length <= 80), 'Field of study must be 2–80 characters').nullable().optional(),
  occupation_status: z.enum(['student', 'employed', 'self_employed', 'freelancer', 'unemployed', 'other']),
  prior_business: z.enum(['none', 'tried_before', 'running_now']),
})

export const stepSkillsSchema = z.object({
  skills: z.array(z.object({
    skill_id: z.number().int().positive(),
    proficiency: z.enum(['beginner', 'intermediate', 'advanced']),
  })).max(10),
  other_skills: z.string().trim().max(1000).default(''),
  experience_level: z.enum(['beginner', 'intermediate', 'advanced']),
  experience_years: z.preprocess((v) => v === '' || v == null ? null : Number(v), z.number().int().min(0).max(60).nullable()),
  portfolio_url: z.string().trim().refine(validHttpUrl, 'Enter a valid portfolio URL').default(''),
  linkedin_url: z.string().trim().refine((v) => !v || (validHttpUrl(v) && /linkedin\.com/i.test(v)), 'Enter a valid LinkedIn URL').default(''),
  github_url: z.string().trim().refine((v) => !v || (validHttpUrl(v) && /github\.com/i.test(v)), 'Enter a valid GitHub URL').default(''),
  availability: z.enum(['full_time', 'part_time', 'evenings_weekends', 'flexible']),
}).superRefine((data, ctx) => {
  if (!data.skills.length && !data.other_skills.trim()) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, path: ['skills'], message: 'Select a technical skill or describe your other skills' })
  }
})

export const stepGoalsSchema = z.object({
  business_category: z.enum(['ecommerce', 'technology_based']),
  business_model: z.enum(['b2b', 'd2c', 'dropshipping', 'b2c']),
  target_audience: z.array(z.enum(['individual_consumers', 'small_businesses', 'startups', 'enterprises', 'students', 'professionals', 'government', 'nonprofits'])).default([]),
  primary_goal: z.string().trim().min(2, 'Describe your primary business goal').max(500),
  expected_business_timeline: z.enum(['within_3_months', '3_6_months', '6_12_months', '1_2_years', 'exploring']),
  available_budget_pkr: z.preprocess((v) => v === '' || v == null ? null : Number(v), z.number().int().min(0).max(1_000_000_000_000).nullable()),
  available_resources: z.array(z.enum(['laptop_computer', 'internet', 'workspace', 'equipment', 'inventory', 'supplier_network', 'transport', 'team', 'other'])).default([]),
  team_members: z.preprocess((v) => v === '' || v == null ? null : Number(v), z.number().int().min(0).max(100).nullable()),
  resource_info: z.array(z.enum(['personal_savings', 'family_support', 'bank_loan', 'investor_funding', 'grant', 'incubator_support', 'other'])).default([]),
}).superRefine((data, ctx) => {
  const allowed = data.business_category === 'ecommerce' ? ['b2b', 'd2c', 'dropshipping'] : ['b2b', 'b2c']
  if (!allowed.includes(data.business_model)) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ['business_model'], message: 'Choose a model supported by the selected category' })
})
