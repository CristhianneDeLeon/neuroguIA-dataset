# Datos de investigación de neuroguIA

Responsable: Cristhianne De León
Fecha de consolidación: 2026-08-01

Este paquete reúne las bases operativas, los resultados de investigación, los instrumentos y los archivos para dashboard.

## Regla central

- Los archivos de `01_INSTRUMENTOS_Y_FUENTES` conservan los instrumentos y bases de referencia.
- Los CSV de `02_SUPABASE` son las tablas listas para importación.
- Los archivos de `03_ANALISIS` contienen los resultados reproducibles.
- El concentrado de `04_DASHBOARD` reúne la información requerida para visualización.
- `05_DOCUMENTACION` conserva el diccionario, las fuentes y los controles de calidad.
- `05_DOCUMENTACION/NeuroGuIA_Instrumentos_Criterios_Reporte.docx` fija la denominación, puntuación y uso metodológico de cada instrumento.

## Supabase

La carpeta `02_SUPABASE` incluye una migración completa y ordenada:
diagnóstico, respaldo, archivo administrativo de registros no analíticos,
creación del esquema, carga automática de los 19 CSV, validación, vistas de
dashboard, seguridad RLS y verificación final.

Comience siempre por `02_SUPABASE/00_LEEME_PRIMERO.md`. La carga fue probada
de principio a fin con los 19 CSV y reproduce 562 participantes, 6,463 sesiones
y 47,670 mensajes. Además, valida 619 alias de perfiles únicos, 92 reactivos o
campos instrumentales y la semántica de los nulos no aplicables. Los 39 casos
operativos que no forman parte del corpus analítico se conservan por separado
en el esquema administrativo y no alimentan los indicadores.

## Fuentes canónicas

- Resultados pretest–postest: `evaluacion_prepost_neuroguIA.xlsx`.
- Participantes y variables descriptivas: `master_input_dataset.xlsx`.
- Operación conversacional: `ng_case_memory.csv` y `conversation_messages_supplemental_clean.csv`.
- WHOQOL-BREF: `whoqol_bref_prepost_dominios_neuroguIA.xlsx`.

Los registros conservan sus marcas temporales suministradas. Las columnas derivadas se identifican en el diccionario y en el registro de transformaciones.

## DOI y citación

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20337422.svg)](https://doi.org/10.5281/zenodo.20337422)

La versión consolidada del dataset se encuentra preservada en Zenodo:

- **Versión publicada:** `v2.0.0`
- **DOI específico de la versión:** [10.5281/zenodo.21755820](https://doi.org/10.5281/zenodo.21755820)
- **DOI general del conjunto:** [10.5281/zenodo.20337422](https://doi.org/10.5281/zenodo.20337422)
- **Tipo de recurso:** Dataset
- **Licencia:** CC BY-NC 4.0
- **Autora:** Cristhianne De León
- **ORCID:** [0009-0007-4777-1741](https://orcid.org/0009-0007-4777-1741)

Para investigaciones, publicaciones o análisis derivados, debe citarse el DOI específico de la versión utilizada.
