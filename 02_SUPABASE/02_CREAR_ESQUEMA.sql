-- neuroguIA — creación del esquema operativo y de investigación
-- PostgreSQL / Supabase
-- Requisito: haber ejecutado 01_RESPALDO_BASE_ACTUAL.sql.
-- Este script sustituye únicamente las tablas canónicas de neuroguIA.

do $$
declare
  latest_backup text;
  archived_count bigint;
begin
  if not exists (
    select 1
    from information_schema.tables
    where table_schema = 'neuroguia_admin'
      and table_name = 'migration_runs'
  ) then
    raise exception 'No existe el registro de respaldo. Ejecute 01_RESPALDO_BASE_ACTUAL.sql.';
  end if;

  if not exists (
    select 1
    from neuroguia_admin.migration_runs
    where backup_completed = true
  ) then
    raise exception 'No hay un respaldo completo registrado. Se cancela la sustitución.';
  end if;

  select backup_schema
  into latest_backup
  from neuroguia_admin.migration_runs
  where backup_completed = true
  order by run_id desc
  limit 1;

  if to_regclass('neuroguia_admin.ng_case_memory_archive') is null then
    raise exception
      'No existe el archivo administrativo de casos. Ejecute 01C_ARCHIVAR_CASOS_NO_ANALITICOS.sql.';
  end if;

  select count(*)
  into archived_count
  from neuroguia_admin.ng_case_memory_archive
  where source_backup_schema = latest_backup
    and analysis_eligible = false;

  if archived_count <> 39 then
    raise exception
      'El archivo administrativo debe contener 39 casos no analíticos; contiene %.',
      archived_count;
  end if;
end
$$;

begin;

drop view if exists public.v_dashboard_whoqol cascade;
drop view if exists public.v_dashboard_weeks cascade;
drop view if exists public.v_dashboard_time_bands cascade;
drop view if exists public.v_dashboard_states cascade;
drop view if exists public.v_dashboard_sessions cascade;
drop view if exists public.v_dashboard_categories cascade;
drop view if exists public.v_dashboard_usage cascade;
drop view if exists public.v_dashboard_prepost cascade;
drop view if exists public.v_dashboard_kpis cascade;

drop table if exists
  public.research_transformations,
  public.research_provenance,
  public.research_analysis_results,
  public.research_instrument_items,
  public.research_instruments,
  public.research_whoqol_items,
  public.research_prepost,
  public.research_participants,
  public.ng_conversation_curation,
  public.ng_learned_patterns,
  public.ng_user_context_memory,
  public.ng_routines,
  public.ng_response_memory,
  public.ng_messages,
  public.ng_messages_supplemental,
  public.conversation_messages_supplemental,
  public.ng_case_memory,
  public.ng_profiles,
  public.ng_families,
  public.app_meta
cascade;

create extension if not exists "uuid-ossp";

