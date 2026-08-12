# -*- coding: utf-8 -*-
"""Fórmulas estadísticas y computacionales utilizadas por neuroguIA.

Este módulo concentra funciones pequeñas, auditables y reutilizables. La capa
pública de reproducibilidad trabaja sobre resultados agregados; los análisis que
requieren registros individuales se ejecutan sobre la fuente restringida y se
publican únicamente como salidas agregadas.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
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


def _paired_arrays(pre: Sequence[float], post: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    frame = pd.DataFrame({"pre": pre, "post": post}).apply(pd.to_numeric, errors="coerce").dropna()
    if frame.empty:
        raise ValueError("No hay pares pretest-postest válidos.")
    return frame["pre"].to_numpy(dtype=float), frame["post"].to_numpy(dtype=float)


def cambio_absoluto(pre: float, post: float) -> float:
    """ΔX = post - pre."""
    return float(post) - float(pre)


def cambio_porcentual_crudo(pre: float, post: float) -> float:
    """((post - pre) / pre) × 100."""
    pre = float(pre)
    return float("nan") if pre == 0 else ((float(post) - pre) / pre) * 100.0


def cambio_favorable_porcentual(pre: float, post: float, mejora: str) -> float:
    """Expresa la mejoría en una dirección común.

    mejora='disminuye': ((pre - post) / pre) × 100
    mejora='aumenta':   ((post - pre) / pre) × 100
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
    """Media post experimental - media post control."""
    return float(post_experimental) - float(post_control)


def desviacion_estandar_combinada(n1: int, sd1: float, n2: int, sd2: float) -> float:
    """SD combinada de dos grupos independientes."""
    n1, n2 = int(n1), int(n2)
    if n1 < 2 or n2 < 2:
        return float("nan")
    numerator = (n1 - 1) * float(sd1) ** 2 + (n2 - 1) * float(sd2) ** 2
    return sqrt(numerator / (n1 + n2 - 2))


def cohen_d_independiente(
    media1: float, media2: float, sd1: float, sd2: float, n1: int, n2: int
) -> float:
    """Cohen's d para grupos independientes."""
    pooled = desviacion_estandar_combinada(n1, sd1, n2, sd2)
    if not np.isfinite(pooled) or pooled == 0:
        return float("nan")
    return (float(media1) - float(media2)) / pooled


def cohen_d_prepost_pooled(pre: Sequence[float], post: Sequence[float]) -> float:
    """Cohen's d pre-post usando SD combinada."""
    pre_arr, post_arr = _paired_arrays(pre, post)
    n = len(pre_arr)
    pooled = desviacion_estandar_combinada(
        n, np.std(pre_arr, ddof=1), n, np.std(post_arr, ddof=1)
    )
    if not np.isfinite(pooled) or pooled == 0:
        return float("nan")
    return float((np.mean(post_arr) - np.mean(pre_arr)) / pooled)


def cohen_dz_pareado(pre: Sequence[float], post: Sequence[float]) -> float:
    """Cohen's dz pareado."""
    pre_arr, post_arr = _paired_arrays(pre, post)
    dif = post_arr - pre_arr
    sd = np.std(dif, ddof=1)
    return float("nan") if sd == 0 or not np.isfinite(sd) else float(np.mean(dif) / sd)


def interpretar_cohen_d(value: float) -> str:
    """Interpretación por magnitud absoluta."""
    if not np.isfinite(value):
        return "No calculable"
    x = abs(float(value))
    if x < 0.20:
        return "Trivial o muy pequeño"
    if x < 0.50:
        return "Pequeño"
    if x < 0.80:
        return "Moderado"
    return "Grande"


def shapiro_wilk(values: Sequence[float]) -> tuple[float, float]:
    arr = _array(values)
    if arr.size < 3:
        return float("nan"), float("nan")
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
    """r = Z / sqrt(N), a partir de un p bilateral."""
    if n <= 0 or not np.isfinite(p_value) or p_value <= 0:
        return float("nan")
    p = min(max(float(p_value), np.finfo(float).tiny), 1.0)
    z = stats.norm.isf(p / 2.0)
    return float((-1.0 if direction < 0 else 1.0) * z / sqrt(n))


def prueba_pareada_automatica(
    pre: Sequence[float], post: Sequence[float], alpha: float = ALPHA_DEFAULT
) -> TestResult:
    pre_arr, post_arr = _paired_arrays(pre, post)
    dif = post_arr - pre_arr
    _, normality_p = shapiro_wilk(dif)
    direction = float(np.mean(dif))
    if np.isfinite(normality_p) and normality_p >= alpha:
        result = stats.ttest_rel(post_arr, pre_arr, nan_policy="omit")
        return TestResult(
            "t de Student para muestras relacionadas",
            float(result.statistic),
            float(result.pvalue),
            float(normality_p),
            rosenthal_r_from_p(float(result.pvalue), len(dif), direction),
            len(dif),
        )
    if np.allclose(dif, 0):
        statistic, p_value = 0.0, 1.0
    else:
        result = stats.wilcoxon(post_arr, pre_arr, zero_method="wilcox", alternative="two-sided")
        statistic, p_value = float(result.statistic), float(result.pvalue)
    return TestResult(
        "Wilcoxon",
        statistic,
        p_value,
        float(normality_p),
        rosenthal_r_from_p(p_value, len(dif), direction),
        len(dif),
    )


