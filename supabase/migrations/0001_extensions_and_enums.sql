-- 0001_extensions_and_enums.sql
-- Phase 1: Extensions and domain enum types

create extension if not exists citext;

create type public.gender_t            as enum ('female', 'male', 'other', 'prefer_not_to_say');
create type public.language_t          as enum ('en', 'ur');
create type public.education_t         as enum ('matric_olevels', 'intermediate_alevels', 'diploma', 'bachelors', 'masters', 'phd', 'other');
create type public.occupation_t        as enum ('student', 'employed', 'self_employed', 'freelancer', 'unemployed', 'other');
create type public.work_experience_t   as enum ('none', 'lt_1', '1_3', '3_5', '5_plus');
create type public.prior_business_t    as enum ('none', 'tried_before', 'running_now');
create type public.primary_goal_t      as enum ('side_income', 'full_time_business', 'scale_existing', 'explore_learn');
create type public.weekly_hours_t      as enum ('lt_5', '5_10', '10_20', '20_40', '40_plus');
create type public.proficiency_t       as enum ('beginner', 'intermediate', 'advanced');
create type public.onboarding_status_t as enum ('not_started', 'in_progress', 'completed');
