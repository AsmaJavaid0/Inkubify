import { defineStore } from 'pinia'
import type { SkillCatalogItem, UserProfile } from '~/types/api'

export const useProfileStore = defineStore('profile', () => {
  const { request } = useApi()

  const profile = ref<UserProfile | null>(null)
  const skillsCatalog = ref<SkillCatalogItem[]>([])
  const loading = ref(false)
  const loaded = ref(false)
  const error = ref<string | null>(null)

  const isOnboardingCompleted = computed(
    () => profile.value?.onboarding.status === 'completed',
  )
  const firstName = computed(() => {
    const full = profile.value?.full_name?.trim()
    return full ? full.split(/\s+/)[0] : 'Founder'
  })

  async function fetchProfile(force = false): Promise<UserProfile | null> {
    if (loaded.value && !force && profile.value) {
      return profile.value
    }
    loading.value = true
    error.value = null
    try {
      const data = await request<UserProfile>('/profiles/me', { method: 'GET' })
      profile.value = data
      loaded.value = true
      return data
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Failed to load profile'
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchSkillsCatalog(): Promise<SkillCatalogItem[]> {
    if (skillsCatalog.value.length > 0) return skillsCatalog.value
    const data = await request<SkillCatalogItem[]>('/catalog/skills', { method: 'GET' })
    skillsCatalog.value = data
    return data
  }

  async function patchProfile(payload: Record<string, unknown>): Promise<UserProfile> {
    const updated = await request<UserProfile>('/profiles/me', {
      method: 'PATCH',
      body: payload,
    })
    profile.value = updated
    loaded.value = true
    return updated
  }

  async function replaceSkills(
    skills: { skill_id: number; proficiency: 'beginner' | 'intermediate' | 'advanced' }[],
  ): Promise<UserProfile> {
    const updated = await request<UserProfile>('/profiles/me/skills', {
      method: 'PUT',
      body: { skills },
    })
    profile.value = updated
    loaded.value = true
    return updated
  }

  async function completeOnboarding(): Promise<UserProfile> {
    const updated = await request<UserProfile>('/profiles/me/onboarding/complete', {
      method: 'POST',
    })
    profile.value = updated
    loaded.value = true
    return updated
  }

  function reset() {
    profile.value = null
    loaded.value = false
    error.value = null
  }

  return {
    profile,
    skillsCatalog,
    loading,
    loaded,
    error,
    isOnboardingCompleted,
    firstName,
    fetchProfile,
    fetchSkillsCatalog,
    patchProfile,
    replaceSkills,
    completeOnboarding,
    reset,
  }
})