def prueba_independiente_automatica(
    group1: Sequence[float], group2: Sequence[float], alpha: float = ALPHA_DEFAULT
) -> TestResult:
    a, b = _array(group1), _array(group2)
    _, p_a = shapiro_wilk(a)
    _, p_b = shapiro_wilk(b)
    normality_p = min(p_a, p_b)
    direction = float(np.mean(a) - np.mean(b))
    if np.isfinite(normality_p) and normality_p >= alpha:
        result = stats.ttest_ind(a, b, equal_var=True, nan_policy="omit")
        name = "t de Student para muestras independientes"
    else:
        result = stats.mannwhitneyu(a, b, alternative="two-sided")
        name = "U de Mann-Whitney"
    return TestResult(
        name,
        float(result.statistic),
        float(result.pvalue),
        float(normality_p),
        rosenthal_r_from_p(float(result.pvalue), len(a) + len(b), direction),
        len(a) + len(b),
    )


def correlacion_spearman(x: Sequence[float], y: Sequence[float]) -> tuple[float, float, int]:
    frame = pd.DataFrame({"x": x, "y": y}).apply(pd.to_numeric, errors="coerce").dropna()
    if len(frame) < 3:
        return float("nan"), float("nan"), len(frame)
    result = stats.spearmanr(frame["x"], frame["y"])
    return float(result.statistic), float(result.pvalue), len(frame)


def correlacion_pearson(x: Sequence[float], y: Sequence[float]) -> tuple[float, float, int]:
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
    true, pred = np.asarray(y_true), np.asarray(y_pred)
    if true.size == 0 or pred.size == 0 or true.size != pred.size:
        raise ValueError("y_true y y_pred deben tener igual longitud y no estar vacíos.")
    out = {
        "accuracy": float(accuracy_score(true, pred)),
        "precision_macro": float(precision_score(true, pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(true, pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(true, pred, average="macro", zero_division=0)),
    }
    out["error_clasificacion"] = 1.0 - out["accuracy"]
    out["roc_auc_ovr_macro"] = float("nan")
    if y_score is not None:
        labels_arr = np.asarray(labels if labels is not None else sorted(pd.unique(true)))
        scores = np.asarray(y_score, dtype=float)
        binary = label_binarize(true, classes=labels_arr)
        out["roc_auc_ovr_macro"] = float(
            roc_auc_score(binary, scores, average="macro", multi_class="ovr")
        )
    return out


def similitud_coseno(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    a, b = np.asarray(vector_a, dtype=float), np.asarray(vector_b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("Los vectores deben tener la misma dimensión.")
    den = np.linalg.norm(a) * np.linalg.norm(b)
    return float("nan") if den == 0 else float(np.dot(a, b) / den)


def ancova_hc3(
    post: Sequence[float], grupo_experimental: Sequence[float], pre: Sequence[float]
) -> dict[str, float]:
    """ANCOVA: post ~ grupo + pre con covarianza robusta HC3.

    grupo_experimental debe codificarse como 1=Experimental, 0=Control.
    """
    df = pd.DataFrame({"post": post, "grupo": grupo_experimental, "pre": pre}).dropna()
    x = sm.add_constant(df[["grupo", "pre"]], has_constant="add")
    model = sm.OLS(df["post"], x).fit(cov_type="HC3")
    ci = model.conf_int().loc["grupo"]
    return {
        "n": int(model.nobs),
        "b_grupo": float(model.params["grupo"]),
        "se_hc3": float(model.bse["grupo"]),
        "ci95_low": float(ci.iloc[0]),
        "ci95_high": float(ci.iloc[1]),
        "p_grupo": float(model.pvalues["grupo"]),
        "b_pre": float(model.params["pre"]),
        "r2": float(model.rsquared),
        "r2_ajustado": float(model.rsquared_adj),
    }


def comparar_con_tolerancia(calculado: float, esperado: float, tolerancia: float) -> bool:
    if not (np.isfinite(calculado) and np.isfinite(esperado)):
        return False
    return abs(float(calculado) - float(esperado)) <= float(tolerancia)


def catalogo_formulas() -> pd.DataFrame:
    rows = [
        ("Cambio absoluto", "post - pre", "cambio_absoluto"),
        ("Cambio porcentual crudo", "((post-pre)/pre)*100", "cambio_porcentual_crudo"),
        ("Cambio favorable", "dirección según constructo", "cambio_favorable_porcentual"),
        ("Diferencia postest", "post_exp - post_control", "diferencia_postest_grupos"),
        ("SD combinada", "pooled SD", "desviacion_estandar_combinada"),
        ("Cohen's d", "diferencia / SD combinada", "cohen_d_independiente"),
        ("Shapiro-Wilk", "scipy.stats.shapiro", "shapiro_wilk"),
        ("t pareada / Wilcoxon", "selección por normalidad", "prueba_pareada_automatica"),
        ("t independiente / Mann-Whitney", "selección por normalidad", "prueba_independiente_automatica"),
        ("r de Rosenthal", "Z/sqrt(N)", "rosenthal_r_from_p"),
        ("Spearman", "rho de rangos", "correlacion_spearman"),
        ("Pearson", "r lineal", "correlacion_pearson"),
        ("ANCOVA HC3", "post ~ grupo + pre; cov_type=HC3", "ancova_hc3"),
        ("Accuracy / precision / recall / F1 / ROC-AUC", "métricas de clasificación", "metricas_clasificador"),
        ("Similitud coseno", "(A·B)/(||A||||B||)", "similitud_coseno"),
    ]
    return pd.DataFrame(rows, columns=["metrica", "formula", "funcion_codigo"])
