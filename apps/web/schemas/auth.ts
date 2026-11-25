import { z } from 'zod'
import { RESERVED_USERNAMES } from '~/constants/reservedUsernames'
import { normalizePakistaniPhone } from '~/utils/phone'

const FULL_NAME_REGEX = /^[A-Za-zÀ-ÖØ-öø-ÿ .'-]+$/
const USERNAME_REGEX = /^[a-z][a-z0-9_]{2,19}$/

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .max(72, 'Password must be 72 characters or fewer')
  .regex(/[a-z]/, 'Password needs at least one lowercase letter')
  .regex(/[A-Z]/, 'Password needs at least one uppercase letter')
  .regex(/\d/, 'Password needs at least one number')

export const fullNameSchema = z
  .string()
  .transform((val) => val.trim().replace(/\s+/g, ' '))
  .pipe(
    z
      .string()
      .min(2, 'Full name must be at least 2 characters')
      .max(60, 'Full name must be 60 characters or fewer')
      .regex(
        FULL_NAME_REGEX,
        'Full name may only contain letters, spaces, periods, apostrophes, and hyphens',
      ),
  )

export const usernameSchema = z
  .string()
  .transform((val) => val.trim().toLowerCase())
  .pipe(
    z
      .string()
      .min(3, 'Username must be 3–20 characters')
      .max(20, 'Username must be 3–20 characters')
      .regex(
        USERNAME_REGEX,
        'Start with a letter and use only lowercase letters, numbers, or underscores',
      )
      .refine((val) => !RESERVED_USERNAMES.has(val), {
        message: 'This username is reserved',
      }),
  )

export const emailSchema = z
  .string()
  .transform((val) => val.trim().toLowerCase())
  .pipe(
    z
      .string()
      .min(1, 'Email is required')
      .max(254, 'Email must be 254 characters or fewer')
      .email('Please enter a valid email address'),
  )

export const phoneSchema = z
  .string()
  .trim()
  .min(1, 'Phone number is required')
  .refine((val) => normalizePakistaniPhone(val) !== null, {
    message: 'Enter a valid Pakistani mobile number (e.g. 03001234567 or +923001234567)',
  })

export const signUpSchema = z
  .object({
    full_name: fullNameSchema,
    username: usernameSchema,
    email: emailSchema,
    phone: phoneSchema,
    country_code: z.literal('PK').default('PK'),
    password: passwordSchema,
    confirm_password: z.string().min(1, 'Please confirm your password'),
    accept_terms: z.literal(true, {
      errorMap: () => ({ message: 'You must accept the Terms and Privacy Policy' }),
    }),
  })
  .refine((data) => data.password === data.confirm_password, {
    path: ['confirm_password'],
    message: 'Passwords do not match',
  })

export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, 'Password is required'),
})

export const forgotPasswordSchema = z.object({
  email: emailSchema,
})

export const resetPasswordSchema = z
  .object({
    password: passwordSchema,
    confirm_password: z.string().min(1, 'Please confirm your password'),
  })
  .refine((data) => data.password === data.confirm_password, {
    path: ['confirm_password'],
    message: 'Passwords do not match',
  })
