-- neuroguIA — índices y vistas calculadas para dashboard

drop view if exists public.v_dashboard_whoqol cascade;
drop view if exists public.v_whoqol_participant_scores cascade;
drop view if exists public.v_dashboard_weeks cascade;
drop view if exists public.v_dashboard_time_bands cascade;
drop view if exists public.v_dashboard_states cascade;
drop view if exists public.v_dashboard_categories cascade;
drop view if exists public.v_dashboard_usage cascade;
drop view if exists public.v_dashboard_prepost cascade;
drop view if exists public.v_dashboard_kpis cascade;
drop view if exists public.v_dashboard_sessions cascade;

create index if not exists idx_ng_messages_session
  on public.ng_messages(session_id);
create index if not exists idx_ng_messages_created
  on public.ng_messages(created_at);
create index if not exists idx_case_created
  on public.ng_case_memory(created_at);
create index if not exists idx_case_category
  on public.ng_case_memory(detected_category);
create index if not exists idx_case_state
  on public.ng_case_memory(primary_state);
create index if not exists idx_curation_source_case
  on public.ng_conversation_curation(source_case_id);
create index if not exists idx_curation_session
  on public.ng_conversation_curation(session_scope_id);
create index if not exists idx_participants_group
  on public.research_participants(group_type);
create index if not exists idx_prepost_group
  on public.research_prepost(group_type);
create index if not exists idx_whoqol_group
  on public.research_whoqol_items(group_type);

create or replace view public.v_dashboard_sessions
with (security_invoker = true) as
select
  m.case_id,
  min(m.session_scope_id) as session_scope_id,
  min(m.family_id::text)::uuid as family_id,
  min(m.profile_id::text)::uuid as profile_id,
  min(m.created_at) as started_at,
  max(m.created_at) as ended_at,
  round((extract(epoch from (max(m.created_at) - min(m.created_at))) / 60.0)::numeric, 2)
    as duration_minutes,
  count(*) as message_count,
  count(*) filter (where m.speaker = 'user') as user_messages,
  count(*) filter (where m.speaker = 'assistant') as assistant_messages,
  min(c.detected_category) as detected_category,
  min(c.primary_state) as primary_state
from public.conversation_messages_supplemental m
join public.ng_case_memory c on c.case_id = m.case_id
group by m.case_id;

create or replace view public.v_dashboard_kpis
with (security_invoker = true) as
select
  (select count(*) from public.research_participants) as participants_total,
  (select count(*) from public.research_participants where group_type = 'Experimental')
    as participants_experimental,
  (select count(*) from public.research_participants where group_type = 'Control')
    as participants_control,
  (select count(distinct family_code) from public.research_participants)
    as research_family_units,
  (select count(*) from public.ng_families) as operational_families,
  (select count(*) from public.ng_profiles) as operational_profiles,
  (select count(*) from public.ng_case_memory) as sessions_total,
  (select count(*) from public.conversation_messages_supplemental) as messages_total,
  (select count(*) from public.conversation_messages_supplemental where speaker = 'user')
    as user_messages,
  (select count(*) from public.conversation_messages_supplemental where speaker = 'assistant')
    as assistant_messages,
  (select round(avg(duration_minutes), 2) from public.v_dashboard_sessions)
    as average_session_duration_minutes,
  (select min(started_at) from public.v_dashboard_sessions) as first_session_at,
  (select max(ended_at) from public.v_dashboard_sessions) as last_session_at;

create or replace view public.v_dashboard_prepost
with (security_invoker = true) as
select
  group_type,
  count(*) as n,
  round(avg(stress_pre)::numeric, 2) as stress_pre_mean,
  round(avg(stress_post)::numeric, 2) as stress_post_mean,
  round(avg(stress_improvement)::numeric, 2) as stress_improvement_mean,
  round(avg(anxiety_pre)::numeric, 2) as anxiety_pre_mean,
  round(avg(anxiety_post)::numeric, 2) as anxiety_post_mean,
  round(avg(anxiety_improvement)::numeric, 2) as anxiety_improvement_mean,
  round(avg(depression_pre)::numeric, 2) as depression_pre_mean,
  round(avg(depression_post)::numeric, 2) as depression_post_mean,
  round(avg(depression_improvement)::numeric, 2) as depression_improvement_mean,
  round(avg(support_pre_1_5)::numeric, 2) as support_pre_mean,
  round(avg(support_post_1_5)::numeric, 2) as support_post_mean,
  round(avg(support_improvement_1_5)::numeric, 2) as support_improvement_mean
