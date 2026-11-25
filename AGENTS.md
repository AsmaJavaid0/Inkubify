# Inkubify — Agent Instructions

Inkubify is a Pakistan-only founder roadmap platform. Stack: Nuxt 3 (apps/web), FastAPI (apps/api), Supabase (supabase/). Do not change the stack.

## Read order at the start of EVERY session
1. docs/PROGRESS.md  (where we are, what's next)
2. docs/ARCHITECTURE.md, docs/DECISIONS.md
3. docs/API.md and docs/DATABASE.md when touching those areas
4. docs/SPEC_PHASE1.md (the original Phase 1 spec)

## At the END of EVERY session
- Update docs/PROGRESS.md (checklist + session log + next steps)
- Update ARCHITECTURE / API / DATABASE docs if reality changed
- Log non-obvious choices in docs/DECISIONS.md

## Rules
- Brand: colours #142535 #23384B #F7F7F7 #C19829 only; logo image alone (no text beside it, no circle) via components/brand/AppLogo.vue
- Never commit secrets; never expose the Supabase service_role key to the browser
- Server-side validation is the authority; client validation is for UX
- Never edit an applied migration; add a new one
- Out of scope: business profile, roadmap, payments, social login
- If the spec is ambiguous: choose the conservative option and log it in docs/DECISIONS.md
