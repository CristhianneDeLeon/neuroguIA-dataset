# Migración de Supabase — neuroguIA

Esta carpeta contiene una ruta única para alinear Supabase con las bases
canónicas de la investigación. No ejecute los scripts fuera de orden.

## Antes de comenzar

- Programe una ventana breve de mantenimiento para evitar escrituras durante la
  sustitución.
- Genere un respaldo del proyecto en **Database > Backups**. Si su plan no
  permite descargar respaldos, realice un volcado lógico con Supabase CLI.
- Ejecute `validar_csv_antes_de_carga.py`. El resultado debe decir
  `APTO PARA CARGA`.
- Guarde la cadena de conexión y la contraseña fuera de esta carpeta.

## Orden exacto

1. `00_DIAGNOSTICO_BASE_ACTUAL.sql` — SQL Editor, solo lectura.
2. `01_RESPALDO_BASE_ACTUAL.sql` — crea una copia interna fechada.
3. `01B_VERIFICAR_CASOS_ADICIONALES.sql` — compara los casos respaldados
   con los 6,463 casos del paquete, sin modificar la base.
4. `01C_ARCHIVAR_CASOS_NO_ANALITICOS.sql` — conserva los 39 registros
   operativos adicionales en el esquema administrativo y los excluye del
   análisis.
5. `02_CREAR_ESQUEMA.sql` — sustituye las tablas canónicas vacías.
6. `03_CARGAR_CSV.psql` — carga automática de los 19 CSV.
7. `04_VALIDAR_CARGA.sql` — cancela si los conteos o relaciones no cuadran.
8. `05_VISTAS_DASHBOARD.sql` — crea indicadores calculados.
9. `06_SEGURIDAD_RLS.sql` — restringe datos y vistas al backend.
10. `07_VERIFICACION_FINAL.sql` — confirma datos, vistas y seguridad.

Si no utiliza `psql`, siga `03_CARGAR_CSV_DESDE_PANEL.md`.

## Resultado esperado

- 562 participantes: 281 experimentales y 281 de comparación.
- 281 unidades familiares de investigación.
- 281 familias operativas y 619 perfiles.
- 6,463 sesiones y 47,670 mensajes.
- 39 registros operativos adicionales conservados fuera del corpus analítico:
  32 sin vínculo verificable y siete pertenecientes a una secuencia operativa.
- 8 instrumentos y 92 reactivos/campos documentados.
- 619 perfiles con alias anonimizados únicos y menciones nominales
  conversacionales alineadas mediante `profile_id`.
- Nulos conservados únicamente cuando el campo no aplica por grupo, rol o
  alcance de memoria.
- 562 registros WHOQOL-BREF, conservados como base independiente.
- Vistas de dashboard calculadas desde las tablas, sin cifras manuales.
- Tablas sensibles protegidas con RLS y sin acceso directo para
  `anon` o `authenticated`.

## Acceso de la plataforma

La configuración incluida supone que Streamlit usa `service_role` desde el
backend. La clave debe permanecer únicamente en los secretos del servidor.
Nunca debe incluirse en JavaScript, repositorios, capturas ni archivos de
entrega.
