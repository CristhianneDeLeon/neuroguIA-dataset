-- =========================================================
-- neuroguIA Dataset Schema
-- PostgreSQL / Supabase Relational Structure
-- Author: Cristhianne De León
-- Version: 1.0
-- =========================================================

-- =========================================================
-- EXTENSIONS
-- =========================================================

create extension if not exists "uuid-ossp";

-- =========================================================
-- TABLE: app_meta
-- =========================================================

create table if not exists public.app_meta (
    meta_key text primary key,
    meta_value text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- =========================================================
-- TABLE: ng_families
-- =========================================================

create table if not exists public.ng_families (
    family_id uuid primary key,
    unit_type text,
    caregiver_alias text,
    context_notes text,
    support_network text,
    environment_type text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- =========================================================
-- TABLE: ng_profiles
-- =========================================================

create table if not exists public.ng_profiles (
    profile_id uuid primary key,
    family_id uuid references public.ng_families(family_id) on delete cascade,
    profile_alias text,
    neurotype text,
    age_range text,
    support_level text,
    communication_style text,
    sensory_profile text,
    school_profile boolean default false,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- =========================================================
-- TABLE: ng_case_memory
-- =========================================================

create table if not exists public.ng_case_memory (
    case_id uuid primary key,
    family_id uuid references public.ng_families(family_id) on delete cascade,
    profile_id uuid references public.ng_profiles(profile_id) on delete cascade,

    detected_category text,
    detected_stage text,

    primary_state text,
    secondary_states jsonb,

    emotional_intensity double precision,
    caregiver_capacity double precision,

    sensory_overload_risk double precision,
    executive_block_risk double precision,
    meltdown_risk double precision,
    shutdown_risk double precision,
    burnout_risk double precision,
    sleep_disruption_risk double precision,

    suggested_strategy text,
    suggested_microaction text,
    suggested_routine_type text,

    response_mode text,
    user_feedback text,

    raw_input text,
    normalized_summary text,

    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- =========================================================
-- TABLE: learned_patterns
-- =========================================================

create table if not exists public.learned_patterns (
    pattern_id uuid primary key,

    category text,
    trigger_context text,

    response_effectiveness double precision,
    reinforcement_score double precision,

    created_at timestamptz default now()
);

-- =========================================================
-- TABLE: ng_response_memory
-- =========================================================

create table if not exists public.ng_response_memory (
    response_id uuid primary key,

    profile_id uuid references public.ng_profiles(profile_id) on delete cascade,

    response_text text,
    category text,

    reuse_score double precision,
    validation_status text,

    created_at timestamptz default now()
);

-- =========================================================
-- TABLE: ng_routines
-- =========================================================

create table if not exists public.ng_routines (
    routine_id uuid primary key,

    profile_id uuid references public.ng_profiles(profile_id) on delete cascade,

    routine_type text,
    routine_goal text,

    sensory_support text,
    executive_support text,

    created_at timestamptz default now()
);

-- =========================================================
-- TABLE: ng_user_context_memory
-- =========================================================

create table if not exists public.ng_user_context_memory (
    context_id uuid primary key,

    profile_id uuid references public.ng_profiles(profile_id) on delete cascade,

    memory_summary text,

    relevance_score double precision,
    retrieval_frequency integer,

    session_scope_id text,

    created_at timestamptz default now()
);

-- =========================================================
-- TABLE: conversation_curation
-- =========================================================

create table if not exists public.conversation_curation (
    conversation_id uuid primary key,

    category text,

    validation_score double precision,

    reviewed_flag boolean default false,

    created_at timestamptz default now()
);

-- =========================================================
-- TABLE: conversation_messages_supplemental
-- =========================================================

create table if not exists public.conversation_messages_supplemental (
    message_id uuid primary key,

    case_id uuid references public.ng_case_memory(case_id) on delete cascade,
    family_id uuid references public.ng_families(family_id) on delete cascade,
    profile_id uuid references public.ng_profiles(profile_id) on delete cascade,

    session_scope_id text,

    speaker text,
    turn_index integer,

    message_text text,

    message_length_chars integer,

    detected_category text,
    primary_state text,

    fallback_reason text,

    created_at timestamptz default now()
);

-- =========================================================
-- TABLE: dataset_summary
-- =========================================================

create table if not exists public.dataset_summary (
    metric text primary key,
    value numeric,
    description text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- =========================================================
-- TABLE: category_distribution
-- =========================================================

create table if not exists public.category_distribution (
    detected_category text primary key,
    count bigint
);

-- =========================================================
-- TABLE: state_distribution
-- =========================================================

create table if not exists public.state_distribution (
    primary_state text primary key,
    count bigint
);

-- =========================================================
-- TABLE: validation_report_conversation_messages
-- =========================================================

create table if not exists public.validation_report_conversation_messages (
    metric text primary key,
    value bigint
);

-- =========================================================
-- INDEXES
-- =========================================================

create index if not exists idx_profiles_family
on public.ng_profiles(family_id);

create index if not exists idx_case_memory_family
on public.ng_case_memory(family_id);

create index if not exists idx_case_memory_profile
on public.ng_case_memory(profile_id);

create index if not exists idx_case_memory_category
on public.ng_case_memory(detected_category);

create index if not exists idx_case_memory_state
on public.ng_case_memory(primary_state);

create index if not exists idx_response_memory_profile
on public.ng_response_memory(profile_id);

create index if not exists idx_routines_profile
on public.ng_routines(profile_id);

create index if not exists idx_context_memory_profile
on public.ng_user_context_memory(profile_id);

create index if not exists idx_messages_case
on public.conversation_messages_supplemental(case_id);

create index if not exists idx_messages_profile
on public.conversation_messages_supplemental(profile_id);

create index if not exists idx_messages_category
on public.conversation_messages_supplemental(detected_category);

create index if not exists idx_messages_state
on public.conversation_messages_supplemental(primary_state);

-- =========================================================
-- COMMENTS
-- =========================================================

comment on schema public is
'neuroguIA hybrid conversational AI relational dataset schema';

comment on table public.ng_case_memory is
'Stores longitudinal contextual conversational memory';

comment on table public.conversation_messages_supplemental is
'Supplemental conversational messages for NLP and longitudinal analytics';

comment on table public.ng_response_memory is
'Reusable validated conversational responses';

comment on table public.ng_user_context_memory is
'Persistent contextual conversational memory';

-- =========================================================
-- END OF SCHEMA
-- =========================================================