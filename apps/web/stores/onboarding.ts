import { defineStore } from 'pinia'
import type { Proficiency, UserProfile } from '~/types/api'

export interface WizardDraft {
  avatar_url: string | null
  full_name: string
  date_of_birth: string
  gender: string | null
  address: string
  province: string
  city: string
  bio: string
  preferred_language: 'en' | 'ur'
  education_level: string
  field_of_study: string
  occupation_status: string
  prior_business: string
  skills: { skill_id: number; proficiency: Proficiency }[]
  other_skills: string
  experience_level: Proficiency | ''
  experience_years: string
  portfolio_url: string
  linkedin_url: string
  github_url: string
  availability: string
  business_category: 'ecommerce' | 'technology_based' | ''
  business_model: string
  target_audience: string[]
  primary_goal: string
  expected_business_timeline: string
  available_budget_pkr: string
  available_resources: string[]
  team_members: string
  resource_info: string[]
}
function emptyDraft(): WizardDraft {
  return {
    avatar_url: null, full_name: '', date_of_birth: '', gender: null, address: '',
    province: '', city: '', bio: '', preferred_language: 'en',
    education_level: '', field_of_study: '', occupation_status: '', prior_business: '',
    skills: [], other_skills: '', experience_level: '', experience_years: '',
    portfolio_url: '', linkedin_url: '', github_url: '', availability: '',
    business_category: '', business_model: '', target_audience: [], primary_goal: '',
    expected_business_timeline: '', available_budget_pkr: '', available_resources: [],
    team_members: '', resource_info: [],
  }
}
export const useOnboardingStore = defineStore('onboarding', () => {
  const currentStep = ref(1)
  const draft = ref<WizardDraft>(emptyDraft())
  function hydrateFromProfile(p: UserProfile) {
    currentStep.value = Math.min(5, Math.max(1, p.onboarding.step || 1))
    draft.value = {
      avatar_url: p.avatar_url, full_name: p.full_name ?? '', date_of_birth: p.date_of_birth ?? '',
      gender: p.gender ?? null, address: p.address ?? '', province: p.province ?? '',
      city: p.city ?? '', bio: p.bio ?? '', preferred_language: p.preferred_language ?? 'en',
      education_level: p.education_level ?? '', field_of_study: p.field_of_study ?? '',
      occupation_status: p.occupation_status ?? '', prior_business: p.prior_business ?? '',
      skills: p.skills.map((s) => ({ skill_id: s.skill_id, proficiency: s.proficiency })),
      other_skills: p.other_skills ?? '', experience_level: p.experience_level ?? '',
      experience_years: p.experience_years === null ? '' : String(p.experience_years),
      portfolio_url: p.portfolio_url ?? '', linkedin_url: p.linkedin_url ?? '',
      github_url: p.github_url ?? '', availability: p.availability ?? '',
      business_category: p.business_category ?? '', business_model: p.business_model ?? '',
      target_audience: [...(p.target_audience ?? [])], primary_goal: p.primary_goal ?? '',
      expected_business_timeline: p.expected_business_timeline ?? '',
      available_budget_pkr: p.available_budget_pkr === null ? '' : String(p.available_budget_pkr),
      available_resources: [...(p.available_resources ?? [])],
      team_members: p.team_members === null ? '' : String(p.team_members),
      resource_info: [...(p.resource_info ?? [])],
    }
  }
  function reset() { currentStep.value = 1; draft.value = emptyDraft() }
  return { currentStep, draft, hydrateFromProfile, reset }
})
