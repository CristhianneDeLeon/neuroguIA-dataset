# Datos de investigación de neuroguIA

**Responsable:** Cristhianne De León  
**ORCID:** https://orcid.org/0009-0007-4777-1741  
**Última armonización documental:** 11 de agosto de 2026

Este repositorio reúne los **resultados públicos agregados, instrumentos, recursos de
reproducibilidad, fuentes para dashboard y documentación metodológica** asociados con
la investigación de neuroguIA.

El repositorio público **no constituye un respaldo restaurable de Supabase** ni
distribuye la base individual utilizada para los análisis.

## Accesos públicos

- Plataforma conversacional: https://neuroguia-ai.streamlit.app/
- Dashboard científico: https://neuroguia-conversational-ai-dashboard.streamlit.app/
- Código de la aplicación: https://github.com/CristhianneDeLeon/neuroguIA-conversational-ai
- Repositorio de datos: https://github.com/CristhianneDeLeon/neuroguIA-dataset
- ORCID: https://orcid.org/0009-0007-4777-1741

## Parámetros canónicos del estudio

| Indicador | Valor |
|---|---:|
| Participantes | 562 |
| Grupo experimental | 281 |
| Grupo control | 281 |
| Familias analíticas | 281 |
| Intervención activa | 18 semanas |
| Periodo activo | 12-ene-2026 a 17-may-2026 |
| Postest/cierre | 18-may-2026 a 21-may-2026 |
| Sesiones en ventana experimental | 1,325 |
| Mensajes en ventana experimental | 10,212 |
| Sesiones técnicas totales | 6,463 |
| Mensajes técnicos totales | 47,670 |
| Duración técnica media de sesión | 6.38 min |

La **ventana experimental** y el **corpus técnico completo** son universos distintos y
se reportan por separado.

## Resultados principales

### DASS-21

En el grupo experimental:

- Estrés: **17.89 → 12.46**; reducción relativa **30.36%**.
- Ansiedad: **12.82 → 8.83**; reducción relativa **31.11%**.
- Depresión: **12.52 → 8.81**; reducción relativa **29.65%**.

La especificación inferencial final utiliza ANCOVA:

`postest ~ grupo + pretest`

con errores estándar robustos **HC3**.

### MSPSS

Resultado oficial agregado:

- Experimental: **2.69 → 4.48**.
- Control: **2.69 → 2.73**.

El MSPSS se mantiene metodológicamente separado del **índice auxiliar de apoyo** usado
en análisis secundarios.

### WHOQOL-BREF

Se publican resultados agregados para los cuatro dominios oficiales:

- físico;
- psicológico;
- relaciones sociales;
- entorno.

El promedio global se conserva únicamente como **indicador descriptivo**.

### Uso y relación dosis–respuesta

Dentro del grupo experimental no se observó una asociación simple significativa entre
la mejoría del estrés y:

- número de mensajes: **ρ = 0.021; p = 0.728**;
- semanas activas: **ρ = 0.002; p = 0.975**.

### PLN

Se mantienen dos capas distintas de evidencia:

- **PLN histórico:** 1,020 registros, 9 categorías, accuracy 0.93, F1 macro 0.931,
  ROC-AUC 0.95.
- **PLN operativo:** 6,463 registros, 7 categorías y accuracy técnica 1.0 en un
  control interno reproducible.

La métrica operativa se interpreta como **control técnico interno**, no como validación
humana externa.

## Estructura pública del repositorio

```text
neuroguIA-dataset/
├── 01_INSTRUMENTOS_Y_FUENTES/
│   └── instrumentos y documentos metodológicos sin respuestas individuales
│
├── 02_SUPABASE/
│   └── metadatos, instrumentos, resultados agregados, procedencia y transformaciones
│
├── 03_ANALISIS/
│   └── resultados descriptivos, inferenciales, uso y métricas PLN
│
├── 04_DASHBOARD/
│   └── fuentes agregadas para visualización científica
│
├── 05_DOCUMENTACION/
│   └── calidad, trazabilidad, diccionario, manifiestos y criterios de reporte
│
└── analysis/
    └── código para validar las salidas públicas agregadas
```

## Privacidad y alcance público

No se distribuyen públicamente:

- nombres ni identificadores directos;
- crosswalks entre códigos;
- UUID vinculables a participantes o familias;
- perfiles individuales;
- respuestas pretest/postest individuales;
- respuestas WHOQOL por reactivo;
- mensajes o conversaciones fila por fila;
- memorias contextuales;
- rutinas asociadas a perfiles;
- métricas individuales de uso;
- corpus conversacional operacional completo;
- el Documento Maestro individual auditado.

La reproducibilidad pública se sostiene mediante **resultados agregados, documentación
de procedencia, transformaciones, controles de calidad y código de validación**.

## Reproducibilidad

Instalación:

```bash
python -m pip install -r requirements.txt
```

Validación:

```bash
python -m pytest analysis/tests -q
python analysis/reproducir_resultados.py   --analysis-dir 03_ANALISIS   --dashboard-dir 04_DASHBOARD   --output outputs/reproducibilidad   --strict
```

La validación pública contrasta los archivos agregados entre sí y no requiere publicar
la base individual.

## Preservación histórica en Zenodo

El repositorio conserva referencias a una publicación archivada previa:

- DOI específico de la publicación archivada v2.0.0:
  https://doi.org/10.5281/zenodo.21755820
- DOI conceptual/general del conjunto:
  https://doi.org/10.5281/zenodo.20337422

**Importante:** el DOI específico de v2.0.0 identifica el contenido archivado de esa
publicación y no debe interpretarse como una huella exacta del estado actual de la rama
`main`, que posteriormente fue armonizada para corregir alcance público, privacidad,
temporalidad y resultados analíticos.

Para citar el **estado actual del repositorio**, utilice la URL de GitHub y la fecha de
consulta. Para reproducir específicamente la publicación archivada v2.0.0, utilice su
DOI específico.

## Licencia

Los materiales públicos de este repositorio se distribuyen bajo
**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

Consulte `LICENSE` para los términos.
