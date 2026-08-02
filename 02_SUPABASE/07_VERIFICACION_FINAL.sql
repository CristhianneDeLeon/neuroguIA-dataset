-- neuroguIA — verificación final de publicación y seguridad

do $$
declare
  problem_count bigint;
begin
  select count(*) into problem_count
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
    and not c.relrowsecurity;
  if problem_count > 0 then
    raise exception 'Hay % tablas canónicas sin RLS habilitado.', problem_count;
  end if;

  select count(*) into problem_count
  from information_schema.role_table_grants
  where table_schema = 'public'
    and grantee in ('anon', 'authenticated')
    and (
      table_name like 'ng_%'
      or table_name like 'research_%'
      or table_name in (
        'app_meta',
        'conversation_messages_supplemental',
        'v_dashboard_sessions',
        'v_dashboard_kpis',
        'v_dashboard_prepost',
        'v_dashboard_usage',
        'v_dashboard_categories',
        'v_dashboard_states',
        'v_dashboard_time_bands',
        'v_dashboard_weeks',
        'v_whoqol_participant_scores',
        'v_dashboard_whoqol'
      )
    );
  if problem_count > 0 then
    raise exception 'Persisten % privilegios directos para anon/authenticated.', problem_count;
  end if;

  if (select participants_total from public.v_dashboard_kpis) <> 562
     or (select participants_experimental from public.v_dashboard_kpis) <> 281
     or (select participants_control from public.v_dashboard_kpis) <> 281
     or (select sessions_total from public.v_dashboard_kpis) <> 6463
     or (select messages_total from public.v_dashboard_kpis) <> 47670 then
    raise exception 'Los KPI generales no reproducen los conteos canónicos.';
  end if;

  if (select sum(sessions) from public.v_dashboard_categories) <> 6463 then
    raise exception 'La vista de categorías no suma 6,463 sesiones.';
  end if;

  if (select sum(sessions) from public.v_dashboard_states) <> 6463 then
    raise exception 'La vista de estados no suma 6,463 sesiones.';
  end if;

  if (select sum(sessions) from public.v_dashboard_time_bands) <> 6463 then
    raise exception 'La vista de franjas horarias no suma 6,463 sesiones.';
  end if;

  if (select sum(n) from public.v_dashboard_prepost) <> 562 then
    raise exception 'La vista pre-post no suma 562 participantes.';
  end if;

  if (select sum(n) from public.v_dashboard_whoqol) <> 562 then
    raise exception 'La vista WHOQOL-BREF no suma 562 registros.';
  end if;

  if (
    select count(distinct lower(alias))
    from public.ng_profiles
  ) <> 619 then
    raise exception 'Los perfiles no conservan 619 alias únicos.';
  end if;

  if (
    select count(*)
    from public.research_instrument_items
  ) <> 92 then
    raise exception 'El catálogo instrumental no contiene 92 reactivos/campos.';
  end if;

  if (
    select count(*)
    from public.app_meta
    where meta_key in ('profile_alias_policy', 'null_semantics_policy')
  ) <> 2 then
    raise exception 'Faltan las políticas de alias o semántica de nulos.';
  end if;

  if (
    select count(*)
    from neuroguia_admin.ng_case_memory_archive a
    where a.analysis_eligible = false
      and a.source_backup_schema = (
        select backup_schema
        from neuroguia_admin.migration_runs
        where backup_completed = true
        order by run_id desc
        limit 1
      )
  ) <> 39 then
    raise exception 'El archivo administrativo no conserva los 39 casos no analíticos.';
  end if;
end
$$;

alter table neuroguia_admin.migration_runs
  add column if not exists published_at timestamptz,
  add column if not exists final_validation text;

update neuroguia_admin.migration_runs
set
  published_at = now(),
  final_validation = 'APROBADA'
where run_id = (
  select run_id
  from neuroguia_admin.migration_runs
  where backup_completed = true
  order by run_id desc
  limit 1
);

select * from public.v_dashboard_kpis;
select * from public.v_dashboard_prepost order by group_type;
select * from public.v_dashboard_usage;
select * from public.v_dashboard_categories;
select * from public.v_dashboard_states;
select * from public.v_dashboard_time_bands;
select * from public.v_dashboard_weeks;
select * from public.v_dashboard_whoqol order by group_type;

select
  'MIGRACIÓN APROBADA' as result,
  now() as verified_at,
  current_user as verified_by,
  619 as unique_profile_aliases,
  92 as documented_instrument_fields,
  39 as archived_nonresearch_cases;
