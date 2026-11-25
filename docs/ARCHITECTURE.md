# Architecture — Inkubify Phase 1

_Last updated: 2026-11-25 (Initial seed from Phase 1 Spec)_

## 1. System Overview

Inkubify is a Pakistan-only founder roadmap platform. Phase 1 covers splash/welcome screens, email+password sign-up with verification, login/password-reset, and a multi-step founder profile wizard.

```
┌───────────────────────────┐        ┌──────────────────────────────┐
│  Nuxt 3 web app (apps/web)│        │  Supabase                    │
│                           │ Auth   │  • Auth (email+password)     │
│  pages / components /     ├───────►│  • Postgres + RLS            │
│  composables / stores     │        │  • Storage (avatars bucket)  │
│                           │        └──────────────▲───────────────┘
│                           │  REST + Bearer JWT    │ user JWT (RLS)
│                           ├──────────────────►┌───┴──────────────┐
└───────────────────────────┘                   │ FastAPI          │
                                                │ (apps/api)       │
                                                │ /api/v1/...      │
                                                └──────────────────┘
```

## 2. Folder Map

- `apps/web/` — Nuxt 3 frontend (TypeScript strict, Tailwind CSS, Pinia, VeeValidate + Zod, `@nuxtjs/supabase`).
- `apps/api/` — FastAPI backend (`/api/v1`), Pydantic v2 validation, JWT verification, profile & catalog services.
- `supabase/` — SQL migrations (`0001`–`0006`), skills catalog `seed.sql`, `config.toml`, email templates.
- `docs/` — Living project documentation (`PROGRESS.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `API.md`, `DATABASE.md`, `design/`).

## 3. Auth Flow

1. Browser talks directly to Supabase Auth via `@nuxtjs/supabase` (`signUp`, `signInWithPassword`, `resetPasswordForEmail`, `updateUser`, `signOut`).
2. On `signUp`, user metadata (`username`, `full_name`, `phone`, `country_code: 'PK'`) triggers Postgres `handle_new_user()` to insert into `public.profiles`.
3. Email confirmation sends the user to `/auth/confirm` which completes PKCE/OTP verification and triggers route guard redirection.
4. For API requests, `useApi.ts` attaches `Authorization: Bearer <access_token>`, refreshing once on `401`.
5. FastAPI verifies the JWT (JWKS or HS256), validates `exp`, `aud == "authenticated"`, and `iss`, and scopes Supabase DB calls to the user's JWT so RLS remains active.

## 4. Profile Wizard Data Flow

- On entering `/onboarding/profile`, `profile` store loads `GET /api/v1/profiles/me` and `catalog/skills`.
- `onboarding` store hydrates form drafts from server state and resumes at `onboarding.step`.
- Each step **Next** calls `PATCH /api/v1/profiles/me` (or `PUT /api/v1/profiles/me/skills` for Step 3), recalculating `profile_completion` and advancing `onboarding_step`.
- **Avatar upload** uploads directly to Supabase Storage (`avatars/{user_id}/avatar.<ext>`) and saves `avatar_url` via `PATCH /api/v1/profiles/me`.
- **Finish** on the Review step calls `POST /api/v1/profiles/me/onboarding/complete`, which re-validates all required fields server-side before marking `onboarding_status = 'completed'`.

### Completion Calculation (`services/completion.py`)
- Required step weights (25 points each, total 100 base):
  - Personal (25): `date_of_birth`, `province`, `city`, `preferred_language` (filled / 4 * 25)
  - Background (25): `education_level`, `occupation_status`, `work_experience`, `prior_business` (filled / 4 * 25)
  - Skills (25): ≥ 1 skill selected (25 if ≥ 1 else 0)
  - Goals (25): `primary_goal`, `weekly_hours` (filled / 2 * 25)
- Optional bonus (up to +10 points, capped so total ≤ 100):
  - `avatar_url` (+2.5), `bio` (+2.5), `field_of_study` (+2.5), social link (`instagram_url` or `linkedin_url`, +2.5).

## 5. Design Tokens and Component Inventory

- Brand tokens: `navy-900` (`#142535`), `navy-700` (`#23384B`), `snow-100` (`#F7F7F7`), `gold-500` (`#C19829`).
- Functional tokens: `danger`, `success`, `warning`.
- Brand component: `components/brand/AppLogo.vue` (`sm | md | lg | splash`).
- UI Kit (`components/ui/`): `BaseButton`, `BaseInput`, `BasePasswordInput`, `BasePhoneInput`, `BaseSelect`, `BaseTextarea`, `BaseCheckbox`, `BaseChipSelect`, `BaseStepper`, `BaseAvatarUpload`, `BaseToast`, `FormField`.

## 6. Route Map and Guard Rules

Handled in `apps/web/middleware/guard.global.ts`:
- Signed out: `/`, `/welcome`, `/signup`, `/login`, `/verify-email`, `/forgot-password`, `/reset-password`, `/auth/confirm`, `/terms`, `/privacy` (else `/login`).
- Signed in, email unverified: `/verify-email`, `/auth/confirm`, `/terms`, `/privacy` (else `/verify-email`).
- Signed in, onboarding incomplete: `/onboarding/profile`, `/auth/confirm`, `/reset-password`, `/terms`, `/privacy` (else `/onboarding/profile`).
- Signed in, onboarding completed: `/dashboard`, `/profile`, `/auth/confirm`, `/reset-password`, `/terms`, `/privacy` (else `/dashboard`).
- Dev-only `/_kit` allowed in `import.meta.dev` mode.

## 7. Environment and Local Development

See root `README.md` and `.env.example` files in root, `apps/web/`, and `apps/api/`.

## 8. Testing Approach

- Frontend unit tests: Vitest (`apps/web/tests/unit/`)
- Frontend E2E smoke test: Playwright (`apps/web/tests/e2e/`)
- Backend unit/API tests: Pytest (`apps/api/tests/`)
- Database RLS smoke check: `supabase/tests/rls_smoke.sql`

## 9. Known Limitations / Tech Debt

- Phase 1 covers founder profile only; business profile (`/business/*`) is reserved for Phase 2.
- `apps/web/public/brand/logo.png` is pending owner upload (`AppLogo.vue` renders a brand-compliant SVG fallback until `logo.png` is added).
- Hosted Supabase project (`auzcprvfomcolgrshzba`) requires applying `supabase/migrations/0001`–`0006` + `supabase/seed.sql` and setting `SUPABASE_SERVICE_ROLE_KEY` in `apps/api/.env` for live username checks and profile writes.
- Email confirmation & SMTP rely on Supabase project settings.
