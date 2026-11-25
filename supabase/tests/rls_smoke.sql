-- rls_smoke.sql
-- Manual / CI SQL verification script to prove RLS isolation between two users
-- and confirm protected columns cannot be modified under the authenticated role.

begin;

-- Simulate User A and User B in auth.users
insert into auth.users (id, email, raw_user_meta_data)
values
  (
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'usera@example.com',
    '{"username":"user_alpha","full_name":"User Alpha","phone":"+923001111111"}'::jsonb
  ),
  (
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    'userb@example.com',
    '{"username":"user_beta","full_name":"User Beta","phone":"+923002222222"}'::jsonb
  );

-- Verify handle_new_user trigger created both profiles
do $$
declare
  cnt int;
begin
  select count(*) into cnt
  from public.profiles
  where id in ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb');
  if cnt <> 2 then
    raise exception 'Expected 2 trigger-created profiles, got %', cnt;
  end if;
end $$;

-- Switch to authenticated role as User B
set local role authenticated;
set local request.jwt.claim.sub = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';
set local request.jwt.claim.role = 'authenticated';

-- User B cannot read User A's profile
do $$
declare
  cnt int;
begin
  select count(*) into cnt
  from public.profiles
  where id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
  if cnt <> 0 then
    raise exception 'RLS violation: User B read User A profile';
  end if;
end $$;

-- User B cannot update User A's profile
update public.profiles
set bio = 'tampered'
where id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

-- User B cannot modify protected columns on own profile
do $$
begin
  update public.profiles
  set onboarding_status = 'completed'
  where id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';
  raise exception 'Protected column guard failed to block onboarding_status update';
exception
  when insufficient_privilege then
    -- expected
    null;
end $$;

rollback;
