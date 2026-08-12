# 05_DOCUMENTACION — trazabilidad, calidad y criterios de publicación

Esta carpeta documenta la procedencia, control de calidad, transformaciones,
estructura de los datos públicos y criterios de reporte utilizados en neuroguIA.

## Alcance

El repositorio público contiene **resultados agregados y materiales reproducibles**.
No constituye una copia de la base individual ni un respaldo restaurable de la
infraestructura operacional de Supabase.

## Parámetros canónicos

- Participantes: **562**.
- Grupo experimental: **281**.
- Grupo control: **281**.
- Familias analíticas: **281**.
- Intervención activa: **18 semanas**, del 12 de enero al 17 de mayo de 2026.
- Ventana experimental: **1,325 sesiones y 10,212 mensajes**.
- Corpus técnico completo: **6,463 sesiones y 47,670 mensajes**.

## Medidas principales

- DASS-21: estrés como variable principal; ansiedad y depresión como dimensiones complementarias.
- MSPSS: resultado oficial agregado. Experimental 2.69→4.48; control 2.69→2.73.
- Índice auxiliar de apoyo: variable secundaria individual, separada conceptualmente de MSPSS.
- WHOQOL-BREF: cuatro dominios oficiales; el promedio global se utiliza solo como indicador descriptivo.
- Instrumentos de experiencia: EUA-neuroguIA/UTIL10, EEP-neuroguIA/APOYO10,
  EAPC-neuroguIA/EAPC12, PRE5 y POST5.

## Archivos de esta carpeta

- `CONTROL_CALIDAD.csv`: controles y decisiones metodológicas.
- `DECLARACION_PROCEDENCIA_DATOS.md`: procedencia, custodia y alcance público.
- `DICCIONARIO_DATOS.csv`: diccionario de las principales salidas públicas.
- `FUENTES_Y_HUELLAS.csv`: fuentes públicas, roles y huellas cuando están disponibles.
- `MANIFIESTO_SHA256.csv`: manifiesto de integridad de las carpetas públicas 01–05.
- `NeuroGuIA_Instrumentos_Criterios_Reporte.docx`: matriz de instrumentos y reglas de reporte.
- `REGISTRO_TRANSFORMACIONES.csv`: transformaciones que conducen a las salidas públicas.
- `VALIDACION_SUPABASE.md`: alcance técnico y límites de la evidencia pública.

## Regla de privacidad

Permanecen fuera del repositorio público las bases individuales, respuestas por reactivo
cuando permiten reconstruir registros personales, identificadores, crosswalks, UUID,
mensajes, memorias, rutinas, corpus conversacional fila por fila y cualquier archivo
que incremente innecesariamente el riesgo de reidentificación.

## Fuente analítica

Las salidas se alinean con la fuente analítica auditada utilizada para la tesis y con
las decisiones canónicas documentadas en el proyecto.
