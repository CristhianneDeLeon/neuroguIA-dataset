# Changelog

Este archivo documenta cambios relevantes del repositorio público
**neuroguIA Dataset**.

La rama `main` puede recibir correcciones documentales y metodológicas sin implicar
necesariamente una nueva publicación archivada o un nuevo número de versión.

---

## [Armonización del repositorio público] — 2026-08-11

**No corresponde a una nueva versión 3.0.0 ni a un nuevo release archivado.**

Se armonizó el estado público del repositorio con las decisiones metodológicas y
analíticas finales de la tesis.

### Privacidad y alcance público

Se retiraron del estado público archivos con granularidad individual u operacional que
no son necesarios para verificar los resultados científicos, incluyendo:

- bases individuales pretest/postest;
- respuestas WHOQOL por participante;
- perfiles, memorias y mensajes fila por fila;
- métricas individuales de uso;
- corpus conversacional operacional;
- archivos de migración que requieren las fuentes restringidas.

La carpeta pública `02_SUPABASE` dejó de presentarse como un respaldo restaurable de la
base operacional.

### Temporalidad

Se fijó como criterio canónico:

- semana preparatoria: 5–11 de enero de 2026;
- intervención activa: **18 semanas**, 12 de enero–17 de mayo de 2026;
- postest/cierre: 18–21 de mayo de 2026.

La ventana experimental contiene **1,325 sesiones y 10,212 mensajes**.

El corpus técnico completo contiene **6,463 sesiones y 47,670 mensajes**.

### Resultados socioemocionales

Se armonizaron las salidas públicas con los resultados auditados:

- estrés experimental: 17.89→12.46;
- ansiedad experimental: 12.82→8.83;
- depresión experimental: 12.52→8.81;
- MSPSS oficial experimental: 2.69→4.48;
- MSPSS oficial control: 2.69→2.73.

MSPSS e índice auxiliar de apoyo quedaron explícitamente separados.

### Estadística

La especificación inferencial pública se documentó como:

`postest ~ grupo + pretest`

con errores estándar robustos **HC3**.

Se actualizaron:

- ANCOVA;
- tamaños del efecto;
- pruebas no paramétricas;
- correlaciones;
- regresión de uso;
- WHOQOL-BREF;
- controles de calidad y trazabilidad.

### Uso y dosis–respuesta

Se corrigieron las referencias de exposición. Dentro del grupo experimental:

- mensajes vs mejoría de estrés: ρ=0.021, p=0.728;
- semanas activas vs mejoría de estrés: ρ=0.002, p=0.975.

No se interpreta una relación dosis–respuesta simple significativa.

### PLN

Se diferenciaron formalmente:

- PLN histórico: 1,020 registros, 9 categorías, accuracy 0.93;
- PLN operativo: 6,463 registros, 7 categorías, accuracy técnica 1.0.

La segunda métrica se presenta como control técnico interno reproducible y no como
validación humana externa.

### Reproducibilidad

La carpeta `analysis/` fue modificada para validar los **resultados agregados públicos**
sin exigir que la base individual permanezca en GitHub.

### Documentación raíz

Se actualizaron:

- `README.md`;
- `VARIABLE_DICTIONARY.md`;
- `DATA_SCHEMA.md`;
- `CITATION.cff`;
- `requirements.txt`;
- `.gitignore`.

El archivo `schema_supabase.sql` deja de formar parte del estado público vigente porque
el repositorio ya no distribuye una reconstrucción completa de la base operacional.

---

## Publicación archivada v2.0.0 — 2026-08

La publicación v2.0.0 permanece como **instantánea histórica archivada**.

- DOI específico: https://doi.org/10.5281/zenodo.21755820
- DOI conceptual: https://doi.org/10.5281/zenodo.20337422

El contenido de la rama `main` fue posteriormente armonizado. Por ello, el DOI
específico v2.0.0 debe utilizarse únicamente cuando se desea citar o reproducir esa
instantánea archivada.

---

## Publicación inicial — 2026-05

La primera publicación estructuró los recursos iniciales de datos, documentación,
validación y arquitectura conversacional utilizados durante el desarrollo del proyecto.

El historial detallado de commits de Git conserva la evolución técnica del repositorio.
