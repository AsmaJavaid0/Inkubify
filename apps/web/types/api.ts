export type Proficiency = 'beginner' | 'intermediate' | 'advanced'
export type OnboardingStatus = 'not_started' | 'in_progress' | 'completed'

export interface SkillCatalogItem {
  id: number
  slug: string
  name: string
  category: string
}

export interface ProfileSkill {
  skill_id: number
  slug: string
  name: string
  proficiency: Proficiency
}

export interface OnboardingState {
  status: OnboardingStatus
  step: number
  completed_at: string | null
}

export interface UserProfile {
  id: string
  username: string
  full_name: string
  email: string | null
  phone_e164: string
  country_code: string
  avatar_url: string | null
  date_of_birth: string | null
  gender: string | null
  province: string | null
  city: string | null
  bio: string | null
  preferred_language: 'en' | 'ur'
  education_level: string | null
  field_of_study: string | null
  occupation_status: string | null
  work_experience: string | null
  prior_business: string | null
  primary_goal: string | null
  weekly_hours: string | null
  interested_in: ('ecommerce' | 'tech_services')[]
  instagram_url: string | null
  linkedin_url: string | null
  skills: ProfileSkill[]
  onboarding: OnboardingState
  profile_completion: number
}

export interface ApiErrorBody {
  error: {
    code: string
    message: string
    fields?: Record<string, string>
  }
}

export interface UsernameAvailabilityResponse {
  available: boolean
}
