-- 0002_profiles.sql
-- Phase 1: Founder profiles table, constraints, indexes, updated_at trigger

create table public.profiles (
  id                      uuid primary key references auth.users(id) on delete cascade,
  username                citext not null unique
                            check (username::text ~ '^[a-z][a-z0-9_]{2,19}$'),
  full_name               text   not null check (char_length(full_name) between 2 and 60),
  phone_e164              text   not null unique check (phone_e164 ~ '^\+923\d{9}$'),
  country_code            char(2) not null default 'PK' check (country_code = 'PK'),

  -- Step 1: personal
  avatar_url              text,
  date_of_birth           date check (date_of_birth between date '1930-01-01' and current_date),
  gender                  public.gender_t,
  province                text,
  city                    text,
  bio                     text check (bio is null or char_length(bio) <= 280),
  preferred_language      public.language_t not null default 'en',

  -- Step 2: background
  education_level         public.education_t,
  field_of_study          text check (field_of_study is null or char_length(field_of_study) between 2 and 80),
  occupation_status       public.occupation_t,
  work_experience         public.work_experience_t,
  prior_business          public.prior_business_t,

  -- Step 4: goals & availability
  primary_goal            public.primary_goal_t,
  weekly_hours            public.weekly_hours_t,
  interested_in           text[] not null default '{}'
                            check (interested_in <@ array['ecommerce', 'tech_services']),
  instagram_url           text,
  linkedin_url            text,

  -- Onboarding state
  onboarding_status       public.onboarding_status_t not null default 'not_started',
  onboarding_step         smallint not null default 1 check (onboarding_step between 1 and 5),
  profile_completion      smallint not null default 0 check (profile_completion between 0 and 100),
  onboarding_completed_at timestamptz,

  created_at              timestamptz not null default now(),
  updated_at              timestamptz not null default now()
);

create index profiles_city_idx on public.profiles (province, city);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_set_updated_at
  before update on public.profiles
  for each row
  execute function public.set_updated_at();
