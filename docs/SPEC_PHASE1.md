# Inkubify — Sign-Up & User Profile Building: Phase 1 Spec Summary

Reference copy of the Phase 1 specification provided at project kickoff.

- **Product:** Inkubify ("Ideas → Plans → Reality"), Pakistan-only founder roadmap platform.
- **Scope:** Splash, 3 welcome slides, email+password sign-up with email verification, login, forgot/reset password, 4-step + review founder profile wizard, profile edit, dashboard placeholder, RLS + storage, docs system.
- **Out of scope:** Business profile (`/business/*`), roadmap generation, milestones, reminders, social login, payments, SMS OTP.
- **Stack:** Nuxt 3 + Tailwind CSS + Pinia + VeeValidate/Zod + `@nuxtjs/supabase`; FastAPI (`/api/v1`); Supabase (Postgres + Auth + Storage + RLS).
- **Brand palette (strict):** `navy-900` `#142535`, `navy-700` `#23384B`, `snow-100` `#F7F7F7`, `gold-500` `#C19829`.
- **Logo rule:** Render via `components/brand/AppLogo.vue` alone; never place text beside it or enclose in a circle.
- **Milestones:** M0 (Bootstrap), M1 (Database), M2 (Design system), M3 (API core), M4 (Splash/Welcome/Auth), M5 (Profile wizard), M6 (Profile edit + dashboard), M7 (Hardening), M8 (Tests & docs).
