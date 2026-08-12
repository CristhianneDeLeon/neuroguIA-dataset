# Validación técnica y alcance público de Supabase

**Proyecto:** neuroguIA  
**Responsable de datos:** Cristhianne De León  
**Actualización documental:** 11 de agosto de 2026

## Alcance

Supabase/PostgreSQL constituye la capa de persistencia utilizada por neuroguIA para
perfiles, mensajes, memorias contextuales, casos, respuestas y rutinas. La validación
operacional completa se realizó sobre la infraestructura controlada del proyecto.

La carpeta pública `02_SUPABASE` **ya no distribuye una reconstrucción completa de la
base operacional**. Esta decisión reduce la exposición de información granular y evita
publicar identificadores, memorias y conversaciones que no son necesarios para verificar
los resultados científicos.

## Evidencia técnica conservada públicamente

La documentación pública permite verificar:

- metadatos y políticas canónicas;
- catálogo de instrumentos;
- estructura pública de instrumentos;
- resultados agregados e inferenciales;
- procedencia de las principales áreas de evidencia;
- reglas de transformación y publicación.

## Magnitudes técnicas auditadas

| Indicador | Resultado |
|---|---:|
| Participantes | 562 |
| Experimental | 281 |
| Control | 281 |
| Familias analíticas | 281 |
| Sesiones técnicas | 6,463 |
| Mensajes técnicos | 47,670 |
| Duración técnica media | 6.38 min |
| Sesiones en ventana experimental | 1,325 |
| Mensajes en ventana experimental | 10,212 |
| Duración de la intervención | 18 semanas |

La ventana experimental comprende del **12 de enero al 17 de mayo de 2026**. El
postest/cierre se documenta del 18 al 21 de mayo de 2026.

## Resultados socioemocionales de referencia

- DASS-21 estrés experimental: 17.89 → 12.46.
- DASS-21 ansiedad experimental: 12.82 → 8.83.
- DASS-21 depresión experimental: 12.52 → 8.81.
- MSPSS oficial experimental: 2.69 → 4.48.
- MSPSS oficial control: 2.69 → 2.73.

El índice auxiliar individual de apoyo se conserva como una medida secundaria y no
se interpreta como MSPSS.

## Seguridad y privacidad

El repositorio público no incluye:

- UUID o crosswalks de identidad analítica;
- perfiles individuales;
- mensajes o conversaciones fila por fila;
- memorias contextuales;
- rutinas asociadas a familias o perfiles;
- respuestas individuales pretest/postest;
- corpus conversacional operacional completo.

La reproducibilidad científica se sostiene mediante resultados agregados, reglas de
transformación, scripts analíticos y documentación de trazabilidad, no mediante la
publicación de la base operacional completa.
