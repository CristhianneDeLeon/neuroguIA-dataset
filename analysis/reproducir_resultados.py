# -*- coding: utf-8 -*-
"""Reproduce y audita los resultados estadísticos utilizados por el dashboard neuroguIA.

Uso principal:
    python analysis/reproducir_resultados.py ^
        --input data/neuroguIA_concentrado_maestro_trazable.xlsx ^
        --output outputs/reproducibilidad

El script no modifica el archivo de entrada. Produce tablas CSV, un manifiesto
JSON y un informe de validación contra las referencias oficiales del dashboard.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
import sklearn
import statsmodels.api as sm

from formulas_neuroguia import (
    cambio_absoluto,
    cambio_favorable_porcentual,
    cambio_porcentual_crudo,
    catalogo_formulas,
    cohen_d_independiente,
    cohen_d_prepost_pooled,
    cohen_dz_pareado,
    correlacion_spearman,
    diferencia_postest_grupos,
    interpretar_cohen_d,
    metricas_clasificador,
    prueba_independiente_automatica,
    prueba_pareada_automatica,
)


VARIABLES = {
    "estres": {
        "pre": ("stress_pre", "estres_pre"),
        "post": ("stress_post", "estres_post"),
        "mejora": "disminuye",
    },
    "ansiedad": {
        "pre": ("anxiety_pre", "ansiedad_pre"),
        "post": ("anxiety_post", "ansiedad_post"),
        "mejora": "disminuye",
    },
    "depresion": {
        "pre": ("depression_pre", "depresion_pre"),
        "post": ("depression_post", "depresion_post"),
        "mejora": "disminuye",
    },
    "apoyo_social": {
        "pre": (
            "support_pre_1_5",
            "support_pre",
            "support_index_pre_1_5",
            "apoyo_pre",
            "mspss_pre",
        ),
        "post": (
            "support_post_1_5",
            "support_post",
            "support_index_post_1_5",
            "apoyo_post",
            "mspss_post",
        ),
        "mejora": "aumenta",
    },
}

GROUP_ALIASES = ("group_type", "group", "grupo")
ID_ALIASES = ("participant_id", "participant", "id_participante", "research_profile_code")
TRUE_LABEL_ALIASES = ("y_true", "true_label", "actual_label", "actual_category", "categoria_real")
PRED_LABEL_ALIASES = ("y_pred", "predicted_label", "predicted_category", "categoria_predicha")


def normalize_name(name: object) -> str:
    text = str(name).strip().lower()
    replacements = str.maketrans("áéíóúüñ", "aeiouun")
    text = text.translate(replacements)
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def normalize_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [normalize_name(column) for column in out.columns]
    return out.dropna(how="all").reset_index(drop=True)


def first_column(df: pd.DataFrame, aliases: tuple[str, ...]) -> str | None:
    columns = {normalize_name(column): column for column in df.columns}
    for alias in aliases:
        key = normalize_name(alias)
        if key in columns:
            return columns[key]
    return None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_input(path: Path) -> dict[str, pd.DataFrame]:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xlsm", ".xls"}:
        sheets = pd.read_excel(path, sheet_name=None)
        return {name: normalize_frame(frame) for name, frame in sheets.items()}
    if suffix == ".csv":
        return {path.stem: normalize_frame(pd.read_csv(path))}
    raise ValueError("La entrada debe ser un archivo .xlsx, .xlsm, .xls o .csv.")


def detect_prepost_sheet(sheets: dict[str, pd.DataFrame]) -> tuple[str, pd.DataFrame]:
    best_name, best_frame, best_score = "", pd.DataFrame(), -1
    for name, frame in sheets.items():
        group = first_column(frame, GROUP_ALIASES)
        score = 2 if group else 0
        for spec in VARIABLES.values():
            if first_column(frame, spec["pre"]) and first_column(frame, spec["post"]):
                score += 3
        if first_column(frame, ID_ALIASES):
            score += 1
        if score > best_score:
            best_name, best_frame, best_score = name, frame, score

    if best_score < 5:
        raise RuntimeError(
            "No se encontró una hoja con group_type y pares pretest-postest reconocibles."
        )
    return best_name, best_frame


def standardize_groups(series: pd.Series) -> pd.Series:
    def convert(value: object) -> str:
        key = normalize_name(value)
        if key in {"experimental", "experimento", "intervencion", "g1"}:
            return "Experimental"
        if key in {"control", "lista_espera", "g2"}:
            return "Control"
        return str(value).strip()
    return series.map(convert)


def analyze_prepost(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    group_col = first_column(frame, GROUP_ALIASES)
    if group_col is None:
        raise RuntimeError("La tabla prepost no contiene columna de grupo.")

    work = frame.copy()
    work["_grupo"] = standardize_groups(work[group_col])

    summary_rows: list[dict[str, Any]] = []
    test_rows: list[dict[str, Any]] = []
    between_rows: list[dict[str, Any]] = []

    detected: dict[str, tuple[str, str, str]] = {}
    for variable, spec in VARIABLES.items():
        pre_col = first_column(work, spec["pre"])
        post_col = first_column(work, spec["post"])
        if pre_col and post_col:
            detected[variable] = (pre_col, post_col, str(spec["mejora"]))

    if not detected:
        raise RuntimeError("No se encontraron pares de variables pretest-postest.")

    for variable, (pre_col, post_col, mejora) in detected.items():
        work[pre_col] = pd.to_numeric(work[pre_col], errors="coerce")
        work[post_col] = pd.to_numeric(work[post_col], errors="coerce")

        for group_name, subset in work.groupby("_grupo", dropna=False):
            pairs = subset[[pre_col, post_col]].dropna()
            if len(pairs) < 3:
                continue

            pre_mean = float(pairs[pre_col].mean())
            post_mean = float(pairs[post_col].mean())
            paired_test = prueba_pareada_automatica(pairs[pre_col], pairs[post_col])

            summary_rows.append(
                {
                    "variable": variable,
                    "grupo": group_name,
                    "n": len(pairs),
                    "pre_media": pre_mean,
                    "pre_sd": float(pairs[pre_col].std(ddof=1)),
                    "post_media": post_mean,
                    "post_sd": float(pairs[post_col].std(ddof=1)),
                    "cambio_absoluto": cambio_absoluto(pre_mean, post_mean),
                    "cambio_porcentual_crudo": cambio_porcentual_crudo(pre_mean, post_mean),
                    "cambio_favorable_porcentual": cambio_favorable_porcentual(
                        pre_mean, post_mean, mejora
                    ),
                    "direccion_favorable": mejora,
                    "cohen_d_prepost_pooled": cohen_d_prepost_pooled(
                        pairs[pre_col], pairs[post_col]
                    ),
                    "cohen_dz_pareado": cohen_dz_pareado(
                        pairs[pre_col], pairs[post_col]
                    ),
                }
            )
            test_rows.append(
                {
                    "variable": variable,
                    "grupo": group_name,
                    **asdict(paired_test),
                }
            )

        exp = work.loc[work["_grupo"] == "Experimental", post_col].dropna()
        control = work.loc[work["_grupo"] == "Control", post_col].dropna()
        if len(exp) >= 3 and len(control) >= 3:
            between = prueba_independiente_automatica(exp, control)
            between_rows.append(
                {
                    "variable": variable,
                    "n_experimental": len(exp),
                    "n_control": len(control),
                    "post_media_experimental": float(exp.mean()),
                    "post_media_control": float(control.mean()),
                    "diferencia_postest": diferencia_postest_grupos(exp.mean(), control.mean()),
                    "cohen_d_independiente": cohen_d_independiente(
                        exp.mean(),
                        control.mean(),
                        exp.std(ddof=1),
                        control.std(ddof=1),
                        len(exp),
                        len(control),
                    ),
                    "interpretacion_cohen_d": interpretar_cohen_d(
                        cohen_d_independiente(
                            exp.mean(),
                            control.mean(),
                            exp.std(ddof=1),
                            control.std(ddof=1),
                            len(exp),
                            len(control),
                        )
                    ),
                    **asdict(between),
                }
            )

    summary = pd.DataFrame(summary_rows)
    tests = pd.DataFrame(test_rows)
    between = pd.DataFrame(between_rows)
    return summary, tests, between


def detect_usage_sheet(
    sheets: dict[str, pd.DataFrame],
    excluded_name: str,
) -> tuple[str, pd.DataFrame] | None:
    usage_aliases = {
        "sessions", "session_count", "sessions_total", "sesiones",
        "messages", "message_count", "messages_total", "mensajes",
        "average_session_duration_minutes", "duration_mean", "duracion_promedio",
        "continuity_contextual", "continuidad_contextual",
        "engagement", "engagement_index",
    }
    best: tuple[str, pd.DataFrame, int] | None = None
    for name, frame in sheets.items():
        if name == excluded_name:
            continue
        id_col = first_column(frame, ID_ALIASES)
        score = 2 if id_col else 0
        score += sum(1 for column in frame.columns if normalize_name(column) in usage_aliases)
        if score >= 3 and (best is None or score > best[2]):
            best = (name, frame, score)
    return None if best is None else (best[0], best[1])


def analyze_correlations_and_regression(
    prepost: pd.DataFrame,
    usage: pd.DataFrame,
    scope: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    pre_id = first_column(prepost, ID_ALIASES)
    usage_id = first_column(usage, ID_ALIASES)
    group_col = first_column(prepost, GROUP_ALIASES)
    stress_pre = first_column(prepost, VARIABLES["estres"]["pre"])
    stress_post = first_column(prepost, VARIABLES["estres"]["post"])

    if not all([pre_id, usage_id, group_col, stress_pre, stress_post]):
        return pd.DataFrame(), pd.DataFrame()

    left = prepost.copy()
    right = usage.copy()
    left[pre_id] = left[pre_id].astype(str)
    right[usage_id] = right[usage_id].astype(str)

    merged = left.merge(right, left_on=pre_id, right_on=usage_id, how="inner", suffixes=("", "_usage"))
    merged["_grupo"] = standardize_groups(merged[group_col])
    merged["_reduccion_estres"] = (
        pd.to_numeric(merged[stress_pre], errors="coerce")
        - pd.to_numeric(merged[stress_post], errors="coerce")
    )

    if scope == "experimental":
        merged = merged[merged["_grupo"] == "Experimental"].copy()

    excluded = {
        normalize_name(pre_id),
        normalize_name(usage_id),
        normalize_name(group_col),
        normalize_name(stress_pre),
        normalize_name(stress_post),
    }

    candidate_columns = []
    for column in usage.columns:
        key = normalize_name(column)
        if key in excluded:
            continue
        numeric = pd.to_numeric(merged.get(column), errors="coerce")
        if numeric.notna().sum() >= 10 and numeric.nunique(dropna=True) > 1:
            merged[column] = numeric
            candidate_columns.append(column)

    corr_rows = []
    for column in candidate_columns:
        rho, p_value, n = correlacion_spearman(merged[column], merged["_reduccion_estres"])
        corr_rows.append(
            {
                "variable_uso": column,
                "resultado": "reduccion_estres",
                "spearman_rho": rho,
                "p_value": p_value,
                "n": n,
                "scope": scope,
            }
        )
    correlations = pd.DataFrame(corr_rows).sort_values(
        "spearman_rho", key=lambda s: s.abs(), ascending=False
    ) if corr_rows else pd.DataFrame()

    regression = pd.DataFrame()
    predictors = candidate_columns[:8]
    regression_frame = merged[predictors + ["_reduccion_estres"]].dropna() if predictors else pd.DataFrame()
    if predictors and len(regression_frame) > len(predictors) + 2:
        x = sm.add_constant(regression_frame[predictors], has_constant="add")
        y = regression_frame["_reduccion_estres"]
        model = sm.OLS(y, x).fit()

        rows = [{
            "dependent_variable": "reduccion_estres",
            "predictors": " | ".join(predictors),
            "n": int(model.nobs),
            "r_squared": float(model.rsquared),
            "adjusted_r_squared": float(model.rsquared_adj),
            "f_statistic": float(model.fvalue) if model.fvalue is not None else float("nan"),
            "p_value_global": float(model.f_pvalue) if model.f_pvalue is not None else float("nan"),
            "scope": scope,
        }]
        for name, coefficient in model.params.items():
            rows.append(
                {
                    "dependent_variable": "coeficiente",
                    "predictors": name,
                    "n": int(model.nobs),
                    "r_squared": float(coefficient),
                    "adjusted_r_squared": float(model.bse[name]),
                    "f_statistic": float(model.tvalues[name]),
                    "p_value_global": float(model.pvalues[name]),
                    "scope": scope,
                }
            )
        regression = pd.DataFrame(rows)

    return correlations, regression


def detect_classifier_sheet(sheets: dict[str, pd.DataFrame]) -> tuple[str, pd.DataFrame] | None:
    for name, frame in sheets.items():
        true_col = first_column(frame, TRUE_LABEL_ALIASES)
        pred_col = first_column(frame, PRED_LABEL_ALIASES)
        if true_col and pred_col:
            return name, frame
    return None


def analyze_classifier(frame: pd.DataFrame) -> pd.DataFrame:
    true_col = first_column(frame, TRUE_LABEL_ALIASES)
    pred_col = first_column(frame, PRED_LABEL_ALIASES)
    if not true_col or not pred_col:
        return pd.DataFrame()

    valid = frame[[true_col, pred_col]].dropna()
    metrics = metricas_clasificador(valid[true_col], valid[pred_col])
    return pd.DataFrame(
        [{"metrica": key, "valor": value, "n": len(valid)} for key, value in metrics.items()]
    )


def hypothesis_summary(summary: pd.DataFrame, tests: pd.DataFrame) -> pd.DataFrame:
    if summary.empty or tests.empty:
        return pd.DataFrame()

    target = summary[
        (summary["variable"] == "estres") & (summary["grupo"] == "Experimental")
    ]
    target_test = tests[
        (tests["variable"] == "estres") & (tests["grupo"] == "Experimental")
    ]
    if target.empty or target_test.empty:
        return pd.DataFrame()

    reduction = float(target.iloc[0]["cambio_favorable_porcentual"])
    p_value = float(target_test.iloc[0]["p_value"])
    threshold = 15.0
    accepted = reduction >= threshold and p_value < 0.05
    return pd.DataFrame(
        [{
            "hypothesis": "H1",
            "minimum_threshold_percent": threshold,
            "observed_reduction_percent": reduction,
            "p_value": p_value,
            "decision": "Se acepta H1" if accepted else "No se acepta H1",
            "criterion": "reducción >= 15% y p < 0.05",
        }]
    )


def metric_map(
    summary: pd.DataFrame,
    between: pd.DataFrame,
    hypothesis: pd.DataFrame,
    classifier: pd.DataFrame,
    correlations: pd.DataFrame,
    regression: pd.DataFrame,
) -> dict[str, float]:
    values: dict[str, float] = {}

    for _, row in summary.iterrows():
        variable = str(row["variable"])
        group = str(row["grupo"]).lower()
        values[f"{variable}_{group}_pre"] = float(row["pre_media"])
        values[f"{variable}_{group}_post"] = float(row["post_media"])
        values[f"{variable}_{group}_change_percent"] = float(row["cambio_favorable_porcentual"])

    if not hypothesis.empty:
        values["stress_h1_reduction_percent"] = float(
            hypothesis.iloc[0]["observed_reduction_percent"]
        )

    if not classifier.empty:
        for _, row in classifier.iterrows():
            values[f"classifier_{row['metrica']}"] = float(row["valor"])

    if not correlations.empty:
        messages = correlations[
            correlations["variable_uso"].map(normalize_name).str.contains("message|mensaje", regex=True)
        ]
        if not messages.empty:
            values["spearman_messages_stress_reduction"] = float(messages.iloc[0]["spearman_rho"])

    if not regression.empty:
        model_row = regression[regression["dependent_variable"] == "reduccion_estres"]
        if not model_row.empty:
            values["regression_r2"] = float(model_row.iloc[0]["r_squared"])
            values["regression_p_global"] = float(model_row.iloc[0]["p_value_global"])

    return values


def validate_references(
    references_path: Path,
    computed: dict[str, float],
) -> pd.DataFrame:
    references = pd.read_csv(references_path)
    rows = []
    for _, row in references.iterrows():
        metric = str(row["metric"])
        expected = pd.to_numeric(pd.Series([row["expected_value"]]), errors="coerce").iloc[0]
        tolerance = pd.to_numeric(pd.Series([row["tolerance"]]), errors="coerce").iloc[0]
        calculated = computed.get(metric, float("nan"))

        if pd.isna(expected):
            status = "SIN_REFERENCIA_NUMERICA"
            difference = float("nan")
        elif not np.isfinite(calculated):
            status = "NO_CALCULADO"
            difference = float("nan")
        else:
            difference = float(calculated - expected)
            status = "COINCIDE" if abs(difference) <= float(tolerance) else "DIFIERE"

        rows.append(
            {
                "metric": metric,
                "expected_value": expected,
                "calculated_value": calculated,
                "difference": difference,
                "tolerance": tolerance,
                "status": status,
                "source_section": row.get("source_section", ""),
                "note": row.get("note", ""),
            }
        )
    return pd.DataFrame(rows)


def save_csv(frame: pd.DataFrame, path: Path) -> None:
    if frame is not None and not frame.empty:
        frame.to_csv(path, index=False, encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce resultados del dashboard neuroguIA.")
    parser.add_argument("--input", required=True, help="Archivo maestro .xlsx o tabla .csv.")
    parser.add_argument("--output", default="outputs/reproducibilidad", help="Directorio de salida.")
    parser.add_argument(
        "--correlation-scope",
        choices=("all", "experimental"),
        default="all",
        help="Muestra utilizada en correlaciones y regresión.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Devuelve error si alguna referencia oficial calculable difiere.",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    sheets = read_input(input_path)
    prepost_sheet_name, prepost = detect_prepost_sheet(sheets)
    summary, tests, between = analyze_prepost(prepost)

    usage_detected = detect_usage_sheet(sheets, prepost_sheet_name)
    correlations, regression = pd.DataFrame(), pd.DataFrame()
    usage_sheet_name = None
    if usage_detected:
        usage_sheet_name, usage = usage_detected
        correlations, regression = analyze_correlations_and_regression(
            prepost, usage, args.correlation_scope
        )

    classifier_detected = detect_classifier_sheet(sheets)
    classifier, classifier_sheet_name = pd.DataFrame(), None
    if classifier_detected:
        classifier_sheet_name, classifier_frame = classifier_detected
        classifier = analyze_classifier(classifier_frame)

    hypothesis = hypothesis_summary(summary, tests)

    save_csv(summary, output_dir / "01_resultados_prepost_reproducidos.csv")
    save_csv(tests, output_dir / "02_pruebas_inferenciales_reproducidas.csv")
    save_csv(between, output_dir / "03_comparacion_postest_grupos.csv")
    save_csv(hypothesis, output_dir / "04_contraste_hipotesis.csv")
    save_csv(correlations, output_dir / "05_correlaciones_spearman.csv")
    save_csv(regression, output_dir / "06_modelo_regresion.csv")
    save_csv(classifier, output_dir / "07_metricas_clasificador.csv")
    catalogo_formulas().to_csv(
        output_dir / "00_catalogo_formulas.csv",
        index=False,
        encoding="utf-8-sig",
    )

    computed = metric_map(summary, between, hypothesis, classifier, correlations, regression)
    references_path = Path(__file__).resolve().with_name("referencias_dashboard.csv")
    validation = validate_references(references_path, computed)
    validation.to_csv(
        output_dir / "08_validacion_referencias_dashboard.csv",
        index=False,
        encoding="utf-8-sig",
    )

    manifest = {
        "project": "neuroguIA",
        "script": str(Path(__file__).resolve()),
        "input_file": str(input_path),
        "input_sha256": file_sha256(input_path),
        "prepost_sheet": prepost_sheet_name,
        "usage_sheet": usage_sheet_name,
        "classifier_sheet": classifier_sheet_name,
        "correlation_scope": args.correlation_scope,
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
        "statsmodels": sm.__version__,
        "outputs": sorted(path.name for path in output_dir.glob("*")),
        "notes": [
            "El dashboard presenta resultados; este script concentra los cálculos.",
            "Cohen's d se calcula sin multiplicar por 100.",
            "Las diferencias contra referencias oficiales se reportan, no se ocultan.",
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    differs = validation["status"].eq("DIFIERE").sum()
    print(f"Entrada: {input_path}")
    print(f"Hoja prepost detectada: {prepost_sheet_name}")
    print(f"Salida: {output_dir}")
    print(f"Referencias que difieren: {differs}")

    if args.strict and differs:
        print(
            "ERROR DE TRAZABILIDAD: existen resultados que no coinciden con "
            "las referencias oficiales del dashboard.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
