# Supabase — documentación pública de neuroguIA

Esta carpeta conserva únicamente los **metadatos, catálogos y resultados agregados**
necesarios para documentar la procedencia y reproducibilidad de la investigación
asociada con neuroguIA.

## Alcance público

El repositorio público **no constituye un respaldo restaurable de Supabase** y no
incluye la base operacional completa.

Por protección de los participantes y por consistencia metodológica, permanecen
fuera del repositorio público:

- identificadores y cruces entre participantes, familias, perfiles y UUID;
- perfiles y memorias contextuales;
- mensajes y conversaciones fila por fila;
- rutinas asociadas a familias o perfiles;
- puntuaciones individuales pretest/postest;
- respuestas individuales de WHOQOL-BREF;
- métricas individuales de exposición y uso;
- corpus conversacional operacional;
- archivos de migración que requieren esas fuentes restringidas.

## Archivos públicos de esta carpeta

- `01_app_meta.csv` — metadatos y políticas canónicas del repositorio.
- `15_research_instruments.csv` — catálogo público de instrumentos y medidas.
- `16_research_instrument_items.csv` — estructura metodológica pública de los instrumentos.
- `17_research_analysis_results.csv` — resultados agregados e inferenciales auditados.
- `18_research_provenance.csv` — procedencia de las principales áreas de evidencia.
- `19_research_transformations.csv` — transformaciones analíticas y reglas de publicación.

## Parámetros canónicos del estudio

- Participantes: **562**.
- Grupo experimental: **281**.
- Grupo control: **281**.
- Intervención activa: **18 semanas**.
- Periodo activo: **12 de enero a 17 de mayo de 2026**.
- Ventana experimental: **1,325 sesiones y 10,212 mensajes**.
- Corpus técnico completo: **6,463 sesiones y 47,670 mensajes**.

La ventana experimental y el corpus técnico completo se reportan como niveles
de evidencia distintos y no deben mezclarse.

## Fuente analítica

Los archivos públicos de esta carpeta se derivan de la **fuente analítica auditada**
utilizada para la tesis y se publican en forma agregada o metodológica.

La base individual auditada permanece bajo control de acceso y no forma parte del
repositorio público.

## Repositorios y accesos

- Repositorio de datos:
  https://github.com/CristhianneDeLeon/neuroguIA-dataset
- Repositorio de código:
  https://github.com/CristhianneDeLeon/neuroguIA-conversational-ai
- Plataforma conversacional:
  https://neuroguia-ai.streamlit.app/
- Dashboard científico:
  https://neuroguia-conversational-ai-dashboard.streamlit.app/

## Nota de reproducibilidad

La reproducibilidad pública se apoya en resultados agregados, documentación de
procedencia, reglas de transformación, diccionario de variables y código de
análisis. La reconstrucción de la base operacional completa de Supabase requiere
fuentes restringidas y no se distribuye públicamente.
