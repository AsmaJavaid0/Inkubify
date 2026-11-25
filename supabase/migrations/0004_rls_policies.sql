-- 0004_rls_policies.sql
-- Phase 1: Row Level Security and protected-column guards

alter table public.profiles       enable row level security;
alter table public.profile_skills enable row level security;
alter table public.skills         enable row level security;

-- profiles: owner only (no insert policy: trigger creates rows; no delete policy in Phase 1)
create policy "profiles_select_own"
  on public.profiles for select
  using (auth.uid() = id);

create policy "profiles_update_own"
  on public.profiles for update
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- profile_skills: owner only
create policy "ps_select_own"
  on public.profile_skills for select
  using (auth.uid() = profile_id);

create policy "ps_insert_own"
  on public.profile_skills for insert
  with check (auth.uid() = profile_id);

create policy "ps_update_own"
  on public.profile_skills for update
  using (auth.uid() = profile_id)
  with check (auth.uid() = profile_id);

create policy "ps_delete_own"
  on public.profile_skills for delete
  using (auth.uid() = profile_id);

-- skills: readable by any authenticated user; writes via migrations/service_role only
create policy "skills_read_auth"
  on public.skills for select
  to authenticated
  using (is_active);

-- Prevent direct client edits to immutable and server-computed profile columns.
-- Only service_role (or postgres) may modify these columns.
create or replace function public.protect_profile_columns()
returns trigger
language plpgsql
as $$
declare
  jwt_role text;
begin
  jwt_role := coalesce(current_setting('request.jwt.claim.role', true), '');

  if current_user in ('authenticated', 'anon') or jwt_role in ('authenticated', 'anon') then
    if new.id is distinct from old.id
      or new.username is distinct from old.username
      or new.phone_e164 is distinct from old.phone_e164
      or new.country_code is distinct from old.country_code
      or new.onboarding_status is distinct from old.onboarding_status
      or new.onboarding_completed_at is distinct from old.onboarding_completed_at
      or new.profile_completion is distinct from old.profile_completion
    then
      raise exception 'Cannot modify protected profile columns directly'
        using errcode = '42501';
    end if;
  end if;

  return new;
end;
$$;

create trigger profiles_protect_columns
  before update on public.profiles
  for each row
  execute function public.protect_profile_columns();
