-- neuroguIA — seguridad de tablas y vistas
-- Supuesto operativo: Streamlit accede desde backend mediante service_role.
-- La clave service_role nunca debe enviarse al navegador ni guardarse en el repositorio.

do $$
declare
  object_name text;
  protected_tables text[] := array[
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
  ];
  protected_views text[] := array[
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
  ];
begin
  foreach object_name in array protected_tables loop
    execute format('alter table public.%I enable row level security', object_name);
    execute format('revoke all on table public.%I from anon, authenticated', object_name);
    execute format('grant all on table public.%I to service_role', object_name);
  end loop;

  foreach object_name in array protected_views loop
    execute format('revoke all on table public.%I from anon, authenticated', object_name);
    execute format('grant select on table public.%I to service_role', object_name);
  end loop;
end
$$;

grant usage, select on all sequences in schema public to service_role;

comment on schema public is
  'Esquema operativo. Los datos neuroguIA se consultan desde el backend autorizado.';
