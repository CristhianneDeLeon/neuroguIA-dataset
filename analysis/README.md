# Reproducibilidad de resultados — neuroguIA

Este directorio separa la **capa analítica** de la interfaz de Streamlit. Su propósito es responder con precisión a la pregunta:

> ¿En qué parte del código se aplican las fórmulas que producen los resultados mostrados en el dashboard?

La respuesta pasa a ser directa:

- `analysis/formulas_neuroguia.py`: contiene las fórmulas.
- `analysis/reproducir_resultados.py`: aplica las fórmulas al archivo maestro.
- `analysis/referencias_dashboard.csv`: registra los valores oficiales contra los que se valida la ejecución.
- `analysis/tests/`: comprueba que las funciones esenciales operan correctamente.
- `outputs/reproducibilidad/`: conserva las tablas obtenidas y un manifiesto con el hash del archivo analizado.

## Fórmulas implementadas

El módulo incluye:

- cambio absoluto pretest–postest;
- reducción porcentual para estrés, ansiedad y depresión;
- incremento porcentual para apoyo social y calidad de vida;
- diferencia postest entre grupo experimental y control;
- desviación estándar combinada;
- Cohen’s d;
- Shapiro-Wilk;
- t de Student para muestras relacionadas e independientes;
- Wilcoxon;
- U de Mann-Whitney;
- r de Rosenthal;
- correlaciones de Spearman y Pearson;
- accuracy, precision, recall, F1 macro, ROC-AUC y error de clasificación;
- similitud coseno;
- regresión lineal múltiple con R², R² ajustado, F y p global.

## Ubicación recomendada

Copiar la carpeta `analysis` en el repositorio:

```text
neuroguIA-dataset/
├── analysis/
│   ├── formulas_neuroguia.py
│   ├── reproducir_resultados.py
│   ├── referencias_dashboard.csv
│   ├── requirements.txt
│   └── tests/
├── data/
└── outputs/
```

Este repositorio es el lugar adecuado porque el código reproduce resultados derivados del dataset publicado. El dashboard puede seguir en su repositorio independiente.

## Instalación

Desde la raíz de `neuroguIA-dataset`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r analysis\requirements.txt
```

## Ejecución

```powershell
python analysis\reproducir_resultados.py `
  --input "data\neuroguIA_concentrado_maestro_trazable.xlsx" `
  --output "outputs\reproducibilidad"
```

Para detener la publicación cuando existan diferencias frente al dashboard:

```powershell
python analysis\reproducir_resultados.py `
  --input "data\neuroguIA_concentrado_maestro_trazable.xlsx" `
  --output "outputs\reproducibilidad" `
  --strict
```

El modo `--strict` devuelve código de salida 2 si algún resultado calculable no coincide con las referencias oficiales.

## Pruebas

```powershell
python -m pytest analysis\tests -q
```

## Archivos de salida

La ejecución puede generar:

```text
00_catalogo_formulas.csv
01_resultados_prepost_reproducidos.csv
02_pruebas_inferenciales_reproducidas.csv
03_comparacion_postest_grupos.csv
04_contraste_hipotesis.csv
05_correlaciones_spearman.csv
06_modelo_regresion.csv
07_metricas_clasificador.csv
08_validacion_referencias_dashboard.csv
manifest.json
```

El `manifest.json` registra la ruta y el SHA-256 del archivo de entrada, las hojas detectadas y las versiones de las librerías.

## Decisión explícita sobre Cohen’s d

En una versión textual de la tesis aparece `×100` junto a la fórmula de Cohen’s d. El código **no multiplica d por 100**, porque:

1. Cohen’s d es adimensional.
2. Los criterios de interpretación usados en la tesis son aproximadamente 0.20, 0.50 y 0.80.
3. Multiplicarlo por 100 impediría reproducir esa escala.

La decisión queda documentada en el código y en este README para evitar una corrección silenciosa.

## Advertencia de trazabilidad

El script no fuerza los resultados para que coincidan. Calcula lo que contiene el archivo de entrada y después lo compara con `referencias_dashboard.csv`.

Esto es importante porque un archivo maestro antiguo, una copia de trabajo o una consolidación operativa pueden contener cifras distintas a la capa oficial del Capítulo 6. En ese caso, `08_validacion_referencias_dashboard.csv` mostrará `DIFIERE`.

No deben ajustarse los datos para “hacerlos coincidir”. Primero se identifica cuál es el archivo oficial que originó las cifras publicadas.
