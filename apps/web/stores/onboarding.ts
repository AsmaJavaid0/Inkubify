import { defineStore } from 'pinia'
import type { Proficiency, UserProfile } from '~/types/api'

export interface WizardDraft {
  // Step 1
  avatar_url: string | null
  date_of_birth: string
  gender: string | null
  province: string
  city: string
  bio: string
  preferred_language: 'en' | 'ur'
  // Step 2
  education_level: string
  field_of_study: string
  occupation_status: string
  work_experience: string
  prior_business: string
  // Step 3
  skills: { skill_id: number; proficiency: Proficiency }[]
  // Step 4
  primary_goal: string
  weekly_hours: string
  interested_in: ('ecommerce' | 'tech_services')[]
  instagram_url: string
  linkedin_url: string
}

function emptyDraft(): WizardDraft {
  return {
    avatar_url: null,
    date_of_birth: '',
    gender: null,
    province: '',
    city: '',
    bio: '',
    preferred_language: 'en',
    education_level: '',
    field_of_study: '',
    occupation_status: '',
    work_experience: '',
    prior_business: '',
    skills: [],
    primary_goal: '',
    weekly_hours: '',
    interested_in: [],
    instagram_url: '',
    linkedin_url: '',
  }
}

export const useOnboardingStore = defineStore('onboarding', () => {
  const currentStep = ref(1)
  const draft = ref<WizardDraft>(emptyDraft())

  function hydrateFromProfile(p: UserProfile) {
    currentStep.value = Math.min(5, Math.max(1, p.onboarding.step || 1))
    draft.value = {
      avatar_url: p.avatar_url,
      date_of_birth: p.date_of_birth ?? '',
      gender: p.gender ?? null,
      province: p.province ?? '',
      city: p.city ?? '',
      bio: p.bio ?? '',
      preferred_language: p.preferred_language ?? 'en',
      education_level: p.education_level ?? '',
      field_of_study: p.field_of_study ?? '',
      occupation_status: p.occupation_status ?? '',
      work_experience: p.work_experience ?? '',
      prior_business: p.prior_business ?? '',
      skills: p.skills.map((s) => ({
        skill_id: s.skill_id,
        proficiency: s.proficiency,
      })),
      primary_goal: p.primary_goal ?? '',
      weekly_hours: p.weekly_hours ?? '',
      interested_in: [...(p.interested_in ?? [])],
      instagram_url: p.instagram_url ?? '',
      linkedin_url: p.linkedin_url ?? '',
    }
  }

  function reset() {
    currentStep.value = 1
    draft.value = emptyDraft()
  }

  return {
    currentStep,
    draft,
    hydrateFromProfile,
    reset,
  }
})