create table if not exists public.app_meta (
  meta_key text primary key,
  meta_value jsonb not null,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table if not exists public.ng_families (
  family_id uuid primary key,
  unit_type text not null,
  caregiver_alias text not null,
  context_notes text,
  support_network text,
  environmental_factors text,
  global_history text,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table if not exists public.ng_profiles (
  profile_id uuid primary key,
  family_id uuid not null references public.ng_families(family_id) on delete cascade,
  alias text not null,
  age integer not null check (age between 0 and 120),
  role text not null,
  conditions jsonb,
  strengths jsonb,
  triggers jsonb,
  early_signs jsonb,
  helpful_strategies jsonb,
  harmful_strategies jsonb,
  sensory_needs jsonb,
  emotional_needs jsonb,
  autonomy_level text,
  sleep_profile text,
  school_profile text,
  executive_profile text,
  evolution_notes text,
  is_active boolean not null,
  created_at timestamptz not null,
  updated_at timestamptz not null,
  constraint chk_ng_profiles_school_scope check (
    (
      role in ('adolescente', 'hijo', 'hija')
      and school_profile is not null
    )
    or role not in ('adolescente', 'hijo', 'hija')
  )
);

create table if not exists public.ng_case_memory (
  case_id uuid primary key,
  family_id uuid not null references public.ng_families(family_id) on delete cascade,
  profile_id uuid not null references public.ng_profiles(profile_id) on delete cascade,
  unit_type text,
  created_at timestamptz,
  updated_at timestamptz,
  raw_input text,
  normalized_summary text,
  detected_category text,
  detected_stage text,
  primary_state text,
  secondary_states jsonb,
  emotional_intensity double precision check (emotional_intensity between 0 and 1),
  caregiver_capacity double precision check (caregiver_capacity between 0 and 1),
  sensory_overload_risk double precision check (sensory_overload_risk between 0 and 1),
  executive_block_risk double precision check (executive_block_risk between 0 and 1),
  meltdown_risk double precision check (meltdown_risk between 0 and 1),
  shutdown_risk double precision check (shutdown_risk between 0 and 1),
  burnout_risk double precision check (burnout_risk between 0 and 1),
  sleep_disruption_risk double precision check (sleep_disruption_risk between 0 and 1),
  suggested_strategy text,
  suggested_microaction text,
  suggested_routine_type text,
  response_mode text,
  user_feedback text,
  observed_result text,
  usefulness_score double precision check (usefulness_score between 0 and 1),
  applied_successfully boolean,
  helps_patterns jsonb,
  worsens_patterns jsonb,
  followup_needed boolean,
  tags jsonb
);

create table if not exists public.conversation_messages_supplemental (
  message_id uuid primary key,
  case_id uuid not null references public.ng_case_memory(case_id) on delete cascade,
  family_id uuid not null references public.ng_families(family_id) on delete cascade,
  profile_id uuid not null references public.ng_profiles(profile_id) on delete cascade,
  session_scope_id text not null,
  speaker text not null check (speaker in ('user','assistant')),
  turn_index integer not null,
  message_text text not null,
  message_length_chars integer not null,
  detected_category text,
  primary_state text,
  created_at timestamptz not null
);

create table if not exists public.ng_messages (
  id bigint generated by default as identity primary key,
  session_id text not null,
  user_role text not null,
  message text not null,
  detected_category text,
  emotional_state text,
  profile_id uuid references public.ng_profiles(profile_id) on delete cascade,
  family_id uuid references public.ng_families(family_id) on delete cascade,
  created_at timestamptz not null
);

create table if not exists public.ng_response_memory (
  response_id uuid primary key,
  family_id uuid references public.ng_families(family_id) on delete cascade,
  profile_id uuid references public.ng_profiles(profile_id) on delete cascade,
  detected_intent text,
  detected_category text,
  primary_state text,
  conversation_stage text,
  complexity_signature text,
  conditions_signature jsonb,
  response_text text,
  response_structure_json jsonb,
  source_type text,
  confidence_score double precision,
  usefulness_score double precision,
  approved_for_reuse boolean,
  usage_count integer,
  success_count integer,
  failure_count integer,
  avoid_rules jsonb,
  must_include jsonb,
  supporting_patterns jsonb,
  tags jsonb,
  llm_prompt_version text,
  origin_case_id uuid references public.ng_case_memory(case_id) on delete set null,
  notes text,
  is_active boolean,
  created_at timestamptz,
  updated_at timestamptz
);

create table if not exists public.ng_routines (
  routine_id uuid primary key,
  family_id uuid references public.ng_families(family_id) on delete cascade,
  profile_id uuid references public.ng_profiles(profile_id) on delete cascade,
  routine_type text,
  routine_name text,
  goal text,
  steps jsonb,
  short_version jsonb,
  adjustments jsonb,
  indicators jsonb,
  followup_question text,
  source_case_id uuid references public.ng_case_memory(case_id) on delete set null,
  is_active boolean,
  created_at timestamptz,
  updated_at timestamptz
);

create table if not exists public.ng_user_context_memory (
  scope_key text primary key,
  scope_type text not null check (scope_type in ('family', 'profile')),
  family_id uuid not null references public.ng_families(family_id) on delete cascade,
  profile_id uuid references public.ng_profiles(profile_id) on delete cascade,
  session_scope_id text,
  inferred_user_role text,
  role_confidence double precision,
  role_source text,
  conversation_preferences_json jsonb,
  recurrent_topics_json jsonb,
  recurrent_signals_json jsonb,
  helpful_strategies_json jsonb,
  helpful_routines_json jsonb,
  last_useful_domain text,
  last_useful_phase text,
  summary_snapshot_json jsonb,
  source_case_id uuid references public.ng_case_memory(case_id) on delete set null,
  created_at timestamptz,
  updated_at timestamptz,
  constraint chk_ng_user_context_scope check (
    (scope_type = 'family' and profile_id is null)
    or (scope_type = 'profile' and profile_id is not null)
  )
);

create table if not exists public.ng_learned_patterns (
  pattern_id uuid primary key,
  family_id uuid references public.ng_families(family_id) on delete cascade,
  profile_id uuid references public.ng_profiles(profile_id) on delete cascade,
  context_key text,
  helps jsonb,
  worsens jsonb,
  confidence_level double precision,
  usage_count integer,
  last_seen timestamptz,
  created_at timestamptz,
  updated_at timestamptz
);

create table if not exists public.ng_conversation_curation (
  curation_id text primary key,
  dedupe_key text,
  scope_key text,
  scope_type text,
  family_id uuid references public.ng_families(family_id) on delete cascade,
  profile_id uuid references public.ng_profiles(profile_id) on delete cascade,
  session_scope_id text,
  source_case_id uuid references public.ng_case_memory(case_id) on delete cascade,
  review_status text,
  candidate_targets_json jsonb,
  review_notes text,
  input_summary_json jsonb,
  detected_category text,
  detected_intent text,
  primary_state text,
  secondary_states_json jsonb,
  conversation_domain text,
  conversation_phase text,
  speaker_role text,
  signal_summary_json jsonb,
  response_text text,
  response_structure_json jsonb,
  response_mode text,
  generation_source text,
  provider text,
  model text,
  used_stub_fallback boolean,
  fallback_reason text,
  llm_enabled boolean,
  llm_quality_score double precision,
  llm_approved boolean,
  metadata_json jsonb,
  created_at timestamptz,
  updated_at timestamptz
);

create table if not exists public.research_participants (
  participant_id text primary key,
  group_type text not null check (group_type in ('Experimental','Control')),
  family_code text not null,
  child_case_code text,
  research_profile_code text,
  role text,
  age integer,
  sex text,
  education text,
  occupation text,
  children_count integer,
  reported_context text,
  cohabitation_time text,
  internet_access text,
  device_access text,
  consent_status text,
  data_scope text,
  source_file text
);

create table if not exists public.research_prepost (
  participant_id text primary key references public.research_participants(participant_id) on delete cascade,
  family_code text,
  student_code text,
  participant_type text,
  relation_to_student text,
  group_type text not null check (group_type in ('Experimental', 'Control')),
  stress_pre double precision,
  stress_post double precision,
  stress_improvement double precision,
  anxiety_pre double precision,
  anxiety_post double precision,
  anxiety_improvement double precision,
  depression_pre double precision,
  depression_post double precision,
  depression_improvement double precision,
  support_index_pre_raw_20_100 double precision,
  support_index_post_raw_20_100 double precision,
  support_pre_1_5 double precision,
  support_post_1_5 double precision,
  support_improvement_1_5 double precision,
  reported_sessions double precision,
  reported_total_duration_min double precision,
  reported_mean_session_duration_min double precision,
  exposure_status text,
  research_notes text,
  constraint chk_research_prepost_usage_scope check (
    (
      group_type = 'Experimental'
      and reported_sessions is not null
      and reported_total_duration_min is not null
      and reported_mean_session_duration_min is not null
    )
    or (
      group_type = 'Control'
      and reported_sessions is null
      and reported_total_duration_min is null
      and reported_mean_session_duration_min is null
    )
  )
);

create table if not exists public.research_whoqol_items (
  participant_id text primary key,
  group_type text,
  family_id text,
  payload jsonb not null
);

create table if not exists public.research_instruments (
  instrument_id text primary key,
  instrument_name text,
  instrument_type text,
  items_or_fields double precision not null,
  response_scale text,
  moments text,
  score_method text,
  documented_reliability text,
  source_file text
);

create table if not exists public.research_instrument_items (
  instrument_id text references public.research_instruments(instrument_id) on delete cascade,
  item_code text,
  domain text,
  item_text text,
  response_scale text,
  reverse_scored boolean,
  primary key (instrument_id, item_code)
);

create table if not exists public.research_analysis_results (
  analysis_id bigint generated by default as identity primary key,
  analysis_family text,
  outcome text,
  statistic text,
  value double precision,
  unit text,
  source_file text,
  calculated_at date
);

create table if not exists public.research_provenance (
  source_file text primary key,
  source_sha256 text not null,
  source_size_bytes bigint,
  source_role text,
  provenance_basis text,
  custodian text
);

create table if not exists public.research_transformations (
  step_id text primary key,
  output text,
  source text,
  operation text,
  records_in integer,
  records_out integer,
  data_values_modified text,
  responsible text,
  date date
);

create index if not exists idx_profiles_family on public.ng_profiles(family_id);
create unique index if not exists uq_ng_profiles_alias_ci
  on public.ng_profiles(lower(alias));
create unique index if not exists uq_ng_families_caregiver_alias_ci
  on public.ng_families(lower(caregiver_alias));
create index if not exists idx_case_family on public.ng_case_memory(family_id);
create index if not exists idx_case_profile on public.ng_case_memory(profile_id);
create index if not exists idx_messages_case on public.conversation_messages_supplemental(case_id);
create index if not exists idx_messages_family on public.conversation_messages_supplemental(family_id);
create index if not exists idx_messages_profile on public.conversation_messages_supplemental(profile_id);
create index if not exists idx_messages_session on public.conversation_messages_supplemental(session_scope_id);
create index if not exists idx_messages_created on public.conversation_messages_supplemental(created_at);
create index if not exists idx_prepost_family on public.research_prepost(family_code);

commit;
