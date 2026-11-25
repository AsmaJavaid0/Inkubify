-- 0003_skills.sql
-- Phase 1: Skills catalog and profile_skills join table

create table public.skills (
  id         smallint generated always as identity primary key,
  slug       text not null unique,
  name       text not null,
  category   text not null,
  sort_order smallint not null default 0,
  is_active  boolean not null default true
);

create table public.profile_skills (
  profile_id  uuid not null references public.profiles(id) on delete cascade,
  skill_id    smallint not null references public.skills(id),
  proficiency public.proficiency_t not null,
  created_at  timestamptz not null default now(),
  primary key (profile_id, skill_id)
);

create index profile_skills_skill_idx on public.profile_skills (skill_id);
