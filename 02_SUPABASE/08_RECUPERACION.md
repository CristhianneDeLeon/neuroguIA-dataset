# Recuperación ante una incidencia

No continúe con la aplicación si `04_VALIDAR_CARGA.sql` o
`07_VERIFICACION_FINAL.sql` termina con una excepción.

La recuperación principal debe realizarse desde el respaldo del proyecto o
desde el volcado lógico creado antes de la migración. Supabase documenta la
restauración desde **Database > Backups** y, para respaldos manuales, mediante
Supabase CLI y `psql`.

`01_RESPALDO_BASE_ACTUAL.sql` crea además un esquema interno llamado
`neuroguia_respaldo_AAAAMMDD_HHMMSS`. Esa copia sirve para comparar o recuperar
registros puntuales, pero no sustituye el respaldo integral del proyecto,
porque una restauración completa también puede involucrar funciones, políticas,
roles, secretos, webhooks y configuración externa a estas tablas.

No elimine `neuroguia_admin` ni el esquema de respaldo hasta que:

1. La verificación final indique `MIGRACIÓN APROBADA`.
2. La plataforma pueda registrar y recuperar una conversación de prueba.
3. El dashboard reproduzca los KPI canónicos.
4. Se haya comprobado el acceso únicamente desde el backend autorizado.
