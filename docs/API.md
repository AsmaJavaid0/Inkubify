# API Contract — Inkubify Phase 1 (`/api/v1`)

_Last updated: 2026-11-25 (Seeded from Spec §9)_

## Common Conventions
- Base prefix: `/api/v1`
- Auth: `Authorization: Bearer <supabase_access_token>` required on all endpoints except `GET /health` and `GET /usernames/availability`.
- Error shape:
```json
{
  "error": {
    "code": "validation_error",
    "message": "Human-readable summary",
    "fields": { "city": "Required" }
  }
}
```
Error codes: `unauthorized` (401), `forbidden` (403), `not_found` (404), `validation_error` (422), `conflict` (409), `rate_limited` (429), `server_error` (500).

## Endpoints

### `GET /api/v1/health`
- **Auth:** None
- **Response 200:** `{ "status": "ok", "version": "0.1.0" }`

### `GET /api/v1/usernames/availability?username=<value>`
- **Auth:** None (Rate-limited: `20/minute` per IP)
- **Validation:** Matches `^[a-z][a-z0-9_]{2,19}$` (lowercased) and not in reserved words list.
- **Response 200:** `{ "available": true | false }`
- **Errors:** `422` invalid format, `429` rate limit exceeded.

### `GET /api/v1/catalog/skills`
- **Auth:** Bearer JWT
- **Response 200:** `[ { "id": 1, "slug": "digital-marketing", "name": "Digital Marketing", "category": "Marketing & Sales" }, ... ]`

### `GET /api/v1/profiles/me`
- **Auth:** Bearer JWT
- **Response 200:** Full profile object including `email`, `skills[]`, `onboarding: { status, step, completed_at }`, and `profile_completion`.

### `PATCH /api/v1/profiles/me`
- **Auth:** Bearer JWT
- **Body:** Partial editable profile fields (`extra="forbid"`). Editable: `full_name`, `avatar_url`, `date_of_birth`, `gender`, `province`, `city`, `bio`, `preferred_language`, `education_level`, `field_of_study`, `occupation_status`, `work_experience`, `prior_business`, `primary_goal`, `weekly_hours`, `interested_in`, `instagram_url`, `linkedin_url`, `onboarding_step`.
- **Behaviour:** Validates fields, advances `onboarding_step` (forward-or-same only, 1–5), sets `onboarding_status = 'in_progress'` (if not already `completed`), recalculates `profile_completion`.
- **Response 200:** Updated `GET /profiles/me` payload.

### `PUT /api/v1/profiles/me/skills`
- **Auth:** Bearer JWT
- **Body:** `{ "skills": [ { "skill_id": 1, "proficiency": "intermediate" } ] }` (1–10 unique items).
- **Response 200:** Updated `GET /profiles/me` payload.

### `POST /api/v1/profiles/me/onboarding/complete`
- **Auth:** Bearer JWT
- **Behaviour:** Re-validates all required wizard fields and minimum 1 skill. Sets `onboarding_status = 'completed'`, `onboarding_completed_at = now()`, `onboarding_step = 5`, recalculates `profile_completion`.
- **Response 200:** Updated `GET /profiles/me` payload.
- **Errors:** `422` with `fields` map if any required step field or skill is missing.
