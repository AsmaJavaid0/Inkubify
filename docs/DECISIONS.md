# Decisions Log — Inkubify

## D-000 — Fixed Technology Stack
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Phase 1 specification fixes the stack across frontend, backend, and database.
- Decision: Nuxt 3 (Vue 3, TypeScript strict, Tailwind CSS, Pinia, VeeValidate + Zod, `@nuxtjs/supabase`), FastAPI (Python 3.11+, Pydantic v2, Uvicorn, `slowapi`, PyJWT), and Supabase (Postgres, Auth, Storage, RLS).
- Consequences: Do not introduce competing frameworks or ORMs without a formal `PROPOSED` ADR.

## D-001 — Country Locked to Pakistan (PK)
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Inkubify is a Pakistan-only founder roadmap platform in Phase 1.
- Decision: `country_code` is fixed to `'PK'` at sign-up, in the DB constraint, and in profile payloads. Phone numbers accept Pakistani mobile formats and normalize to E.164 (`+923XXXXXXXXX`).
- Consequences: Multi-country expansion later requires a schema migration and phone validation generalization.

## D-002 — Server-Authoritative Validation
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Client-side validation provides immediate UX feedback, while data integrity and security require server enforcement.
- Decision: FastAPI Pydantic schemas enforce all rules (age ≥ 18, province/city pairing, URL formats, bio length, enums, `extra="forbid"`). Client Zod schemas mirror these rules for UX only.
- Consequences: Validation rules exist in both `apps/web/schemas` and `apps/api/app/schemas` and must stay aligned.

## D-003 — Profile Creation via Postgres Trigger
- Date: 2026-11-25
- Status: ACCEPTED
- Context: A user signing up through Supabase Auth must atomically receive a `public.profiles` row without client-side insert race conditions.
- Decision: `handle_new_user()` trigger (`SECURITY DEFINER`) inserts into `public.profiles` from `auth.users.raw_user_meta_data`. No direct client `INSERT` RLS policy exists on `profiles`.
- Consequences: Uniqueness violations on `username` or `phone_e164` abort sign-up with a database error mapped to a friendly UI message.

## D-004 — Minimum Age 18+ Assumption
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Business registration in Pakistan generally requires legal adulthood; spec §15 leaves this as an initial assumption.
- Decision: Require founders to be at least 18 years old based on `date_of_birth`, not in the future, and not before `1930-01-01`.
- Consequences: Owner can lower this threshold later by updating the API/Zod validators.

## D-005 — Avatars Storage Bucket Public Read
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Spec §8.6 allows either public read or private signed URLs for the `avatars` bucket.
- Decision: Configure `avatars` as a public-read bucket with authenticated owner-only write/update/delete RLS policies scoped to `{auth.uid()}/...`, 2 MB file size limit, and `image/jpeg`, `image/png`, `image/webp` MIME restrictions.
- Consequences: Avatar URLs are straightforward to render without signed-URL expiry; assumes avatars are non-sensitive.

## D-006 — Protected Profile Columns Enforcement
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Spec §8.4 requires preventing clients from directly modifying `username`, `phone_e164`, `country_code`, `onboarding_status`, `onboarding_completed_at`, and `profile_completion` via Supabase PostgREST directly.
- Decision: Use a `BEFORE UPDATE` trigger (`protect_profile_immutable_and_server_fields()`) that checks a transaction-local GUC (`app.bypass_profile_guard`) or `current_user` / role (`service_role` / `postgres`), rejecting or reverting client-side changes to protected columns from `authenticated` direct updates, while FastAPI uses `extra="forbid"` and either a trusted RPC (`security definer`) or `service_role` only after verifying the user's JWT and enforcing RLS on reads/normal writes. Wait: to keep RLS in force on FastAPI writes while allowing FastAPI to update `onboarding_status`, `onboarding_completed_at`, and `profile_completion`, FastAPI calls a `SECURITY DEFINER` Postgres RPC or sets a signed/validated path — specifically, `SECURITY DEFINER` RPCs (`api_update_profile_progress`, `api_complete_onboarding`) scoped to `auth.uid()`.
- Consequences: Direct browser Supabase client `UPDATE` calls cannot tamper with `username`, `phone_e164`, `country_code`, `onboarding_status`, `onboarding_completed_at`, or `profile_completion`, while FastAPI calls remain user-JWT scoped with RLS active.

## D-007 — JWT Verification via JWKS with HS256 Fallback
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Modern Supabase projects sign JWTs asymmetrically (ES256/RS256 via JWKS), while local/legacy setups may use HS256 with `SUPABASE_JWT_SECRET`.
- Decision: FastAPI checks the token header algorithm and verifies asymmetric tokens against `SUPABASE_JWKS_URL` (cached `PyJWKClient`), falling back to HS256 with `SUPABASE_JWT_SECRET` when configured for HS256. Always validates `exp`, `aud == "authenticated"`, and `iss`.
- Consequences: Works seamlessly against both hosted Supabase (publishable key + JWKS) and local/unit-test environments.

## D-008 — Brand Favicon Generation
- Date: 2026-11-25
- Status: ACCEPTED
- Context: Spec §4.3 specifies deriving a favicon from the bulb/arrow area of the logo and recording how in `DECISIONS.md`; owner has not yet supplied `logo.png`.
- Decision: Provide a clean SVG favicon (`apps/web/public/brand/favicon.svg`) and PNG icon depicting the navy cube / glowing gold bulb+arrow motif using strictly the brand palette (`#142535`, `#23384B`, `#F7F7F7`, `#C19829`), and wire `AppLogo.vue` to render `/brand/logo.png` (or a clean brand panel fallback if the file is absent/pending owner export).
- Consequences: Once the owner places their `logo.png` in `apps/web/public/brand/logo.png`, `AppLogo.vue` displays it immediately without code changes.
