# Reproducibilidad pública de resultados — neuroguIA

La carpeta `analysis/` contiene el código utilizado para **validar las salidas públicas
agregadas** de neuroguIA y comprobar que las cifras publicadas en el repositorio sean
coherentes entre sí.

## Principio de diseño

La reproducibilidad pública **no requiere publicar la base individual**.

Por esta razón, el script actual trabaja sobre los CSV agregados de `03_ANALISIS`
y, cuando está disponible, contrasta también `04_DASHBOARD`. Las reestimaciones que
requieren registros individuales —por ejemplo, ANCOVA HC3 a partir de las observaciones
pre/post— se ejecutan en la fuente restringida y se publican únicamente como resultados
agregados.

## Estructura

```text
analysis/
├── formulas_neuroguia.py
├── reproducir_resultados.py
├── referencias_dashboard.csv
├── requirements.txt
└── tests/
    ├── test_formulas.py
    └── test_public_outputs.py
```

## Qué valida

- muestra final: 562 participantes, 281/281;
- intervención activa: 18 semanas, 12-ene-2026 a 17-may-2026;
- 1,325 sesiones y 10,212 mensajes en la ventana experimental;
- 6,463 sesiones y 47,670 mensajes del corpus técnico;
- DASS-21 pre/post;
- MSPSS oficial agregado 2.69→4.48 en experimental;
- ANCOVA con errores robustos HC3;
- tamaños del efecto;
- WHOQOL-BREF agregado;
- correlaciones y regresión de uso;
- PLN histórico y PLN operativo como capas distintas;
- coherencia entre categorías, franjas horarias y totales de sesiones.

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
  --analysis-dir 03_ANALISIS `
  --dashboard-dir 04_DASHBOARD `
  --output outputs\reproducibilidad `
  --strict
```

El modo `--strict` devuelve código de salida 2 cuando una referencia oficial o un
control de consistencia no coincide.

## Pruebas

```powershell
python -m pytest analysis\tests -q
```

## Salidas

```text
00_catalogo_formulas.csv
01_validacion_referencias.csv
02_validacion_consistencia.csv
manifest.json
```

## Nota sobre MSPSS

MSPSS y el índice auxiliar de apoyo son medidas distintas. El repositorio público
conserva MSPSS como resultado agregado oficial y no intenta reconstruir sus puntuaciones
individuales a partir del índice auxiliar.

## Nota sobre ANCOVA

La especificación final es:

`postest ~ grupo + pretest`

con errores estándar robustos **HC3**. La función `ancova_hc3()` está disponible en
`formulas_neuroguia.py` para ejecuciones sobre la fuente restringida.

## Privacidad

No son necesarios para esta capa pública:

- identificadores de participante;
- UUID;
- respuestas individuales;
- mensajes o conversaciones;
- memorias contextuales;
- corpus conversacional fila por fila.

La reproducción pública verifica cálculos derivados, referencias oficiales y
consistencia transversal sin exponer esa información.