from public.research_prepost
group by group_type;

create or replace view public.v_dashboard_usage
with (security_invoker = true) as
select
  count(*) as sessions_total,
  sum(message_count) as messages_total,
  count(distinct family_id) as active_families,
  count(distinct profile_id) as active_profiles,
  round(avg(message_count)::numeric, 2) as average_messages_per_session,
  round(avg(duration_minutes)::numeric, 2) as average_session_duration_minutes,
  percentile_cont(0.5) within group (order by duration_minutes)
    as median_session_duration_minutes,
  count(*) filter (where duration_minutes > 10) as sessions_over_10_minutes
from public.v_dashboard_sessions;

create or replace view public.v_dashboard_categories
with (security_invoker = true) as
select
  detected_category,
  count(*) as sessions,
  round(
    100.0 * count(*)::numeric / sum(count(*)) over (),
    2
  ) as percentage
from public.ng_case_memory
group by detected_category
order by sessions desc, detected_category;

create or replace view public.v_dashboard_states
with (security_invoker = true) as
select
  primary_state,
  count(*) as sessions,
  round(
    100.0 * count(*)::numeric / sum(count(*)) over (),
    2
  ) as percentage
from public.ng_case_memory
group by primary_state
order by sessions desc, primary_state;

create or replace view public.v_dashboard_time_bands
with (security_invoker = true) as
with classified as (
  select
    case
      when extract(hour from started_at at time zone 'America/Mexico_City') between 0 and 5
        then '00:00–05:59'
      when extract(hour from started_at at time zone 'America/Mexico_City') between 6 and 11
        then '06:00–11:59'
      when extract(hour from started_at at time zone 'America/Mexico_City') between 12 and 17
        then '12:00–17:59'
      else '18:00–23:59'
    end as time_band,
    case
      when extract(hour from started_at at time zone 'America/Mexico_City') between 0 and 5 then 1
      when extract(hour from started_at at time zone 'America/Mexico_City') between 6 and 11 then 2
      when extract(hour from started_at at time zone 'America/Mexico_City') between 12 and 17 then 3
      else 4
    end as band_order
  from public.v_dashboard_sessions
)
select
  time_band,
  count(*) as sessions,
  round(100.0 * count(*)::numeric / sum(count(*)) over (), 2) as percentage
from classified
group by time_band, band_order
order by band_order;

create or replace view public.v_dashboard_weeks
with (security_invoker = true) as
select
  date_trunc(
    'week',
    s.started_at at time zone 'America/Mexico_City'
  )::date as week_start,
  count(*) as sessions,
  sum(s.message_count) as messages,
  count(distinct s.family_id) as active_families,
  round(avg(s.duration_minutes)::numeric, 2) as average_duration_minutes
from public.v_dashboard_sessions s
group by week_start
order by week_start;

