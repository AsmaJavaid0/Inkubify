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
          address: string | null
          province: string | null
          city: string | null
          bio: string | null
          preferred_language: 'en' | 'ur'
          education_level: 'matric_olevels' | 'intermediate_alevels' | 'diploma' | 'bachelors' | 'masters' | 'phd' | 'other' | null
          field_of_study: string | null
          occupation_status: 'student' | 'employed' | 'self_employed' | 'freelancer' | 'unemployed' | 'other' | null
          prior_business: 'none' | 'tried_before' | 'running_now' | null
          other_skills: string | null
          experience_level: 'beginner' | 'intermediate' | 'advanced' | null
          experience_years: number | null
          portfolio_url: string | null
          linkedin_url: string | null
          github_url: string | null
          availability: 'full_time' | 'part_time' | 'evenings_weekends' | 'flexible' | null
          business_category: 'ecommerce' | 'technology_based' | null
          business_model: 'b2b' | 'd2c' | 'dropshipping' | 'b2c' | null
          target_audience: string[]
          primary_goal: string | null
          expected_business_timeline: 'within_3_months' | '3_6_months' | '6_12_months' | '1_2_years' | 'exploring' | null
          available_budget_pkr: number | null
          available_resources: string[]
          team_members: number | null
          resource_info: string[]
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
          address?: string | null
          province?: string | null
          city?: string | null
          bio?: string | null
          preferred_language?: 'en' | 'ur'
          education_level?: 'matric_olevels' | 'intermediate_alevels' | 'diploma' | 'bachelors' | 'masters' | 'phd' | 'other' | null
          field_of_study?: string | null
          occupation_status?: 'student' | 'employed' | 'self_employed' | 'freelancer' | 'unemployed' | 'other' | null
          prior_business?: 'none' | 'tried_before' | 'running_now' | null
          other_skills?: string | null
          experience_level?: 'beginner' | 'intermediate' | 'advanced' | null
          experience_years?: number | null
          portfolio_url?: string | null
          linkedin_url?: string | null
          github_url?: string | null
          availability?: 'full_time' | 'part_time' | 'evenings_weekends' | 'flexible' | null
          business_category?: 'ecommerce' | 'technology_based' | null
          business_model?: 'b2b' | 'd2c' | 'dropshipping' | 'b2c' | null
          target_audience?: string[]
          primary_goal?: string | null
          expected_business_timeline?: 'within_3_months' | '3_6_months' | '6_12_months' | '1_2_years' | 'exploring' | null
          available_budget_pkr?: number | null
          available_resources?: string[]
          team_members?: number | null
          resource_info?: string[]
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
