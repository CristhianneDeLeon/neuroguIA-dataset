# -*- coding: utf-8 -*-
"""Fórmulas estadísticas y computacionales utilizadas por neuroguIA.

Este módulo concentra las fórmulas para que los resultados no dependan de la
interfaz de Streamlit. Las funciones son deliberadamente pequeñas, auditables
y reutilizables.

Nota metodológica sobre Cohen's d
---------------------------------
En el texto de la tesis aparece una multiplicación por 100 junto a la fórmula
de Cohen's d. No se aplica aquí porque Cohen's d es una medida adimensional y
se interpreta con puntos de referencia aproximados de 0.20, 0.50 y 0.80.
El criterio queda documentado de manera explícita, no corregido en silencio.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.preprocessing import label_binarize


ALPHA_DEFAULT = 0.05


def _array(values: Iterable[float]) -> np.ndarray:
    arr = pd.to_numeric(pd.Series(list(values)), errors="coerce").dropna().to_numpy(dtype=float)
    if arr.size == 0:
        raise ValueError("No hay valores numéricos válidos.")
    return arr


def cambio_absoluto(pre: float, post: float) -> float:
    """ΔX = X_post - X_pre."""
    return float(post) - float(pre)


def cambio_porcentual_crudo(pre: float, post: float) -> float:
    """Cambio relativo con signo: ((post - pre) / pre) × 100."""
    pre = float(pre)
    if pre == 0:
        return float("nan")
    return ((float(post) - pre) / pre) * 100.0


def cambio_favorable_porcentual(pre: float, post: float, mejora: str) -> float:
    """Cambio favorable en una dirección común.

    mejora='disminuye':
        ((pre - post) / pre) × 100
        Para estrés, ansiedad y depresión.

    mejora='aumenta':
        ((post - pre) / pre) × 100
        Para apoyo social y calidad de vida.
    """
    pre = float(pre)
    if pre == 0:
        return float("nan")

    key = mejora.strip().lower()
    if key == "disminuye":
        return ((pre - float(post)) / pre) * 100.0
    if key == "aumenta":
        return ((float(post) - pre) / pre) * 100.0
    raise ValueError("mejora debe ser 'disminuye' o 'aumenta'.")


def diferencia_postest_grupos(post_experimental: float, post_control: float) -> float:
    """D_post = media_post_experimental - media_post_control."""
    return float(post_experimental) - float(post_control)


def desviacion_estandar_combinada(
    n1: int,
    sd1: float,
    n2: int,
    sd2: float,
) -> float:
    """s_p = sqrt(((n1−1)s1² + (n2−1)s2²) / (n1+n2−2))."""
    n1, n2 = int(n1), int(n2)
    if n1 < 2 or n2 < 2:
        return float("nan")
    denominator = n1 + n2 - 2
    numerator = (n1 - 1) * float(sd1) ** 2 + (n2 - 1) * float(sd2) ** 2
    return sqrt(numerator / denominator)


def cohen_d_independiente(
    media1: float,
    media2: float,
    sd1: float,
    sd2: float,
    n1: int,
    n2: int,
) -> float:
    """Cohen's d para dos grupos independientes con desviación combinada."""
    pooled = desviacion_estandar_combinada(n1, sd1, n2, sd2)
    if not np.isfinite(pooled) or pooled == 0:
        return float("nan")
    return (float(media1) - float(media2)) / pooled


def cohen_d_prepost_pooled(pre: Sequence[float], post: Sequence[float]) -> float:
    """Cohen's d pretest-postest con SD combinada, acorde con la tesis."""
    pre_arr, post_arr = _array(pre), _array(post)
    n = min(pre_arr.size, post_arr.size)
    pre_arr, post_arr = pre_arr[:n], post_arr[:n]
    pooled = desviacion_estandar_combinada(
        n,
        np.std(pre_arr, ddof=1),
        n,
        np.std(post_arr, ddof=1),
    )
    if not np.isfinite(pooled) or pooled == 0:
        return float("nan")
    return (np.mean(post_arr) - np.mean(pre_arr)) / pooled


def cohen_dz_pareado(pre: Sequence[float], post: Sequence[float]) -> float:
    """Cohen's dz complementario: media de diferencias / SD de diferencias."""
    pre_arr, post_arr = _paired_arrays(pre, post)
    differences = post_arr - pre_arr
    sd_diff = np.std(differences, ddof=1)
    if sd_diff == 0 or not np.isfinite(sd_diff):
        return float("nan")
    return float(np.mean(differences) / sd_diff)