create or replace view public.v_whoqol_participant_scores
with (security_invoker = true) as
select
  participant_id,
  group_type,
  family_id,
  (payload ->> 'q1_pre')::numeric as global_quality_pre,
  (payload ->> 'q1_post')::numeric as global_quality_post,
  (payload ->> 'q2_pre')::numeric as general_health_pre,
  (payload ->> 'q2_post')::numeric as general_health_post,
  round((
    (
      (6 - (payload ->> 'q3_pre')::numeric)
      + (6 - (payload ->> 'q4_pre')::numeric)
      + (payload ->> 'q10_pre')::numeric
      + (payload ->> 'q15_pre')::numeric
      + (payload ->> 'q16_pre')::numeric
      + (payload ->> 'q17_pre')::numeric
      + (payload ->> 'q18_pre')::numeric
    ) / 7.0 - 1
  ) * 25, 2) as physical_pre_0_100,
  round((
    (
      (6 - (payload ->> 'q3_post')::numeric)
      + (6 - (payload ->> 'q4_post')::numeric)
      + (payload ->> 'q10_post')::numeric
      + (payload ->> 'q15_post')::numeric
      + (payload ->> 'q16_post')::numeric
      + (payload ->> 'q17_post')::numeric
      + (payload ->> 'q18_post')::numeric
    ) / 7.0 - 1
  ) * 25, 2) as physical_post_0_100,
  round((
    (
      (payload ->> 'q5_pre')::numeric
      + (payload ->> 'q6_pre')::numeric
      + (payload ->> 'q7_pre')::numeric
      + (payload ->> 'q11_pre')::numeric
      + (payload ->> 'q19_pre')::numeric
      + (6 - (payload ->> 'q26_pre')::numeric)
    ) / 6.0 - 1
  ) * 25, 2) as psychological_pre_0_100,
  round((
    (
      (payload ->> 'q5_post')::numeric
      + (payload ->> 'q6_post')::numeric
      + (payload ->> 'q7_post')::numeric
      + (payload ->> 'q11_post')::numeric
      + (payload ->> 'q19_post')::numeric
      + (6 - (payload ->> 'q26_post')::numeric)
    ) / 6.0 - 1
  ) * 25, 2) as psychological_post_0_100,
  round((
    (
      (payload ->> 'q20_pre')::numeric
      + (payload ->> 'q21_pre')::numeric
      + (payload ->> 'q22_pre')::numeric
    ) / 3.0 - 1
  ) * 25, 2) as social_pre_0_100,
  round((
    (
      (payload ->> 'q20_post')::numeric
      + (payload ->> 'q21_post')::numeric
      + (payload ->> 'q22_post')::numeric
    ) / 3.0 - 1
  ) * 25, 2) as social_post_0_100,
  round((
    (
      (payload ->> 'q8_pre')::numeric
      + (payload ->> 'q9_pre')::numeric
      + (payload ->> 'q12_pre')::numeric
      + (payload ->> 'q13_pre')::numeric
      + (payload ->> 'q14_pre')::numeric
      + (payload ->> 'q23_pre')::numeric
      + (payload ->> 'q24_pre')::numeric
      + (payload ->> 'q25_pre')::numeric
    ) / 8.0 - 1
  ) * 25, 2) as environment_pre_0_100,
  round((
    (
      (payload ->> 'q8_post')::numeric
      + (payload ->> 'q9_post')::numeric
      + (payload ->> 'q12_post')::numeric
      + (payload ->> 'q13_post')::numeric
      + (payload ->> 'q14_post')::numeric
      + (payload ->> 'q23_post')::numeric
      + (payload ->> 'q24_post')::numeric
      + (payload ->> 'q25_post')::numeric
    ) / 8.0 - 1
  ) * 25, 2) as environment_post_0_100
from public.research_whoqol_items;

create or replace view public.v_dashboard_whoqol
with (security_invoker = true) as
select
  group_type,
  count(*) as n,
  round(avg(physical_pre_0_100), 2) as physical_pre,
  round(avg(physical_post_0_100), 2) as physical_post,
  round(avg(psychological_pre_0_100), 2) as psychological_pre,
  round(avg(psychological_post_0_100), 2) as psychological_post,
  round(avg(social_pre_0_100), 2) as social_pre,
  round(avg(social_post_0_100), 2) as social_post,
  round(avg(environment_pre_0_100), 2) as environment_pre,
  round(avg(environment_post_0_100), 2) as environment_post,
  round(avg(
    (
      physical_pre_0_100
      + psychological_pre_0_100
      + social_pre_0_100
      + environment_pre_0_100
    ) / 4.0
  ), 2) as global_descriptive_pre,
  round(avg(
    (
      physical_post_0_100
      + psychological_post_0_100
      + social_post_0_100
      + environment_post_0_100
    ) / 4.0
  ), 2) as global_descriptive_post
from public.v_whoqol_participant_scores
group by group_type;

comment on view public.v_dashboard_kpis is
  'Indicadores generales calculados directamente desde las tablas canónicas.';
comment on view public.v_dashboard_prepost is
  'Medias pretest-postest por grupo; apoyo reportado como índice propio 1–5.';
comment on view public.v_dashboard_whoqol is
  'WHOQOL-BREF independiente, resumido por grupo y dominio en escala 0–100.';
