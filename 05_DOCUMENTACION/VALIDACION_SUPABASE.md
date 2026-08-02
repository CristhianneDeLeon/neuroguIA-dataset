# Validación técnica de Supabase

Fecha: 2026-07-24
Responsable de datos: Cristhianne De León

La ruta de migración incluida en `02_SUPABASE` fue ejecutada de principio a fin
en una instancia PostgreSQL aislada, utilizando los 19 CSV del paquete.

## Comprobaciones superadas

- Creación de las 19 tablas canónicas.
- Importación transaccional de todos los CSV.
- Conversión correcta de JSON, UUID, booleanos, fechas y valores numéricos.
- Claves primarias sin duplicados.
- 619 alias de perfiles y 281 alias de cuidadores únicos, sin distinguir
  mayúsculas y minúsculas.
- Menciones nominales conversacionales alineadas con el `profile_id`
  relacionado.
- Catálogo completo de ocho instrumentos con 92 reactivos o campos.
- Nulos restringidos a los casos no aplicables por grupo, rol o alcance.
- Cero relaciones huérfanas en familias, perfiles, sesiones, mensajes,
  participantes e instrumentos.
- Resguardo administrativo de 39 registros operativos adicionales,
  expresamente marcados como no elegibles para análisis.
- Validación exacta de 281 participantes experimentales y 281 de comparación.
- Creación y consulta de diez vistas para dashboard.
- Habilitación de RLS en todas las tablas canónicas.
- Retiro de privilegios directos para `anon` y `authenticated`.
- Acceso reservado al backend mediante `service_role`.

## Resultados reproducidos desde las vistas

| Indicador | Resultado |
|---|---:|
| Participantes | 562 |
| Grupo experimental | 281 |
| Grupo de comparación | 281 |
| Unidades familiares de investigación | 281 |
| Familias operativas | 281 |
| Perfiles operativos | 619 |
| Sesiones | 6,463 |
| Mensajes | 47,670 |
| Registros operativos fuera del corpus analítico | 39 |
| Mensajes de usuario | 23,835 |
| Mensajes del asistente | 23,835 |
| Duración media de sesión | 6.38 min |
| Sesiones de más de 10 minutos | 2,092 |

## Resultados pretest–postest

| Grupo | Estrés | Ansiedad | Depresión | Apoyo 1–5 |
|---|---:|---:|---:|---:|
| Experimental | 17.89 → 12.46 | 12.82 → 8.83 | 12.52 → 8.81 | 2.69 → 3.40 |
| Comparación | 17.98 → 18.16 | 12.83 → 12.95 | 12.53 → 12.63 | 2.69 → 2.73 |

Las vistas no almacenan cifras manuales: calculan los indicadores directamente
desde las tablas canónicas. WHOQOL-BREF se conserva como base independiente y
se resume por grupo y dominio en escala 0–100.
