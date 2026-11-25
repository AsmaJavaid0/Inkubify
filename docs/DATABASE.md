# Database Schema — Inkubify Phase 1

_Last updated: 2026-11-25 (Seeded from Spec §8)_

## Migrations

| Version | File | Description |
|---|---|---|
| 0001 | `supabase/migrations/0001_extensions_and_enums.sql` | `citext` extension and 10 domain enums |
| 0002 | `supabase/migrations/0002_profiles.sql` | `public.profiles` table, constraints, `updated_at` trigger |
| 0003 | `supabase/migrations/0003_skills.sql` | `public.skills` and `public.profile_skills` tables |
| 0004 | `supabase/migrations/0004_rls_policies.sql` | RLS policies + protected-column guard & server RPCs |
| 0005 | `supabase/migrations/0005_new_user_trigger.sql` | `handle_new_user()` trigger on `auth.users` |
| 0006 | `supabase/migrations/0006_storage_avatars.sql` | `avatars` bucket and storage RLS policies |

Seed file: `supabase/seed.sql` (22 skills across 4 categories).

## Regenerating TypeScript Types
```bash
npx supabase gen types typescript --project-id <project-id> > apps/web/types/database.types.ts
```
(Or `--local` when using local Supabase CLI.)
