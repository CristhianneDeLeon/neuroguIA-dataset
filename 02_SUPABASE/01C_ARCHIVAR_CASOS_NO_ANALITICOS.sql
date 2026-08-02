-- neuroguIA — resguardo de registros operativos fuera del corpus analítico
-- Requisito: haber ejecutado 01_RESPALDO_BASE_ACTUAL.sql y
-- 01B_VERIFICAR_CASOS_ADICIONALES.sql.
--
-- Este script no elimina ni modifica datos de public. Copia en el esquema
-- administrativo los 39 casos que no pertenecen al corpus canónico de 6,463
-- sesiones y los marca expresamente como no elegibles para análisis.

create schema if not exists neuroguia_admin;

create table if not exists neuroguia_admin.ng_case_memory_archive (
  case_id uuid primary key,
  source_backup_schema text not null,
  record_data jsonb not null,
  analysis_eligible boolean not null default false
    check (analysis_eligible = false),
  exclusion_reason text not null,
  archived_at timestamptz not null default now()
);

comment on table neuroguia_admin.ng_case_memory_archive is
  'Registros operativos conservados para trazabilidad y excluidos de los resultados de investigación.';

do $$
declare
  backup_name text;
  source_count bigint;
  archived_count bigint;
  unlinked_count bigint;
  linked_sequence_count bigint;
  stable_demo_count bigint;
  linked_case_ids text[] := array[
    '08b192a7-568f-4311-a421-784fcb4c2cb0',
    '0da9afab-e256-4b0c-970e-7143dc167e9b',
    '29c384ff-fb6b-4d9d-b3bf-29dcc1565d36',
    '39075fe9-c551-4b13-856a-737a2bd91abf',
    '6810ab14-3a4e-468b-bc37-269bdf86c584',
    'ad020f0f-fa9a-4c73-9599-48836911121e',
    'c4f31add-8e15-4ebe-ba34-942aa5b85dd5'
  ];
begin
  select backup_schema
  into backup_name
  from neuroguia_admin.migration_runs
  where backup_completed = true
  order by run_id desc
  limit 1;

  if backup_name is null then
    raise exception 'No existe un respaldo completo registrado.';
  end if;

  if to_regclass(format('%I.ng_case_memory', backup_name)) is null then
    raise exception 'El respaldo % no contiene ng_case_memory.', backup_name;
  end if;

  execute format(
    'select count(*)
       from %I.ng_case_memory
      where family_id is null
         or profile_id is null
         or case_id::text = any($1)',
    backup_name
  )
  into source_count
  using linked_case_ids;

  if source_count <> 39 then
    raise exception
      'Se esperaban 39 registros fuera del corpus y se encontraron %.',
      source_count;
  end if;

  execute format(
    'insert into neuroguia_admin.ng_case_memory_archive (
       case_id,
       source_backup_schema,
       record_data,
       analysis_eligible,
       exclusion_reason,
       archived_at
     )
     select
       src.case_id::uuid,
       %L,
       to_jsonb(src),
       false,
       case
         when src.family_id is null or src.profile_id is null
           then ''Sin vínculo verificable con perfil y familia del corpus canónico''
         else ''Secuencia operativa identificada fuera del corpus canónico''
       end,
       now()
     from %I.ng_case_memory src
     where src.family_id is null
        or src.profile_id is null
        or src.case_id::text = any($1)
     on conflict (case_id) do update
       set source_backup_schema = excluded.source_backup_schema,
           record_data = excluded.record_data,
           analysis_eligible = false,
           exclusion_reason = excluded.exclusion_reason,
           archived_at = excluded.archived_at',
    backup_name,
    backup_name
  )
  using linked_case_ids;

  select
    count(*),
    count(*) filter (
      where record_data ->> 'family_id' is null
         or record_data ->> 'profile_id' is null
    ),
    count(*) filter (
      where record_data ->> 'family_id' is not null
        and record_data ->> 'profile_id' is not null
    ),
    count(*) filter (
      where record_data -> 'tags' @> '["stable_demo"]'::jsonb
    )
  into
    archived_count,
    unlinked_count,
    linked_sequence_count,
    stable_demo_count
  from neuroguia_admin.ng_case_memory_archive
  where source_backup_schema = backup_name;

  if archived_count <> 39
     or unlinked_count <> 32
     or linked_sequence_count <> 7
     or stable_demo_count <> 33 then
    raise exception
      'Clasificación inesperada: total %, sin vínculo %, vinculados %, stable_demo %.',
      archived_count,
      unlinked_count,
      linked_sequence_count,
      stable_demo_count;
  end if;
end
$$;

revoke all on schema neuroguia_admin from public, anon, authenticated;
revoke all on table neuroguia_admin.ng_case_memory_archive
  from public, anon, authenticated;

with latest_backup as (
  select backup_schema
  from neuroguia_admin.migration_runs
  where backup_completed = true
  order by run_id desc
  limit 1
)
select
  a.source_backup_schema,
  count(*) as archived_nonresearch_cases,
  count(*) filter (
    where a.record_data ->> 'family_id' is null
       or a.record_data ->> 'profile_id' is null
  ) as cases_without_verified_link,
  count(*) filter (
    where a.record_data ->> 'family_id' is not null
      and a.record_data ->> 'profile_id' is not null
  ) as linked_operational_sequence,
  count(*) filter (
    where a.record_data -> 'tags' @> '["stable_demo"]'::jsonb
  ) as cases_marked_stable_demo,
  count(*) filter (where a.analysis_eligible) as analysis_eligible_cases,
  bool_and(not a.analysis_eligible) as archive_completed
from neuroguia_admin.ng_case_memory_archive a
join latest_backup b on b.backup_schema = a.source_backup_schema
group by a.source_backup_schema;