def interpretar_cohen_d(value: float) -> str:
    """Interpretación por magnitud absoluta."""
    if not np.isfinite(value):
        return "No calculable"
    magnitude = abs(float(value))
    if magnitude < 0.20:
        return "Trivial o muy pequeño"
    if magnitude < 0.50:
        return "Pequeño"
    if magnitude < 0.80:
        return "Moderado"
    return "Grande"


def _paired_arrays(pre: Sequence[float], post: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    frame = pd.DataFrame({"pre": pre, "post": post}).apply(pd.to_numeric, errors="coerce").dropna()
    if frame.empty:
        raise ValueError("No hay pares pretest-postest válidos.")
    return frame["pre"].to_numpy(dtype=float), frame["post"].to_numpy(dtype=float)


def shapiro_wilk(values: Sequence[float]) -> tuple[float, float]:
    """Prueba de normalidad de Shapiro-Wilk."""
    arr = _array(values)
    if arr.size < 3:
        return float("nan"), float("nan")
    # scipy advierte para n > 5000; en neuroguIA n=562.
    result = stats.shapiro(arr)
    return float(result.statistic), float(result.pvalue)


@dataclass(frozen=True)
class TestResult:
    test: str
    statistic: float
    p_value: float
    normality_p: float
    rosenthal_r: float
    n: int


def rosenthal_r_from_p(p_value: float, n: int, direction: float = 1.0) -> float:
    """Aproximación r = Z/sqrt(N), con Z derivado del valor p bilateral."""
    if n <= 0 or not np.isfinite(p_value) or p_value <= 0:
        return float("nan")
    p = min(max(float(p_value), np.finfo(float).tiny), 1.0)
    z = stats.norm.isf(p / 2.0)
    sign = -1.0 if direction < 0 else 1.0
    return float(sign * z / sqrt(n))


def prueba_pareada_automatica(
    pre: Sequence[float],
    post: Sequence[float],
    alpha: float = ALPHA_DEFAULT,
) -> TestResult:
    """Selecciona t pareada o Wilcoxon según normalidad de las diferencias."""
    pre_arr, post_arr = _paired_arrays(pre, post)
    differences = post_arr - pre_arr
    _, normality_p = shapiro_wilk(differences)

    if np.isfinite(normality_p) and normality_p >= alpha:
        result = stats.ttest_rel(post_arr, pre_arr, nan_policy="omit")
        test_name = "t de Student para muestras relacionadas"
    else:
        if np.allclose(differences, 0):
            statistic, p_value = 0.0, 1.0
        else:
            result = stats.wilcoxon(post_arr, pre_arr, zero_method="wilcox", alternative="two-sided")
            statistic, p_value = float(result.statistic), float(result.pvalue)
        test_name = "Wilcoxon"
        direction = float(np.mean(differences))
        return TestResult(
            test=test_name,
            statistic=float(statistic),
            p_value=float(p_value),
            normality_p=float(normality_p),
            rosenthal_r=rosenthal_r_from_p(float(p_value), len(differences), direction),
            n=len(differences),
        )

    direction = float(np.mean(differences))
    return TestResult(
        test=test_name,
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        normality_p=float(normality_p),
        rosenthal_r=rosenthal_r_from_p(float(result.pvalue), len(differences), direction),
        n=len(differences),
    )


def prueba_independiente_automatica(
    group1: Sequence[float],
    group2: Sequence[float],
    alpha: float = ALPHA_DEFAULT,
) -> TestResult:
    """Selecciona t independiente o Mann-Whitney según normalidad."""
    a, b = _array(group1), _array(group2)
    _, p_a = shapiro_wilk(a)
    _, p_b = shapiro_wilk(b)
    normality_p = min(p_a, p_b) if np.isfinite(p_a) and np.isfinite(p_b) else float("nan")

    if np.isfinite(normality_p) and normality_p >= alpha:
        result = stats.ttest_ind(a, b, equal_var=True, nan_policy="omit")
        test_name = "t de Student para muestras independientes"
    else:
        result = stats.mannwhitneyu(a, b, alternative="two-sided")
        test_name = "U de Mann-Whitney"

    direction = float(np.mean(a) - np.mean(b))
    return TestResult(
        test=test_name,
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        normality_p=float(normality_p),
        rosenthal_r=rosenthal_r_from_p(float(result.pvalue), len(a) + len(b), direction),
        n=len(a) + len(b),
    )


def correlacion_spearman(x: Sequence[float], y: Sequence[float]) -> tuple[float, float, int]:
    """Coeficiente rho de Spearman y valor p."""
    frame = pd.DataFrame({"x": x, "y": y}).apply(pd.to_numeric, errors="coerce").dropna()
    if len(frame) < 3:
        return float("nan"), float("nan"), len(frame)
    result = stats.spearmanr(frame["x"], frame["y"])
    return float(result.statistic), float(result.pvalue), len(frame)


def correlacion_pearson(x: Sequence[float], y: Sequence[float]) -> tuple[float, float, int]:
    """Correlación lineal de Pearson y valor p."""
    frame = pd.DataFrame({"x": x, "y": y}).apply(pd.to_numeric, errors="coerce").dropna()
    if len(frame) < 3:
        return float("nan"), float("nan"), len(frame)
    result = stats.pearsonr(frame["x"], frame["y"])
    return float(result.statistic), float(result.pvalue), len(frame)


def metricas_clasificador(
    y_true: Sequence[object],
    y_pred: Sequence[object],
    y_score: np.ndarray | None = None,
    labels: Sequence[object] | None = None,
) -> dict[str, float]:
    """Accuracy, precision, recall, F1 macro, ROC-AUC y error."""
    true = np.asarray(y_true)
    pred = np.asarray(y_pred)
    if true.size == 0 or pred.size == 0 or true.size != pred.size:
        raise ValueError("y_true y y_pred deben tener la misma longitud y no estar vacíos.")

    output = {
        "accuracy": float(accuracy_score(true, pred)),
        "precision_macro": float(precision_score(true, pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(true, pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(true, pred, average="macro", zero_division=0)),
    }
    output["error_clasificacion"] = 1.0 - output["accuracy"]
    output["roc_auc_ovr_macro"] = float("nan")

    if y_score is not None:
        labels_arr = np.asarray(labels if labels is not None else sorted(pd.unique(true)))
        scores = np.asarray(y_score, dtype=float)
        if scores.ndim != 2 or scores.shape[0] != true.size or scores.shape[1] != labels_arr.size:
            raise ValueError("y_score debe tener forma (n_muestras, n_clases).")
        binary = label_binarize(true, classes=labels_arr)
        output["roc_auc_ovr_macro"] = float(
            roc_auc_score(binary, scores, average="macro", multi_class="ovr")
        )
    return output


def similitud_coseno(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    """cos(theta) = (A·B) / (||A|| ||B||)."""
    a, b = np.asarray(vector_a, dtype=float), np.asarray(vector_b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("Los vectores deben tener la misma dimensión.")
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return float("nan")
    return float(np.dot(a, b) / denominator)


def catalogo_formulas() -> pd.DataFrame:
    """Inventario auditable de fórmulas y funciones."""
    rows = [
        ("Cambio absoluto", "post - pre", "cambio_absoluto"),
        ("Cambio porcentual crudo", "((post - pre) / pre) * 100", "cambio_porcentual_crudo"),
        ("Reducción favorable", "((pre - post) / pre) * 100", "cambio_favorable_porcentual"),
        ("Incremento favorable", "((post - pre) / pre) * 100", "cambio_favorable_porcentual"),
        ("Diferencia postest", "post_exp - post_control", "diferencia_postest_grupos"),
        ("SD combinada", "sqrt(((n1-1)s1² + (n2-1)s2²)/(n1+n2-2))", "desviacion_estandar_combinada"),
        ("Cohen's d", "(media1 - media2) / SD_combinada", "cohen_d_independiente"),
        ("Shapiro-Wilk", "scipy.stats.shapiro", "shapiro_wilk"),
        ("t pareada / Wilcoxon", "selección por normalidad de diferencias", "prueba_pareada_automatica"),
        ("t independiente / Mann-Whitney", "selección por normalidad", "prueba_independiente_automatica"),
        ("r de Rosenthal", "Z / sqrt(N)", "rosenthal_r_from_p"),
        ("Spearman", "rho de rangos", "correlacion_spearman"),
        ("Pearson", "r lineal", "correlacion_pearson"),
        ("Accuracy", "aciertos / total", "metricas_clasificador"),
        ("Precision macro", "promedio por clase de TP/(TP+FP)", "metricas_clasificador"),
        ("Recall macro", "promedio por clase de TP/(TP+FN)", "metricas_clasificador"),
        ("F1 macro", "promedio por clase de 2PR/(P+R)", "metricas_clasificador"),
        ("ROC-AUC macro OVR", "promedio uno-contra-resto", "metricas_clasificador"),
        ("Error de clasificación", "1 - accuracy", "metricas_clasificador"),
        ("Similitud coseno", "(A·B)/(||A||||B||)", "similitud_coseno"),
    ]
    return pd.DataFrame(rows, columns=["metrica", "formula", "funcion_codigo"])
