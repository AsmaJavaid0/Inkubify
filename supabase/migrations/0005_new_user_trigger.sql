-- 0005_new_user_trigger.sql
-- Phase 1: Atomically create public.profiles row on auth.users sign-up

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, username, full_name, phone_e164, country_code)
  values (
    new.id,
    lower(trim(coalesce(new.raw_user_meta_data->>'username', ''))),
    regexp_replace(trim(coalesce(new.raw_user_meta_data->>'full_name', '')), '\s+', ' ', 'g'),
    trim(coalesce(new.raw_user_meta_data->>'phone', '')),
    'PK'
  );
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
  after insert on auth.users
  for each row
  execute function public.handle_new_user();
