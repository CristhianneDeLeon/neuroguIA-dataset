# 03_ANALISIS — resultados públicos y reproducibles de neuroguIA

Esta carpeta contiene **resultados agregados, salidas inferenciales y métricas técnicas**
utilizadas para documentar los resultados de la investigación.

La carpeta pública no incluye bases individuales, respuestas por participante,
identificadores, UUID, mensajes fila por fila ni el corpus conversacional operacional.

## Parámetros canónicos

- Participantes: **562**.
- Grupo experimental: **281**.
- Grupo control: **281**.
- Familias analíticas: **281**.
- Intervención activa: **18 semanas**.
- Periodo activo: **12 de enero a 17 de mayo de 2026**.
- Postest/cierre: **18 a 21 de mayo de 2026**.
- Uso en ventana experimental: **1,325 sesiones y 10,212 mensajes**.
- Corpus técnico completo: **6,463 sesiones y 47,670 mensajes**.
- Duración técnica promedio de sesión: **6.38 min**.

## Resultados psicométricos principales

### DASS-21
En el grupo experimental:
- Estrés: 17.89 → 12.46; reducción relativa 30.36%.
- Ansiedad: 12.82 → 8.83; reducción relativa 31.11%.
- Depresión: 12.52 → 8.81; reducción relativa 29.65%.

### MSPSS
Resultado oficial agregado:
- Experimental: 2.69 → 4.48.
- Control: 2.69 → 2.73.

El MSPSS se mantiene metodológicamente separado del **índice auxiliar de apoyo**.

### WHOQOL-BREF
Se publican resultados agregados por dominio y un índice global descriptivo.
Las respuestas y puntuaciones individuales permanecen fuera del repositorio público.

## Análisis inferencial

- ANCOVA: postest ~ grupo + pretest.
- Errores estándar robustos **HC3**.
- Tamaños del efecto postest.
- Pruebas no paramétricas complementarias.
- Correlaciones de Spearman y regresión de uso.

Dentro del grupo experimental **no se identificó una relación dosis–respuesta simple**
entre el número de mensajes o las semanas activas y la mejoría del estrés.

## PLN

Se mantienen dos capas distintas:

1. **PLN histórico**: 1,020 registros, 9 categorías, accuracy 0.93.
2. **PLN operativo**: 6,463 registros, 7 categorías y accuracy técnica 1.0 en un
   holdout agrupado por familia. Esta segunda métrica se interpreta como control técnico
   reproducible, no como validación humana externa.

## Privacidad

Los archivos públicos de esta carpeta son agregados. No se distribuyen:
- bases pre/post individuales;
- respuestas WHOQOL por persona;
- métricas individuales de uso;
- corpus conversacional fila por fila;
- textos de conversaciones;
- crosswalks o identificadores operativos.

## Fuente analítica

Resultados derivados de la fuente analítica auditada utilizada en la tesis de neuroguIA.
