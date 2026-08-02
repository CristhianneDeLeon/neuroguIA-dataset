-- neuroguIA — validación obligatoria posterior a la importación
-- Si alguna regla falla, el script termina con una excepción.

begin;

create temporary table expected_counts (
  table_name text primary key,
  expected_rows bigint not null
) on commit drop;

insert into expected_counts (table_name, expected_rows) values
  ('app_meta', 6),
  ('ng_families', 281),
  ('ng_profiles', 619),
  ('ng_case_memory', 6463),
  ('conversation_messages_supplemental', 47670),
  ('ng_messages', 47670),
  ('ng_response_memory', 465),
  ('ng_routines', 1468),
  ('ng_user_context_memory', 562),
  ('ng_learned_patterns', 1885),
  ('ng_conversation_curation', 6463),
  ('research_participants', 562),
  ('research_prepost', 562),
  ('research_whoqol_items', 562),
  ('research_instruments', 8),
  ('research_instrument_items', 92),
  ('research_analysis_results', 152),
  ('research_provenance', 20),
  ('research_transformations', 10);

create temporary table actual_counts (
  table_name text primary key,
  actual_rows bigint not null
) on commit drop;

insert into actual_counts (table_name, actual_rows)
select 'app_meta', count(*) from public.app_meta
union all select 'ng_families', count(*) from public.ng_families
union all select 'ng_profiles', count(*) from public.ng_profiles
union all select 'ng_case_memory', count(*) from public.ng_case_memory
union all select 'conversation_messages_supplemental', count(*) from public.conversation_messages_supplemental
union all select 'ng_messages', count(*) from public.ng_messages
union all select 'ng_response_memory', count(*) from public.ng_response_memory
union all select 'ng_routines', count(*) from public.ng_routines
union all select 'ng_user_context_memory', count(*) from public.ng_user_context_memory
union all select 'ng_learned_patterns', count(*) from public.ng_learned_patterns
union all select 'ng_conversation_curation', count(*) from public.ng_conversation_curation
union all select 'research_participants', count(*) from public.research_participants
union all select 'research_prepost', count(*) from public.research_prepost
union all select 'research_whoqol_items', count(*) from public.research_whoqol_items
union all select 'research_instruments', count(*) from public.research_instruments
union all select 'research_instrument_items', count(*) from public.research_instrument_items
union all select 'research_analysis_results', count(*) from public.research_analysis_results
union all select 'research_provenance', count(*) from public.research_provenance
union all select 'research_transformations', count(*) from public.research_transformations;

do $$
declare
  failures text;
  problem_count bigint;
