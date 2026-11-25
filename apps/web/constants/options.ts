export interface OptionItem<T extends string = string> {
  value: T
  label: string
  description?: string
}

export const GENDER_OPTIONS: OptionItem[] = [
  { value: 'female', label: 'Female' },
  { value: 'male', label: 'Male' },
  { value: 'other', label: 'Other' },
  { value: 'prefer_not_to_say', label: 'Prefer not to say' },
]

export const LANGUAGE_OPTIONS: OptionItem<'en' | 'ur'>[] = [
  { value: 'en', label: 'English' },
  { value: 'ur', label: 'Urdu (اردو)' },
]

export const EDUCATION_OPTIONS: OptionItem[] = [
  { value: 'matric_olevels', label: 'Matric / O-Levels' },
  { value: 'intermediate_alevels', label: 'Intermediate / A-Levels' },
  { value: 'diploma', label: 'Diploma / Technical Certificate' },
  { value: 'bachelors', label: "Bachelor's Degree" },
  { value: 'masters', label: "Master's Degree" },
  { value: 'phd', label: 'PhD / Doctorate' },
  { value: 'other', label: 'Other' },
]

export const OCCUPATION_OPTIONS: OptionItem[] = [
  { value: 'student', label: 'Student' },
  { value: 'employed', label: 'Employed (Full/Part-time)' },
  { value: 'self_employed', label: 'Self-employed' },
  { value: 'freelancer', label: 'Freelancer' },
  { value: 'unemployed', label: 'Currently unemployed' },
  { value: 'other', label: 'Other' },
]

export const WORK_EXPERIENCE_OPTIONS: OptionItem[] = [
  { value: 'none', label: 'No prior work experience' },
  { value: 'lt_1', label: 'Less than 1 year' },
  { value: '1_3', label: '1 – 3 years' },
  { value: '3_5', label: '3 – 5 years' },
  { value: '5_plus', label: '5+ years' },
]

export const PRIOR_BUSINESS_OPTIONS: OptionItem[] = [
  { value: 'none', label: 'Never run a business' },
  { value: 'tried_before', label: 'Tried before, stopped' },
  { value: 'running_now', label: 'Running one now' },
]

export const PROFICIENCY_OPTIONS: OptionItem<'beginner' | 'intermediate' | 'advanced'>[] = [
  { value: 'beginner', label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced', label: 'Advanced' },
]

export const PRIMARY_GOAL_OPTIONS: OptionItem[] = [
  { value: 'side_income', label: 'Build a side income' },
  { value: 'full_time_business', label: 'Launch a full-time business' },
  { value: 'scale_existing', label: 'Scale an existing venture' },
  { value: 'explore_learn', label: 'Explore & learn first' },
]

export const WEEKLY_HOURS_OPTIONS: OptionItem[] = [
  { value: 'lt_5', label: 'Less than 5 hours / week' },
  { value: '5_10', label: '5 – 10 hours / week' },
  { value: '10_20', label: '10 – 20 hours / week' },
  { value: '20_40', label: '20 – 40 hours / week' },
  { value: '40_plus', label: '40+ hours / week (full-time)' },
]

export const INTERESTED_IN_OPTIONS: OptionItem<'ecommerce' | 'tech_services'>[] = [
  { value: 'ecommerce', label: 'E-commerce (B2B, D2C, Dropshipping)' },
  { value: 'tech_services', label: 'Tech-based (Apps, AI/Data, UI/UX)' },
]

export const WELCOME_SLIDES = [
  {
    title: 'Ideas → Plans',
    description:
      'Tell us the business you want to start and get a clear, step-by-step roadmap built for Pakistan.',
  },
  {
    title: 'Stay on track',
    description:
      "Reminders, milestone tracking and early warnings so setbacks don't catch you off guard.",
  },
  {
    title: 'Decide with evidence',
    description:
      'Every suggestion is labelled: verified, estimate, assumption or AI hypothesis. You stay in control.',
  },
] as const

export const WIZARD_STEPS = [
  { number: 1, title: 'Personal', shortTitle: 'Personal' },
  { number: 2, title: 'Background', shortTitle: 'Background' },
  { number: 3, title: 'Skills & Expertise', shortTitle: 'Skills' },
  { number: 4, title: 'Goals & Availability', shortTitle: 'Goals' },
  { number: 5, title: 'Review & Finish', shortTitle: 'Review' },
] as const
