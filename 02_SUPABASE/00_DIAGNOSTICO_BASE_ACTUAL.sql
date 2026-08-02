-- neuroguIA — diagnóstico previo de la base activa
-- Solo lectura: no modifica tablas, registros ni políticas.

select
  current_database() as database_name,
  current_user as executed_by,
  now() as executed_at,
  version() as postgres_version;

select
  c.relname as table_name,
  c.reltuples::bigint as estimated_rows,
  c.relrowsecurity as rls_enabled,
  c.relforcerowsecurity as rls_forced
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind = 'r'
  and c.relname in (
    'app_meta',
    'ng_families',
    'ng_profiles',
    'ng_case_memory',
    'conversation_messages_supplemental',
    'ng_messages',
    'ng_response_memory',
    'ng_routines',
    'ng_user_context_memory',
    'ng_learned_patterns',
    'ng_conversation_curation',
    'research_participants',
    'research_prepost',
    'research_whoqol_items',
    'research_instruments',
    'research_instrument_items',
    'research_analysis_results',
    'research_provenance',
    'research_transformations'
  )
order by c.relname;

select
  table_name,
  ordinal_position,
  column_name,
  data_type,
  udt_name,
  is_nullable,
  column_default
from information_schema.columns
where table_schema = 'public'
  and table_name in (
    'app_meta',
    'ng_families',
    'ng_profiles',
    'ng_case_memory',
    'conversation_messages_supplemental',
    'ng_messages',
    'ng_response_memory',
    'ng_routines',
    'ng_user_context_memory',
    'ng_learned_patterns',
    'ng_conversation_curation',
    'research_participants',
    'research_prepost',
    'research_whoqol_items',
    'research_instruments',
    'research_instrument_items',
    'research_analysis_results',
    'research_provenance',
    'research_transformations'
  )
order by table_name, ordinal_position;

select
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
from pg_policies
where schemaname = 'public'
  and tablename like any (array['ng_%', 'research_%'])
order by tablename, policyname;

select
  table_name,
  grantee,
  string_agg(privilege_type, ', ' order by privilege_type) as privileges
from information_schema.role_table_grants
where table_schema = 'public'
  and grantee in ('anon', 'authenticated', 'service_role')
  and (
    table_name like 'ng_%'
    or table_name like 'research_%'
    or table_name in ('app_meta', 'conversation_messages_supplemental')
  )
group by table_name, grantee
order by table_name, grantee;