begin
  select string_agg(
    format('%s: esperado %s, observado %s', e.table_name, e.expected_rows, a.actual_rows),
    '; '
  )
  into failures
  from expected_counts e
  join actual_counts a using (table_name)
  where e.expected_rows <> a.actual_rows;

  if failures is not null then
    raise exception 'Conteos incorrectos: %', failures;
  end if;

  select count(*) into problem_count
  from public.ng_profiles p
  left join public.ng_families f on f.family_id = p.family_id
  where f.family_id is null;
  if problem_count > 0 then
    raise exception 'Hay % perfiles sin familia.', problem_count;
  end if;

  select count(*) into problem_count
  from public.ng_case_memory c
  left join public.ng_families f on f.family_id = c.family_id
  left join public.ng_profiles p on p.profile_id = c.profile_id
  where f.family_id is null or p.profile_id is null;
  if problem_count > 0 then
    raise exception 'Hay % sesiones sin familia o perfil válido.', problem_count;
  end if;

  select count(*) into problem_count
  from public.conversation_messages_supplemental m
  left join public.ng_case_memory c on c.case_id = m.case_id
  left join public.ng_families f on f.family_id = m.family_id
  left join public.ng_profiles p on p.profile_id = m.profile_id
  where c.case_id is null or f.family_id is null or p.profile_id is null;
  if problem_count > 0 then
    raise exception 'Hay % mensajes con relaciones incompletas.', problem_count;
  end if;

  select count(*) into problem_count
  from public.research_prepost r
  left join public.research_participants p on p.participant_id = r.participant_id
  where p.participant_id is null or p.group_type <> r.group_type;
  if problem_count > 0 then
    raise exception 'Hay % registros pre-post sin participante o con grupo discordante.', problem_count;
  end if;

  select count(*) into problem_count
  from public.research_instrument_items i
  left join public.research_instruments n on n.instrument_id = i.instrument_id
  where n.instrument_id is null;
  if problem_count > 0 then
    raise exception 'Hay % reactivos sin instrumento válido.', problem_count;
  end if;

  select count(*) into problem_count
  from public.research_prepost
  where stress_pre not between 0 and 42
     or stress_post not between 0 and 42
     or anxiety_pre not between 0 and 42
     or anxiety_post not between 0 and 42
     or depression_pre not between 0 and 42
     or depression_post not between 0 and 42
     or support_pre_1_5 not between 1 and 5
     or support_post_1_5 not between 1 and 5;
  if problem_count > 0 then
    raise exception 'Hay % registros pre-post fuera de los rangos definidos.', problem_count;
  end if;

  select count(*) into problem_count
  from public.research_whoqol_items w
  where (select count(*) from jsonb_object_keys(w.payload)) <> 52
     or exists (
       select 1
       from jsonb_each_text(w.payload) item
       where item.value::integer not between 1 and 5
     );
  if problem_count > 0 then
    raise exception 'Hay % registros WHOQOL-BREF incompletos o fuera de rango.', problem_count;
  end if;

  if (select count(*) from public.research_participants where group_type = 'Experimental') <> 281
     or (select count(*) from public.research_participants where group_type = 'Control') <> 281 then
    raise exception 'La distribución experimental/control no es 281/281.';
  end if;

  if (select count(distinct case_id) from public.conversation_messages_supplemental) <> 6463
     or (select count(distinct session_scope_id) from public.conversation_messages_supplemental) <> 6463 then
    raise exception 'El total de sesiones conversacionales no es 6,463.';
  end if;

  if (select count(*) from public.conversation_messages_supplemental where speaker = 'user') <> 23835
     or (select count(*) from public.conversation_messages_supplemental where speaker = 'assistant') <> 23835 then
    raise exception 'La distribución de mensajes usuario/asistente no es 23,835/23,835.';
  end if;

  select count(*) into problem_count
  from (
    select lower(alias)
    from public.ng_profiles
    group by lower(alias)
    having count(*) > 1
  ) duplicate_aliases;
  if problem_count > 0 then
    raise exception 'Hay % alias de perfil repetidos.', problem_count;
  end if;

  select count(*) into problem_count
  from (
    select lower(caregiver_alias)
    from public.ng_families
    group by lower(caregiver_alias)
    having count(*) > 1
  ) duplicate_aliases;
  if problem_count > 0 then
    raise exception 'Hay % alias de cuidadores repetidos.', problem_count;
  end if;

  select count(*) into problem_count
  from public.ng_profiles
  where role in ('adolescente', 'hijo', 'hija')
    and school_profile is null;
  if problem_count > 0 then
    raise exception 'Hay % perfiles infantiles sin school_profile.', problem_count;
  end if;

  select count(*) into problem_count
  from public.ng_user_context_memory
  where not (
    (scope_type = 'family' and profile_id is null)
    or (scope_type = 'profile' and profile_id is not null)
  );
  if problem_count > 0 then
    raise exception 'Hay % memorias con alcance familiar/perfil incoherente.', problem_count;
  end if;

  select count(*) into problem_count
  from public.research_prepost
  where (
      group_type = 'Experimental'
      and (
        reported_sessions is null
        or reported_total_duration_min is null
        or reported_mean_session_duration_min is null
      )
    )
    or (
      group_type = 'Control'
      and (
        reported_sessions is not null
        or reported_total_duration_min is not null
        or reported_mean_session_duration_min is not null
      )
    );
  if problem_count > 0 then
    raise exception 'Hay % registros con nulos de uso incoherentes con el grupo.', problem_count;
  end if;

  select count(*) into problem_count
  from public.research_instruments instrument
  left join (
    select instrument_id, count(*)::double precision as documented_fields
    from public.research_instrument_items
    group by instrument_id
  ) item_count using (instrument_id)
  where coalesce(item_count.documented_fields, 0) <> instrument.items_or_fields;
  if problem_count > 0 then
    raise exception 'Hay % instrumentos con catálogo incompleto.', problem_count;
  end if;

  select count(*) into problem_count
  from (
    select m.profile_id, m.message_text as text_value
    from public.conversation_messages_supplemental m
    union all
    select m.profile_id, m.message
    from public.ng_messages m
    union all
    select c.profile_id, c.raw_input
    from public.ng_case_memory c
    union all
    select c.profile_id, c.input_summary_json::text
    from public.ng_conversation_curation c
    union all
    select c.profile_id, c.metadata_json::text
    from public.ng_conversation_curation c
  ) text_source
  join public.ng_profiles p using (profile_id)
  where text_source.text_value ~
    '(Iker|Mateo|Diego|Ximena|Valeria|Bruno|Santiago|Damián|Camila|Renata|Gael|Samuel|Regina|Paula|Luna)'
    and position(p.alias in text_source.text_value) = 0;
  if problem_count > 0 then
    raise exception 'Hay % textos con seudónimo distinto al perfil relacionado.', problem_count;
  end if;

  if (
    select count(*)
    from public.app_meta
    where meta_key in (
      'schema_version',
      'created_by',
      'data_provenance',
      'canonical_source_policy',
      'profile_alias_policy',
      'null_semantics_policy'
    )
  ) <> 6 then
    raise exception 'Los metadatos estructurales están incompletos.';
  end if;
end
$$;

select
  e.table_name,
  e.expected_rows,
  a.actual_rows,
  case when e.expected_rows = a.actual_rows then 'OK' else 'REVISAR' end as status
from expected_counts e
join actual_counts a using (table_name)
order by e.table_name;

select
  'VALIDACIÓN COMPLETA' as result,
  562 as participants,
  281 as experimental,
  281 as control,
  6463 as sessions,
  47670 as messages,
  619 as unique_profile_aliases,
  92 as documented_instrument_fields;

commit;
