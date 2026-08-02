# Carga de los CSV

La carga automatizada se realiza con `03_CARGAR_CSV.psql`. Este método evita
importar manualmente los 19 archivos uno por uno.

## Opción recomendada: psql

1. Abra la carpeta `02_SUPABASE` en una terminal.
2. Copie desde Supabase la cadena de conexión de **Session pooler**.
3. Ejecute:

   ```bash
   psql "CADENA_DE_CONEXION" -f 03_CARGAR_CSV.psql
   ```

4. No escriba la contraseña dentro de ningún archivo del paquete.
5. Si ocurre un error, `ON_ERROR_STOP` interrumpe la ejecución y la transacción
   no queda publicada.

## Alternativa desde Table Editor

Abra cada tabla en Supabase, seleccione **Insert > Import Data from CSV** e
importe los archivos en orden numérico, del `01_app_meta.csv` al
`19_research_transformations.csv`.

Las tablas `ng_messages` y `research_analysis_results` incluyen una clave
interna autogenerada. En esas dos importaciones, relacione únicamente las
columnas que aparecen en el CSV.

Al terminar, ejecute `04_VALIDAR_CARGA.sql` en SQL Editor. No habilite el acceso
de la aplicación antes de completar también las vistas y la seguridad RLS.
