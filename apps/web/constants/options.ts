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

export const AVAILABILITY_OPTIONS: OptionItem[] = [
  { value: 'full_time', label: 'Full-time' },
  { value: 'part_time', label: 'Part-time' },
  { value: 'evenings_weekends', label: 'Evenings / weekends' },
  { value: 'flexible', label: 'Flexible' },
]

export const BUSINESS_CATEGORY_OPTIONS: OptionItem[] = [
  { value: 'ecommerce', label: 'E-commerce' },
  { value: 'technology_based', label: 'Technology-based business' },
]
export const ECOMMERCE_MODEL_OPTIONS: OptionItem[] = [
  { value: 'b2b', label: 'B2B' }, { value: 'd2c', label: 'D2C' },
  { value: 'dropshipping', label: 'Dropshipping' },
]
export const TECHNOLOGY_MODEL_OPTIONS: OptionItem[] = [
  { value: 'b2b', label: 'B2B' }, { value: 'b2c', label: 'B2C' },
]
export const BUSINESS_TIMELINE_OPTIONS: OptionItem[] = [
  { value: 'within_3_months', label: 'Within 3 months' },
  { value: '3_6_months', label: '3–6 months' },
  { value: '6_12_months', label: '6–12 months' },
  { value: '1_2_years', label: '1–2 years' },
  { value: 'exploring', label: 'Still exploring' },
]
export const TARGET_AUDIENCE_OPTIONS: OptionItem[] = [
  { value: 'individual_consumers', label: 'Individual consumers' },
  { value: 'small_businesses', label: 'Small businesses' },
  { value: 'startups', label: 'Startups' },
  { value: 'enterprises', label: 'Large enterprises' },
  { value: 'students', label: 'Students' },
  { value: 'professionals', label: 'Working professionals' },
  { value: 'government', label: 'Government organizations' },
  { value: 'nonprofits', label: 'Non-profit organizations' },
]
export const AVAILABLE_RESOURCE_OPTIONS: OptionItem[] = [
  { value: 'laptop_computer', label: 'Laptop / computer' },
  { value: 'internet', label: 'Reliable internet' },
  { value: 'workspace', label: 'Workspace' },
  { value: 'equipment', label: 'Equipment / tools' },
  { value: 'inventory', label: 'Initial inventory' },
  { value: 'supplier_network', label: 'Supplier network' },
  { value: 'transport', label: 'Transport' },
  { value: 'team', label: 'Team / collaborators' },
  { value: 'other', label: 'Other resources' },
]
export const RESOURCE_INFO_OPTIONS: OptionItem[] = [
  { value: 'personal_savings', label: 'Personal savings' },
  { value: 'family_support', label: 'Family support' },
  { value: 'bank_loan', label: 'Bank loan' },
  { value: 'investor_funding', label: 'Investor funding' },
  { value: 'grant', label: 'Grant / funding program' },
  { value: 'incubator_support', label: 'Incubator support' },
  { value: 'other', label: 'Other source of support' },
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
  { number: 1, title: 'Personal Information', shortTitle: 'Personal' },
  { number: 2, title: 'Education & Background', shortTitle: 'Background' },
  { number: 3, title: 'Skills & Expertise', shortTitle: 'Skills' },
  { number: 4, title: 'Business & Resources', shortTitle: 'Business' },
  { number: 5, title: 'Review & Finish', shortTitle: 'Review' },
] as const
