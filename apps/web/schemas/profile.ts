import { z } from 'zod'
import { PROVINCES, PROVINCE_CITIES, type Province } from '~/constants/geo'

const CITY_REGEX = /^[A-Za-z0-9 .'-]{2,60}$/
const INSTAGRAM_HANDLE_REGEX = /^[A-Za-z0-9._]{1,30}$/

export function isAtLeast18(dobString: string): boolean {
  const parsed = new Date(`${dobString}T00:00:00Z`)
  if (Number.isNaN(parsed.getTime())) return false
  const today = new Date()
  const yearDiff = today.getUTCFullYear() - parsed.getUTCFullYear()
  const monthDiff = today.getUTCMonth() - parsed.getUTCMonth()
  const dayDiff = today.getUTCDate() - parsed.getUTCDate()
  const age = yearDiff - (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0) ? 1 : 0)
  return age >= 18
}

export function isValidInstagram(raw: string): boolean {
  const val = raw.trim()
  if (!val) return true
  if (val.startsWith('@')) {
    return INSTAGRAM_HANDLE_REGEX.test(val.slice(1).replace(/\/+$/, ''))
  }
  if (val.toLowerCase().includes('instagram.com')) {
    try {
      const url = new URL(val.startsWith('http') ? val : `https://${val}`)
      const host = url.hostname.toLowerCase()
      if (host !== 'instagram.com' && host !== 'www.instagram.com') return false
      const parts = url.pathname.split('/').filter(Boolean)
      return parts.length > 0 && INSTAGRAM_HANDLE_REGEX.test(parts[0]!.replace(/^@/, ''))
    } catch {
      return false
    }
  }
  return INSTAGRAM_HANDLE_REGEX.test(val.replace(/\/+$/, ''))
}

export function isValidLinkedIn(raw: string): boolean {
  const val = raw.trim()
  if (!val) return true
  try {
    const url = new URL(val.startsWith('http') ? val : `https://${val}`)
    const host = url.hostname.toLowerCase()
    const validHost = host === 'linkedin.com' || host.endsWith('.linkedin.com')
    return validHost && url.pathname.length > 1
  } catch {
    return false
  }
}

export const stepPersonalSchema = z
  .object({
    avatar_url: z.string().nullable().optional(),
    date_of_birth: z
      .string()
      .min(1, 'Date of birth is required')
      .refine((v) => v >= '1930-01-01', 'Date of birth cannot be before 1930')
      .refine((v) => new Date(`${v}T00:00:00Z`) <= new Date(), 'Date of birth cannot be in the future')
      .refine(isAtLeast18, 'You must be at least 18 years old'),
    gender: z
      .enum(['female', 'male', 'other', 'prefer_not_to_say'])
      .nullable()
      .optional(),
    province: z.enum(PROVINCES, {
      errorMap: () => ({ message: 'Please select a province or territory' }),
    }),
    city: z
      .string()
      .trim()
      .min(2, 'Please select or enter your city')
      .max(60, 'City name must be 60 characters or fewer')
      .refine((v) => v.toLowerCase() !== 'other', 'Please enter your city name')
      .refine((v) => CITY_REGEX.test(v), 'Please enter a valid city name'),
    bio: z
      .string()
      .max(280, 'Bio must be 280 characters or fewer')
      .nullable()
      .optional(),
    preferred_language: z.enum(['en', 'ur']).default('en'),
  })
  .superRefine((data, ctx) => {
    const cityLower = data.city.toLowerCase()
    for (const [prov, cities] of Object.entries(PROVINCE_CITIES) as [Province, readonly string[]][]) {
      if (prov !== data.province && cities.some((c) => c.toLowerCase() === cityLower)) {
        const alsoInSelected = PROVINCE_CITIES[data.province].some(
          (c) => c.toLowerCase() === cityLower,
        )
        if (!alsoInSelected) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ['city'],
            message: `${data.city} does not belong to ${data.province}`,
          })
        }
      }
    }
  })

export const stepBackgroundSchema = z.object({
  education_level: z.enum(
    ['matric_olevels', 'intermediate_alevels', 'diploma', 'bachelors', 'masters', 'phd', 'other'],
    { errorMap: () => ({ message: 'Please select your education level' }) },
  ),
  field_of_study: z
    .string()
    .trim()
    .refine((v) => v === '' || (v.length >= 2 && v.length <= 80), {
      message: 'Field of study must be 2–80 characters',
    })
    .nullable()
    .optional(),
  occupation_status: z.enum(
    ['student', 'employed', 'self_employed', 'freelancer', 'unemployed', 'other'],
    { errorMap: () => ({ message: 'Please select your current status' }) },
  ),
  work_experience: z.enum(['none', 'lt_1', '1_3', '3_5', '5_plus'], {
    errorMap: () => ({ message: 'Please select your work experience' }),
  }),
  prior_business: z.enum(['none', 'tried_before', 'running_now'], {
    errorMap: () => ({ message: 'Please select your prior business experience' }),
  }),
})

export const stepSkillsSchema = z.object({
  skills: z
    .array(
      z.object({
        skill_id: z.number().int().positive(),
        proficiency: z.enum(['beginner', 'intermediate', 'advanced']),
      }),
    )
    .min(1, 'Please select at least 1 skill')
    .max(10, 'You can select up to 10 skills'),
})

export const stepGoalsSchema = z.object({
  primary_goal: z.enum(
    ['side_income', 'full_time_business', 'scale_existing', 'explore_learn'],
    { errorMap: () => ({ message: 'Please select your primary goal' }) },
  ),
  weekly_hours: z.enum(['lt_5', '5_10', '10_20', '20_40', '40_plus'], {
    errorMap: () => ({ message: 'Please select weekly time available' }),
  }),
  interested_in: z.array(z.enum(['ecommerce', 'tech_services'])).default([]),
  instagram_url: z
    .string()
    .trim()
    .refine(isValidInstagram, 'Enter a valid Instagram handle or URL')
    .nullable()
    .optional(),
  linkedin_url: z
    .string()
    .trim()
    .refine(isValidLinkedIn, 'Enter a valid linkedin.com profile URL')
    .nullable()
    .optional(),
})
