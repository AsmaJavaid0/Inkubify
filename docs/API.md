# API Contract — Inkubify Phase 1 (`/api/v1`)

_Last updated: 2026-11-27_

## Common conventions
- Base prefix: `/api/v1`.
- Protected endpoints use `Authorization: Bearer <supabase_access_token>`.
- Error response: `{ "error": { "code": "...", "message": "...", "fields": {} } }`.
- Validation is authoritative in FastAPI; frontend Zod validation provides immediate feedback.

## Endpoints

### `POST /api/v1/auth/login`
- Auth: None; rate-limited to 5 attempts/minute per IP.
- Body: `{ "username": "founder_name", "password": "..." }`.
- Behaviour: resolves the username privately on the server, then verifies the password through Supabase Auth. The API does not return the account email or expose a username-to-email lookup endpoint.
- Response: Supabase `access_token`, `refresh_token`, `token_type`, and `expires_in`.
- Errors: 401 invalid username/password; 403 email not verified; 422 invalid username format; 429 rate limit exceeded.

### `GET /api/v1/health`
- Auth: None.
- Response: `{ "status": "ok", "version": "0.1.0" }`.

### `GET /api/v1/usernames/availability?username=<value>`
- Auth: None; rate-limited to 20/minute.
- Response: `{ "available": true | false }`.

### `GET /api/v1/catalog/skills`
- Auth: Bearer JWT.
- Response: active skill catalog items.

### `GET /api/v1/profiles/me`
- Auth: Bearer JWT.
- Response: founder profile, contact details, selected technical skills, business interests, financial/resource information, onboarding state, and completion percentage.

### `PATCH /api/v1/profiles/me`
- Auth: Bearer JWT.
- Body: partial editable founder-profile fields; unknown fields are rejected.
- Personal: `full_name`, `avatar_url`, `date_of_birth`, `gender`, `address`, `province`, `city`, `bio`, `preferred_language`.
- Education/background: `education_level`, `field_of_study`, `occupation_status`, `prior_business`.
- Skills/expertise: `other_skills`, `experience_level`, `experience_years`, `portfolio_url`, `linkedin_url`, `github_url`, `availability`.
- Business interests: `business_category`, `business_model`, `target_audience`, free-text `primary_goal`, `expected_business_timeline`.
- Financial/resources: `available_budget_pkr`, `available_resources`, `team_members`, `resource_info`.
- Business category is restricted to E-commerce or Technology-based. E-commerce models: B2B, D2C, Dropshipping. Technology-based models: B2B, B2C.
- Age is derived from `date_of_birth`; it is not stored as a duplicate field. Country is fixed to Pakistan in Phase 1.
- Response: updated full profile.

### `PUT /api/v1/profiles/me/skills`
- Auth: Bearer JWT.
- Body: `{ "skills": [{ "skill_id": 1, "proficiency": "intermediate" }] }`.
- Accepts 0–10 catalog skills so a founder may use only the custom `other_skills` field.

### `POST /api/v1/profiles/me/onboarding/complete`
- Auth: Bearer JWT.
- Re-validates required personal, background, expertise, and business-interest fields server-side, then marks onboarding completed.
- Financial/resource information and external profile links are optional.
