# Architecture — Inkubify Phase 1

_Last updated: 2026-11-27_

## 1. System Overview

Inkubify is a Pakistan-only founder roadmap platform. Phase 1 covers splash/welcome screens, email+password sign-up with verification, username login/password-reset, and a multi-step founder profile wizard.

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
- `supabase/` — SQL migrations (`0001`–`0007`), skills catalog `seed.sql`, `config.toml`, email templates.
- `docs/` — Living project documentation (`PROGRESS.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `API.md`, `DATABASE.md`, `design/`).

## 3. Auth Flow

1. Sign-up, email verification, password reset, and password updates use Supabase Auth.
2. Login accepts username + password. FastAPI privately resolves the username to its Auth user, then verifies the password through Supabase Auth and returns session tokens. No public username-to-email lookup is exposed.
3. On `signUp`, user metadata (`username`, `full_name`, `phone`, `country_code: 'PK'`) triggers Postgres `handle_new_user()` to insert into `public.profiles`.
4. Email confirmation sends the user to `/auth/confirm` which completes PKCE/OTP verification and triggers route guard redirection.
5. For API requests, `useApi.ts` attaches `Authorization: Bearer <access_token>`, refreshing once on `401`.
6. FastAPI verifies the JWT (JWKS or HS256), validates `exp`, `aud == "authenticated"`, and `iss`, and scopes Supabase DB calls to the user's JWT so RLS remains active.

## 4. Profile Wizard Data Flow

- On entering `/onboarding/profile`, the profile store loads `GET /api/v1/profiles/me` and `catalog/skills`.
- The wizard contains Personal Information, Education & Background, Skills & Expertise, Business & Resources, and Review & Finish.
- Each step saves through `PATCH /api/v1/profiles/me`; catalog skills use `PUT /api/v1/profiles/me/skills`.
- Avatar upload remains in Supabase Storage (`avatars/{user_id}/avatar.<ext>`).
- Finish calls `POST /api/v1/profiles/me/onboarding/complete`, which re-validates required fields server-side.

### Profile completion calculation (`services/completion.py`)
- Personal information: 25 points (date of birth, province, city, preferred language).
- Education/background: 15 points (education, occupation, prior business experience).
- Skills/expertise: 20 points (catalog or custom skills, experience level, availability).
- Business interests: 40 points (business category, compatible model, primary goal, expected timeline).
- Financial/resource details, target audience, address, bio, and external links are optional and do not block completion.
- Age is calculated from date of birth; it is not stored separately.

## 5. Design Tokens and Component Inventory

- Brand tokens: `navy-900` (`#142535`), `navy-700` (`#23384B`), `snow-100` (`#F7F7F7`), `gold-500` (`#C19829`).
- Functional tokens: `danger`, `success`, `warning`.
- Brand component: `components/brand/AppLogo.vue` (`sm | md | lg | splash`).
- UI Kit (`components/ui/`): `BaseButton`, `BaseInput`, `BasePasswordInput`, `BasePhoneInput`, `BaseSelect`, `BaseTextarea`, `BaseCheckbox`, `BaseChipSelect`, `BaseStepper`, `BaseAvatarUpload`, `BaseToast`, `FormField`, `SearchableMultiSelect`.

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

- Phase 1 captures founder information, skills, business interests, and available resources. A separate business profile (`/business/*`) remains reserved for Phase 2.
- `apps/web/public/brand/logo.png` is pending owner upload (`AppLogo.vue` renders a brand-compliant SVG fallback until `logo.png` is added).
- Hosted Supabase project (`auzcprvfomcolgrshzba`) requires applying `supabase/migrations/0001`–`0007` + `supabase/seed.sql` and setting `SUPABASE_SERVICE_ROLE_KEY` in `apps/api/.env` for live username checks and profile writes.
- Email confirmation & SMTP rely on Supabase project settings.
