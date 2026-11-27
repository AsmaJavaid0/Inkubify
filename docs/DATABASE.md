# Database Schema — Inkubify Phase 1

_Last updated: 2026-11-27_

## Migrations

| Version | File | Description |
|---|---|---|
| 0001 | `0001_extensions_and_enums.sql` | Extensions and shared domain enums |
| 0002 | `0002_profiles.sql` | Canonical `public.profiles` table and update trigger |
| 0003 | `0003_skills.sql` | `public.skills` catalog and `public.profile_skills` junction |
| 0004 | `0004_rls_policies.sql` | Owner-only RLS and protected-column guards |
| 0005 | `0005_new_user_trigger.sql` | Create profile after Supabase Auth sign-up |
| 0006 | `0006_storage_avatars.sql` | Avatar storage bucket and RLS |
| 0007 | `0007_founder_profile_expansion.sql` | Personal address, expertise, business interests, and financial/resource fields; replaces superseded profile fields |

Seed file: `supabase/seed.sql` (22 technical skills across 4 categories).

## Profile data design
- `profiles` remains the single canonical founder-profile table; no duplicate profile table is introduced.
- Auth-managed email and password remain in Supabase Auth. Username, name, phone, and country code are established during sign-up; username and phone are not editable from the profile screen.
- Age is calculated from `date_of_birth`; it is not stored separately.
- Province and city provide the Pakistan location. Country is fixed to `PK` for Phase 1.
- Technical skills use `skills` + `profile_skills`; custom skills and experience metadata are stored on `profiles`.
- Business category/model constraints enforce E-commerce (B2B, D2C, Dropshipping) and Technology-based (B2B, B2C).
- Migration 0007 preserves old primary-goal text, maps previous interest to the new single category, and converts the old work-experience and weekly-hours values to approximate years and availability.
- Available resources and funding/support sources are stored as validated text arrays.

## Regenerating TypeScript types
```bash
npx supabase gen types typescript --project-id <project-id> > apps/web/types/database.types.ts
```
