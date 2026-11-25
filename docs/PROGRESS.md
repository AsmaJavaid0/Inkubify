# Progress — Inkubify Phase 1 (Sign-up & User Profile)

_Last updated: 2026-11-25 by Antigravity_

## Current status
**Phase:** 1 — Sign-up & user profile
**Current milestone:** M1 / M4–M8 live Supabase verification
**App runs locally:** yes (`apps/web` builds and serves HTTP 200; `apps/api` serves `/api/v1/health` HTTP 200)
**Blockers:** Local Docker is unavailable and `SUPABASE_SERVICE_ROLE_KEY` / Supabase DB access were not provided, so `supabase/migrations/0001`–`0006` + `supabase/seed.sql` are not yet applied to the hosted Supabase project (`auzcprvfomcolgrshzba`) and live E2E signup/wizard tests could not be executed against Postgres yet.

## Milestone checklist
- [x] M0 Repo bootstrap
- [ ] M1 Database (SQL migrations `0001`–`0006`, `seed.sql`, `rls_smoke.sql` written; awaiting `supabase db push` / SQL Editor execution & live RLS verification)
- [x] M2 Design system
- [x] M3 API core (15/15 `pytest` tests and `ruff` pass using mocked Supabase client)
- [ ] M4 Splash, welcome, auth pages (implemented, type-checked, linted, built; awaiting live Supabase Auth E2E run)
- [ ] M5 Profile wizard (implemented, type-checked, linted, built; awaiting live DB/Storage E2E run)
- [ ] M6 Profile edit + dashboard (implemented, type-checked, linted, built; awaiting live DB E2E run)
- [ ] M7 Hardening (security headers, CORS, 1 MB limit, rate limiting, a11y attributes, unit tests in place; awaiting Lighthouse >= 90 audit & live RLS check)
- [ ] M8 Tests & docs (15 API tests + 10 web unit tests pass; Playwright E2E spec written at `apps/web/tests/e2e/onboarding.spec.ts`, awaiting live server + Supabase run)

## Next steps (ordered, concrete)
1. Apply `supabase/migrations/0001_extensions_and_enums.sql` through `0006_storage_avatars.sql` and `supabase/seed.sql` to the Supabase project (`auzcprvfomcolgrshzba`), then run `supabase/tests/rls_smoke.sql` to verify RLS isolation and mark M1 complete.
2. Add `SUPABASE_SERVICE_ROLE_KEY` to `apps/api/.env` (never commit `.env`), and ensure Supabase Auth Redirect URLs include `http://localhost:3000/auth/confirm` and `http://localhost:3000/reset-password`.
3. Drop the official Inkubify logo PNG at `apps/web/public/brand/logo.png` (currently `AppLogo.vue` renders a brand-compliant SVG fallback).
4. Start both servers (`uvicorn app.main:app --reload --port 8000` in `apps/api`, `npm run dev` in `apps/web`), run Playwright E2E (`npm run test:e2e`) and Lighthouse accessibility audit, and tick M4–M8.
5. Prepare Phase 2: Business Profile (`/business/*`).

## Open questions for the owner
- Supply `apps/web/public/brand/logo.png` (and optional transparent/SVG export).
- Confirm minimum age (18+ assumed per `D-004`) and compare Phase 1 profile fields against owner's list.
- Choose production SMTP provider before launch.

## Parking lot (ideas out of scope)
- Business profile (`/business/*`) — Phase 2
- Roadmap generation, milestones, reminders, market trends
- Urdu UI translations (only `preferred_language` stored in Phase 1)

## Session log (newest first)
### 2026-11-25 — Session 1
- Done: Cloned `AsmaJavaid0/Inkubify`, bootstrapped `AGENTS.md`, `CLAUDE.md`, `docs/*`, `.gitignore`, `.editorconfig`, `.env.example`s, `README.md`. Authored all Supabase migrations (`0001`–`0006`), `seed.sql`, `config.toml`, email templates, and `rls_smoke.sql`. Built FastAPI backend (`apps/api`) with JWKS/HS256 JWT verification, rate-limited `/usernames/availability`, `/catalog/skills`, `/profiles/me` GET/PATCH/PUT skills/POST complete, completion scoring, and 15 pytest tests. Built Nuxt 3 frontend (`apps/web`) with strict brand tokens, `AppLogo.vue`, 12 `ui/*` components, `/_kit`, route guard, splash/welcome/auth flows, 4-step + review profile wizard, avatar upload, `/profile`, `/dashboard`, security headers middleware, 10 Vitest unit tests, and Playwright smoke spec. Populated gitignored local `.env` files with provided `SUPABASE_URL` and publishable key (`SUPABASE_SERVICE_ROLE_KEY` left blank).
- Files created/changed: `AGENTS.md`, `CLAUDE.md`, `README.md`, `.gitignore`, `.editorconfig`, `.env.example`, `docs/*`, `supabase/*`, `apps/api/*`, `apps/web/*`.
- Tests run / result:
  - `apps/api`: `pytest -v` -> 15 passed; `ruff check .` -> 0 errors.
  - `apps/web`: `npm run test:unit` -> 10 passed; `npm run typecheck` -> 0 errors; `npm run lint` -> 0 errors; `npm run build` -> succeeded.
  - Live server smoke check: `uvicorn` `/api/v1/health` -> 200 `{"status":"ok","version":"0.1.0"}`; built Nitro server `/welcome` -> 200 with `X-Frame-Options: DENY`.
- Next: Apply Supabase migrations + seed, add `SUPABASE_SERVICE_ROLE_KEY` to `apps/api/.env`, run live E2E & Lighthouse checks, and drop in `logo.png`.
- Notes/risks: `apps/api/.env` and `apps/web/.env` exist locally (gitignored). Do not commit `.env`. Hosted Supabase JWKS verified live (`ES256`) and `mailer_autoconfirm` verified `false` (email confirmation enabled).
