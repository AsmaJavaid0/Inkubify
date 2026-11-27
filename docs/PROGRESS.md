# Progress — Inkubify Phase 1 (Sign-up & Founder Profile)

_Last updated: 2026-11-27_

## Current status
**Phase:** 1 — Sign-up, authentication, and founder profile  
**Current milestone:** Profile expansion and username-login implementation  
**Repository:** `AsmaJavaid0/Inkubify`, changes committed directly to `main`  
**Database status:** Migration `0007_founder_profile_expansion.sql` has been added but has not been applied to the hosted Supabase project.  
**Verification status:** Automated tests, typecheck, lint, and build have not been run after the 2026-11-27 changes. Live Supabase login and profile persistence still require verification.

## Completed in this session
- [x] Expanded the existing founder profile; retained the canonical `profiles` table and existing skill catalog/junction.
- [x] Added address and profile contact display; age is derived from date of birth.
- [x] Added custom skills, overall experience level, numeric years, portfolio, LinkedIn, GitHub, and availability.
- [x] Added E-commerce and Technology-based categories with category-specific business models.
- [x] Added target audience, free-text primary goal, and expected business timeline.
- [x] Added available budget, available resources, team-member count, and funding/resource information.
- [x] Added searchable multi-select controls for target audience and resource/funding options.
- [x] Added migration `0007_founder_profile_expansion.sql`; existing applied migrations were not edited.
- [x] Changed login UI and API to accept username + password. Username resolution stays server-side and does not expose the account email.
- [x] Updated API schemas, profile completion validation, frontend types, tests, and project documentation.

## Remaining work
1. Apply migrations `0001`–`0007` and `supabase/seed.sql` to the hosted Supabase project; run `supabase/tests/rls_smoke.sql`.
2. Confirm `SUPABASE_SERVICE_ROLE_KEY` is configured only in the FastAPI environment; never expose it to the browser or commit it.
3. Run backend `pytest -v` and `ruff check .`.
4. Run frontend `npm run typecheck`, `npm run lint`, `npm run test:unit`, and `npm run build`.
5. Run end-to-end sign-up, email verification, username login, profile save/reload, and onboarding completion against the hosted/local Supabase database.
6. Review UI responsiveness and accessibility for the expanded profile forms.

## Scope notes
- Phase 1 business categories remain E-commerce and Technology-based only.
- E-commerce models: B2B, D2C, Dropshipping.
- Technology-based models: B2B, B2C.
- No Team Status field is included.
- A separate business profile, roadmap generation, milestones, reminders, payments, and social login remain outside this Phase 1 change.

## Session log
### 2026-11-27 — Founder profile and username login
- Added the expanded profile fields to the existing database/API/frontend architecture.
- Added server-side username login while retaining Supabase Auth as the credential and session authority.
- Added migration 0007 and updated profile/API/database documentation.
- Tests and build checks are pending; the repository connector did not provide a local execution environment for running them.
