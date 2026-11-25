# Inkubify

> **Ideas → Plans → Reality**  
> A Pakistan-only web platform helping new founders go from idea to a running business.

## Repository Structure

```
inkubify/
├── apps/
│   ├── web/        # Nuxt 3 frontend (port 3000)
│   └── api/        # FastAPI backend (port 8000)
├── supabase/       # Postgres migrations, seed, config, email templates
└── docs/           # Living documentation (PROGRESS, ARCHITECTURE, API, DATABASE, DECISIONS)
```

## Prerequisites

- **Node.js** 20+ (with `npm` or `pnpm`)
- **Python** 3.11+ (with `uv` or `pip` + `venv`)
- **Supabase** project (hosted or local via [Supabase CLI](https://supabase.com/docs/guides/cli) + Docker)

## Quick Start

### 1. Environment Variables

Copy the example environment files and fill in your Supabase credentials:

```bash
cp apps/web/.env.example apps/web/.env
cp apps/api/.env.example apps/api/.env
```

> **Note:** Never commit `.env` files or expose `SUPABASE_SERVICE_ROLE_KEY` to the browser.

### 2. Database (Supabase)

**Using Supabase CLI (local or linked hosted project):**

```bash
# Local development (requires Docker)
supabase start
supabase db reset   # Applies supabase/migrations/* and supabase/seed.sql

# Or link to your hosted Supabase project and push migrations
supabase link --project-ref <project-ref>
supabase db push
```

If applying manually via the Supabase SQL Editor, run `supabase/migrations/0001_extensions_and_enums.sql` through `0006_storage_avatars.sql` in order, followed by `supabase/seed.sql`.

Ensure **Confirm email** is enabled in Supabase Auth settings (Authentication → Providers → Email), and configure Site URL / Redirect URLs to include `http://localhost:3000/auth/confirm` and `http://localhost:3000/reset-password`.

### 3. Backend API (`apps/api`)

```bash
cd apps/api
uv venv
# Activate venv (Windows PowerShell: .venv\Scripts\Activate.ps1 | Unix: source .venv/bin/activate)
uv pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

Run backend tests & linter:

```bash
pytest
ruff check .
```

### 4. Frontend Web App (`apps/web`)

```bash
cd apps/web
npm install   # or: pnpm install
npm run dev   # http://localhost:3000
```

Run frontend checks & tests:

```bash
npm run typecheck
npm run lint
npm run test:unit
```

## Documentation

Read `AGENTS.md` and `docs/PROGRESS.md` at the start of every development session.
