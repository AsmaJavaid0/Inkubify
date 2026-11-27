-- 0007_founder_profile_expansion.sql
-- Extend the existing founder profile; this is not a separate business profile.
-- Preserve useful values from the fields replaced by this migration.

alter table public.profiles
  alter column primary_goal type text using primary_goal::text;

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

-- Preserve the previous primary-goal meaning as readable text.
update public.profiles
set primary_goal = case primary_goal
  when 'side_income' then 'Build a side income'
  when 'full_time_business' then 'Launch a full-time business'
  when 'scale_existing' then 'Scale an existing business'
  when 'explore_learn' then 'Explore and learn about starting a business'
  else primary_goal
end;

-- Convert the old multi-select category into the new single main category.
-- If both were selected, E-commerce takes precedence; the founder can edit it later.
update public.profiles
set business_category = case
  when 'ecommerce' = any(interested_in) then 'ecommerce'
  when 'tech_services' = any(interested_in) then 'technology_based'
  else null
end;

-- Preserve the previous experience range as an approximate numeric year value.
update public.profiles
set experience_years = case work_experience::text
  when 'none' then 0
  when 'lt_1' then 0
  when '1_3' then 2
  when '3_5' then 4
  when '5_plus' then 5
  else null
end
where work_experience is not null;

-- Convert weekly time commitment into the new availability choices.
update public.profiles
set availability = case weekly_hours::text
  when 'lt_5' then 'evenings_weekends'
  when '5_10' then 'evenings_weekends'
  when '10_20' then 'part_time'
  when '20_40' then 'part_time'
  when '40_plus' then 'full_time'
  else null
end
where weekly_hours is not null;

alter table public.profiles
  drop column work_experience,
  drop column weekly_hours,
  drop column interested_in,
  drop column instagram_url;

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
