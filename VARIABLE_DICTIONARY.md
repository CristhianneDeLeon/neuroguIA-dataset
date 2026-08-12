# neuroguIA Dataset — Diccionario de variables públicas

## Alcance

Este diccionario describe las principales variables de los **archivos públicos
agregados**. Los identificadores, perfiles y registros individuales de la base
operacional no forman parte del conjunto público actual.

Para el diccionario tabular completo consulte:

`05_DOCUMENTACION/DICCIONARIO_DATOS.csv`

---

## 1. Muestra y temporalidad

### `03_ANALISIS/sample_summary.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `indicator` | Texto | Parámetro de muestra o temporalidad |
| `value` | Mixto | Valor canónico |
| `unit` | Texto | Unidad |
| `note` | Texto | Nota metodológica |

Indicadores principales:

- `participants_total`
- `participants_experimental`
- `participants_control`
- `analytical_families`
- `active_intervention_weeks`
- fechas de preparación, intervención y cierre

---

## 2. DASS-21

### `03_ANALISIS/prepost_summary.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `outcome` | Texto | `stress`, `anxiety` o `depression` |
| `group_type` | Texto | Experimental o Control |
| `n` | Entero | Tamaño del grupo |
| `pre_mean` | Numérico | Media pretest |
| `pre_sd` | Numérico | DE pretest |
| `post_mean` | Numérico | Media postest |
| `post_sd` | Numérico | DE postest |
| `favorable_change_mean` | Numérico | Cambio expresado en dirección favorable |
| `favorable_change_percent` | Numérico | Cambio relativo favorable (%) |

Para DASS-21 una reducción se interpreta como cambio favorable.

---

## 3. MSPSS

### `03_ANALISIS/mspss_summary.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `measure` | Texto | Medida reportada |
| `group_type` | Texto | Experimental o Control |
| `n` | Entero | Tamaño del grupo |
| `pre_mean` | Numérico | Media oficial basal |
| `post_mean` | Numérico | Media oficial postest |
| `change_mean` | Numérico | Diferencia post-pre |
| `change_percent` | Numérico | Cambio porcentual oficial |
| `scale` | Texto | Escala utilizada |
| `note` | Texto | Nota metodológica |

MSPSS **no debe mezclarse** con el índice auxiliar de apoyo.

---

## 4. WHOQOL-BREF

### `03_ANALISIS/whoqol_summary.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `group_type` | Texto | Experimental o Control |
| `domain` | Texto | Físico, psicológico, relaciones, entorno o global descriptivo |
| `n` | Entero | Tamaño del grupo |
| `pre_mean` | Numérico | Media pretest |
| `pre_sd` | Numérico | DE pretest |
| `post_mean` | Numérico | Media postest |
| `post_sd` | Numérico | DE postest |
| `mean_change` | Numérico | Diferencia post-pre |
| `change_percent_group_means` | Numérico | Cambio porcentual entre medias |

`global_descriptive` no constituye un quinto dominio oficial.

---

## 5. ANCOVA

### `03_ANALISIS/ancova_hc3.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `instrument` | Texto | DASS21, APOYO_AUX o WHOQOL |
| `outcome` | Texto | Resultado analizado |
| `n` | Entero | Observaciones |
| `adjusted_group_difference` | Numérico | Diferencia ajustada Experimental-Control |
| `ci95_low` | Numérico | Límite inferior IC95% |
| `ci95_high` | Numérico | Límite superior IC95% |
| `p_group` | Texto/Numérico | Valor p |
| `r2` | Numérico | Coeficiente de determinación |
| `standard_error_method` | Texto | Método de error estándar; `HC3` |
| `interpretation_note` | Texto | Regla de interpretación |

---

## 6. Tamaños del efecto

### `03_ANALISIS/effect_sizes.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `instrument` | Texto | Instrumento |
| `outcome` | Texto | Resultado |
| `effect_definition` | Texto | Comparación representada |
| `effect_value` | Numérico | Tamaño del efecto |
| `effect_metric` | Texto | Métrica, p. ej. Cohen's d |
| `interpretation` | Texto | Nota de dirección |

---

## 7. Uso

### `03_ANALISIS/usage_summary.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `indicator` | Texto | Indicador de uso |
| `value` | Numérico | Valor |
| `unit` | Texto | Unidad |
| `scope` | Texto | Universo temporal |
| `note` | Texto | Delimitación metodológica |

Es esencial distinguir `active_window` de `technical_total`.

### `03_ANALISIS/weekly_distribution.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `week` | Entero | Semana activa 1–18 |
| `start_date` | Fecha | Inicio de semana |
| `end_date` | Fecha | Fin de semana |
| `sessions` | Entero | Sesiones en la semana |
| `period` | Texto | Ventana metodológica |

---

## 8. Correlaciones y regresión

### `03_ANALISIS/usage_correlations.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `sample` | Texto | Muestra analizada |
| `predictor` | Texto | Mensajes o semanas activas |
| `outcome` | Texto | Resultado |
| `spearman_rho` | Numérico | ρ de Spearman |
| `p_value` | Numérico | Valor p |
| `n` | Entero | Observaciones |
| `interpretation` | Texto | Interpretación |

### `03_ANALISIS/usage_regression.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `model` | Texto | Modelo |
| `predictor` | Texto | Predictor o estadístico de ajuste |
| `coefficient` | Numérico | Coeficiente / valor |
| `p_value` | Numérico | Valor p cuando corresponde |
| `significance` | Texto | Indicador descriptivo |
| `note` | Texto | Nota |

---

## 9. PLN

### `03_ANALISIS/nlp_metrics_historical.csv`

Resume la capa histórica de 1,020 registros y 9 categorías.

### `03_ANALISIS/nlp_metrics.csv`

Documenta el control técnico operativo con 6,463 registros y 7 categorías.

### `03_ANALISIS/category_distribution.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `category` | Texto | Categoría operativa |
| `sessions` | Entero | Sesiones clasificadas |
| `percent_sessions` | Numérico | Porcentaje de las 6,463 sesiones |

---

## 10. Dashboard

Los archivos `04_DASHBOARD/dashboard_*.csv` son vistas agregadas derivadas de las
salidas analíticas. No deben considerarse una fuente primaria independiente.

---

## 11. Variables restringidas

Quedan fuera del diccionario público fila por fila:

- `participant_id`;
- `family_id`;
- `profile_id`;
- UUID de sesiones/mensajes;
- textos conversacionales;
- respuestas individuales de instrumentos;
- crosswalks;
- memorias contextuales;
- rutinas vinculadas a perfiles.

Su existencia puede documentarse metodológicamente, pero sus valores no se distribuyen
en el repositorio público.
