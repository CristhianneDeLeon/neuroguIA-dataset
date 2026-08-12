# neuroguIA Dataset — Esquema de datos público

## Propósito

Este documento describe la **arquitectura pública del repositorio de investigación**.
No representa el esquema completo de la base operacional de neuroguIA.

La infraestructura de la aplicación utiliza PostgreSQL/Supabase y estructuras
contextuales persistentes, pero los registros individuales y conversacionales
necesarios para reconstruir esa base permanecen bajo acceso restringido.

---

## 1. Arquitectura pública del repositorio

```text
01_INSTRUMENTOS_Y_FUENTES
    ↓ documentación de instrumentos
02_SUPABASE
    ↓ metadatos + procedencia + transformaciones + resultados agregados
03_ANALISIS
    ↓ resultados descriptivos e inferenciales
04_DASHBOARD
    ↓ fuentes agregadas para visualización
05_DOCUMENTACION
    ↓ calidad + diccionario + manifiestos + reglas de reporte
analysis
    ↓ código de validación de las salidas públicas
```

---

## 2. Unidades de análisis

| Unidad | Valor / función |
|---|---|
| Participante | 562 |
| Grupo experimental | 281 |
| Grupo control | 281 |
| Familia analítica | 281 |
| Ventana experimental | 18 semanas |
| Sesiones activas | 1,325 |
| Mensajes activos | 10,212 |
| Sesiones técnicas | 6,463 |
| Mensajes técnicos | 47,670 |

---

## 3. `01_INSTRUMENTOS_Y_FUENTES`

Contiene documentos metodológicos sin matrices individuales de respuestas.

Incluye:

- consentimiento informado;
- ficha sociodemográfica;
- DASS-21 contextualizado;
- instrumentos complementarios de experiencia;
- documentos pretest/postest.

Las bases individuales utilizadas durante el análisis no forman parte del estado
público actual.

---

## 4. `02_SUPABASE`

La carpeta pública conserva una **representación documental**, no una migración
restaurable.

Archivos principales:

- `01_app_meta.csv`
- `15_research_instruments.csv`
- `16_research_instrument_items.csv`
- `17_research_analysis_results.csv`
- `18_research_provenance.csv`
- `19_research_transformations.csv`

No se distribuyen públicamente perfiles, familias, mensajes, memorias, rutinas,
crosswalks ni tablas individuales de investigación.

---

## 5. `03_ANALISIS`

### Resultados psicométricos

- `prepost_summary.csv`
- `mspss_summary.csv`
- `whoqol_summary.csv`
- `experience_use_summary.csv`

### Inferencia

- `ancova_hc3.csv`
- `effect_sizes.csv`
- `nonparametric_effects.csv`
- `usage_correlations.csv`
- `usage_regression.csv`
- `whoqol_ancova.csv`

### Uso y temporalidad

- `sample_summary.csv`
- `usage_summary.csv`
- `weekly_distribution.csv`
- `time_band_distribution.csv`

### PLN

- `nlp_metrics_historical.csv`
- `nlp_metrics.csv`
- `nlp_confusion_matrix.csv`
- `category_distribution.csv`

### Calidad y soporte

- `relational_integrity.csv`
- `data_quality_log.csv`
- `data_dictionary.csv`
- `dashboard_kpis.csv`

---

## 6. `04_DASHBOARD`

Contiene fuentes agregadas utilizadas para consulta y visualización:

- `dashboard_kpis.csv`
- `dashboard_prepost.csv`
- `dashboard_weeks.csv`
- `dashboard_categories.csv`
- `dashboard_states.csv`
- `dashboard_time_bands.csv`
- `dashboard_whoqol.csv`
- `NeuroGuIA_Concentrado_Publico.xlsx`

El concentrado público no contiene filas individuales.

---

## 7. `05_DOCUMENTACION`

Integra:

- control de calidad;
- declaración de procedencia;
- diccionario de datos;
- huellas y manifiestos SHA-256;
- transformaciones;
- criterios de reporte;
- documentación de alcance público de Supabase.

---

## 8. `analysis`

El código público valida:

1. referencias canónicas;
2. consistencia entre archivos;
3. fórmulas reproducibles;
4. suma de semanas y categorías;
5. concordancia entre análisis y dashboard.

Las reestimaciones que requieren filas individuales se realizan en la fuente restringida
y se publican únicamente como salidas agregadas.

---

## 9. Arquitectura operacional restringida

La aplicación neuroguIA utiliza estructuras persistentes para perfiles, familias,
mensajes, memoria contextual, memoria de caso, memoria de respuesta y rutinas.

Esas estructuras se documentan conceptualmente en la tesis y en el repositorio de
código, pero **sus registros fila por fila no se distribuyen en este repositorio de datos**.

Esta separación evita confundir:

- arquitectura de software;
- base operacional;
- muestra analítica;
- corpus técnico;
- y resultados públicos de investigación.
