-- 0007_founder_profile_expansion.sql
-- Extend the existing founder profile; this is not a separate business profile.

alter table public.profiles
  alter column primary_goal type text using primary_goal::text,
  drop column work_experience,
  drop column weekly_hours,
  drop column interested_in,
  drop column instagram_url;

alter table public.profiles
  add column address text check (address is null or char_length(address) <= 250),
  add column other_skills text check (other_skills is null or char_length(other_skills) <= 1000),
  add column experience_level public.proficiency_t,
  add column experience_years smallint check (experience_years between 0 and 60),
  add column portfolio_url text,
  add column github_url text,
  add column availability text check (availability in ('full_time', 'part_time', 'evenings_weekends', 'flexible')),
  add column business_category text check (business_category in ('ecommerce', 'technology_based')),
  add column business_model text,
  add column target_audience text[] not null default '{}',
  add column expected_business_timeline text check (
    expected_business_timeline in ('within_3_months', '3_6_months', '6_12_months', '1_2_years', 'exploring')
  ),
  add column available_budget_pkr bigint check (available_budget_pkr between 0 and 1000000000000),
  add column available_resources text[] not null default '{}',
  add column team_members smallint check (team_members between 0 and 100),
  add column resource_info text[] not null default '{}';

alter table public.profiles
  add constraint profiles_primary_goal_length_check
    check (primary_goal is null or char_length(primary_goal) between 2 and 500),
  add constraint profiles_business_model_check
    check (
      business_model is null
      or (
        business_category = 'ecommerce'
        and business_model in ('b2b', 'd2c', 'dropshipping')
      )
      or (
        business_category = 'technology_based'
        and business_model in ('b2b', 'b2c')
      )
    ),
  add constraint profiles_target_audience_check
    check (target_audience <@ array[
      'individual_consumers', 'small_businesses', 'startups', 'enterprises',
      'students', 'professionals', 'government', 'nonprofits'
    ]::text[]),
  add constraint profiles_available_resources_check
    check (available_resources <@ array[
      'laptop_computer', 'internet', 'workspace', 'equipment', 'inventory',
      'supplier_network', 'transport', 'team', 'other'
    ]::text[]),
  add constraint profiles_resource_info_check
    check (resource_info <@ array[
      'personal_savings', 'family_support', 'bank_loan', 'investor_funding',
      'grant', 'incubator_support', 'other'
    ]::text[]);
