export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string
          username: string
          full_name: string
          phone_e164: string
          country_code: string
          avatar_url: string | null
          date_of_birth: string | null
          gender: 'female' | 'male' | 'other' | 'prefer_not_to_say' | null
          province: string | null
          city: string | null
          bio: string | null
          preferred_language: 'en' | 'ur'
          education_level:
            | 'matric_olevels'
            | 'intermediate_alevels'
            | 'diploma'
            | 'bachelors'
            | 'masters'
            | 'phd'
            | 'other'
            | null
          field_of_study: string | null
          occupation_status:
            | 'student'
            | 'employed'
            | 'self_employed'
            | 'freelancer'
            | 'unemployed'
            | 'other'
            | null
          work_experience: 'none' | 'lt_1' | '1_3' | '3_5' | '5_plus' | null
          prior_business: 'none' | 'tried_before' | 'running_now' | null
          primary_goal:
            | 'side_income'
            | 'full_time_business'
            | 'scale_existing'
            | 'explore_learn'
            | null
          weekly_hours: 'lt_5' | '5_10' | '10_20' | '20_40' | '40_plus' | null
          interested_in: string[]
          instagram_url: string | null
          linkedin_url: string | null
          onboarding_status: 'not_started' | 'in_progress' | 'completed'
          onboarding_step: number
          profile_completion: number
          onboarding_completed_at: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          username: string
          full_name: string
          phone_e164: string
          country_code?: string
        }
        Update: {
          full_name?: string
          avatar_url?: string | null
          date_of_birth?: string | null
          gender?: 'female' | 'male' | 'other' | 'prefer_not_to_say' | null
          province?: string | null
          city?: string | null
          bio?: string | null
          preferred_language?: 'en' | 'ur'
          education_level?:
            | 'matric_olevels'
            | 'intermediate_alevels'
            | 'diploma'
            | 'bachelors'
            | 'masters'
            | 'phd'
            | 'other'
            | null
          field_of_study?: string | null
          occupation_status?:
            | 'student'
            | 'employed'
            | 'self_employed'
            | 'freelancer'
            | 'unemployed'
            | 'other'
            | null
          work_experience?: 'none' | 'lt_1' | '1_3' | '3_5' | '5_plus' | null
          prior_business?: 'none' | 'tried_before' | 'running_now' | null
          primary_goal?:
            | 'side_income'
            | 'full_time_business'
            | 'scale_existing'
            | 'explore_learn'
            | null
          weekly_hours?: 'lt_5' | '5_10' | '10_20' | '20_40' | '40_plus' | null
          interested_in?: string[]
          instagram_url?: string | null
          linkedin_url?: string | null
          onboarding_step?: number
        }
      }
      skills: {
        Row: {
          id: number
          slug: string
          name: string
          category: string
          sort_order: number
          is_active: boolean
        }
      }
      profile_skills: {
        Row: {
          profile_id: string
          skill_id: number
          proficiency: 'beginner' | 'intermediate' | 'advanced'
          created_at: string
        }
        Insert: {
          profile_id: string
          skill_id: number
          proficiency: 'beginner' | 'intermediate' | 'advanced'
        }
        Update: {
          proficiency?: 'beginner' | 'intermediate' | 'advanced'
        }
      }
    }
  }
}
