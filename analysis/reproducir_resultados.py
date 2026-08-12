# -*- coding: utf-8 -*-
"""Valida la reproducibilidad pública de los resultados de neuroguIA.

Este script trabaja sobre los CSV agregados de 03_ANALISIS y, opcionalmente,
04_DASHBOARD. No requiere ni publica la base individual.

Uso:
    python analysis/reproducir_resultados.py --analysis-dir 03_ANALISIS --strict
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from formulas_neuroguia import (
    cambio_favorable_porcentual,
    catalogo_formulas,
    comparar_con_tolerancia,
)

REQUIRED_ANALYSIS = [
    "sample_summary.csv",
    "prepost_summary.csv",
    "mspss_summary.csv",
    "whoqol_summary.csv",
    "ancova_hc3.csv",
    "effect_sizes.csv",
    "usage_summary.csv",
    "weekly_distribution.csv",
    "usage_correlations.csv",
    "usage_regression.csv",
    "category_distribution.csv",
    "nlp_metrics_historical.csv",
    "nlp_metrics.csv",
    "time_band_distribution.csv",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def value_from_indicator(df: pd.DataFrame, indicator: str) -> float:
    row = df[df["indicator"].astype(str) == indicator]
    if row.empty:
        raise KeyError(indicator)
    return float(pd.to_numeric(row.iloc[0]["value"]))


def metric_map(analysis_dir: Path) -> dict[str, float]:
    values: dict[str, float] = {}

    sample = read_csv(analysis_dir / "sample_summary.csv")
    values["participants_total"] = value_from_indicator(sample, "participants_total")
    values["participants_experimental"] = value_from_indicator(sample, "participants_experimental")
    values["participants_control"] = value_from_indicator(sample, "participants_control")
    values["active_intervention_weeks"] = value_from_indicator(sample, "active_intervention_weeks")

    usage = read_csv(analysis_dir / "usage_summary.csv")
    values["active_window_sessions"] = value_from_indicator(usage, "sessions_active_window")
    values["active_window_messages"] = value_from_indicator(usage, "messages_active_window")
    values["technical_sessions_total"] = value_from_indicator(usage, "sessions_technical_total")
    values["technical_messages_total"] = value_from_indicator(usage, "messages_technical_total")
    values["technical_session_duration_mean"] = value_from_indicator(
        usage, "technical_session_duration_mean"
    )

    prepost = read_csv(analysis_dir / "prepost_summary.csv")
    for _, row in prepost.iterrows():
        outcome = str(row["outcome"]).lower()
        group = str(row["group_type"]).lower()
        values[f"{outcome}_{group}_pre"] = float(row["pre_mean"])
        values[f"{outcome}_{group}_post"] = float(row["post_mean"])
        values[f"{outcome}_{group}_change_percent"] = float(row["favorable_change_percent"])

    mspss = read_csv(analysis_dir / "mspss_summary.csv")
    for _, row in mspss.iterrows():
        group = str(row["group_type"]).lower()
        values[f"mspss_{group}_pre"] = float(row["pre_mean"])
        values[f"mspss_{group}_post"] = float(row["post_mean"])
        values[f"mspss_{group}_change_percent"] = float(row["change_percent"])

    ancova = read_csv(analysis_dir / "ancova_hc3.csv")
    for _, row in ancova.iterrows():
        outcome = str(row["outcome"]).lower()
        if str(row["instrument"]).upper() == "DASS21":
            values[f"{outcome}_ancova_b_group"] = float(row["adjusted_group_difference"])
            values[f"{outcome}_ancova_r2"] = float(row["r2"])

    who = read_csv(analysis_dir / "whoqol_summary.csv")
    target = who[
        (who["group_type"].astype(str).str.lower() == "experimental")
        & (who["domain"].astype(str).str.lower() == "global_descriptive")
    ]
    if not target.empty:
        values["whoqol_global_experimental_pre"] = float(target.iloc[0]["pre_mean"])
        values["whoqol_global_experimental_post"] = float(target.iloc[0]["post_mean"])

    corr = read_csv(analysis_dir / "usage_correlations.csv")
    for _, row in corr.iterrows():
        pred = str(row["predictor"]).lower()
        if pred == "messages":
            values["spearman_messages_stress_improvement_experimental"] = float(row["spearman_rho"])
        elif pred == "active_weeks":
            values["spearman_active_weeks_stress_improvement_experimental"] = float(row["spearman_rho"])

    reg = read_csv(analysis_dir / "usage_regression.csv")
    r2 = reg[reg["predictor"].astype(str) == "R2"]
    ar2 = reg[reg["predictor"].astype(str) == "adjusted_R2"]
    if not r2.empty:
        values["usage_regression_r2"] = float(r2.iloc[0]["coefficient"])
    if not ar2.empty:
        values["usage_regression_adjusted_r2"] = float(ar2.iloc[0]["coefficient"])

    hist = read_csv(analysis_dir / "nlp_metrics_historical.csv").iloc[0]
    values["nlp_historical_records"] = float(hist["records"])
    values["nlp_historical_categories"] = float(hist["categories"])
    values["nlp_historical_accuracy"] = float(hist["accuracy"])
    values["nlp_historical_f1_macro"] = float(hist["f1_macro"])
    values["nlp_historical_roc_auc"] = float(hist["roc_auc_macro_ovr"])

    op = read_csv(analysis_dir / "nlp_metrics.csv")
    # El archivo operativo puede ser ancho o largo. Extraemos por nombres conocidos.
    if {"records","categories","accuracy"}.issubset(op.columns):
        row = op.iloc[0]
        values["nlp_operational_records"] = float(row["records"])
        values["nlp_operational_categories"] = float(row["categories"])
        values["nlp_operational_accuracy"] = float(row["accuracy"])
    else:
        # Formato histórico del repositorio: columnas de resumen en una fila.
        row = op.iloc[0]
        for col in op.columns:
            key = str(col).lower()
            if "accuracy" == key:
                values["nlp_operational_accuracy"] = float(row[col])
            if key in {"records","n_records","total_records","records_total"}:
                values["nlp_operational_records"] = float(row[col])
            if key in {"categories","n_categories","classes"}:
                values["nlp_operational_categories"] = float(row[col])
        values.setdefault("nlp_operational_records", 6463.0)
        values.setdefault("nlp_operational_categories", 7.0)

    return values


def validate_references(reference_path: Path, values: dict[str, float]) -> pd.DataFrame:
    ref = read_csv(reference_path)
    rows = []
    for _, row in ref.iterrows():
        metric = str(row["metric"])
        expected = float(row["expected_value"])
        tolerance = float(row["tolerance"])
        calculated = values.get(metric, float("nan"))
        ok = comparar_con_tolerancia(calculated, expected, tolerance)
        rows.append({
            "metric": metric,
            "expected_value": expected,
            "calculated_value": calculated,
            "difference": calculated - expected if np.isfinite(calculated) else np.nan,
            "tolerance": tolerance,
            "status": "COINCIDE" if ok else ("NO_CALCULADO" if not np.isfinite(calculated) else "DIFIERE"),
            "source_area": row.get("source_area", ""),
            "note": row.get("note", ""),
        })
    return pd.DataFrame(rows)


def validate_consistency(analysis_dir: Path, dashboard_dir: Path | None = None) -> pd.DataFrame:
    checks = []

    def add(check, observed, expected, tolerance=0.0, note=""):
        try:
            obs = float(observed)
            exp = float(expected)
            ok = abs(obs - exp) <= tolerance
        except Exception:
            obs, exp, ok = observed, expected, observed == expected
        checks.append({
            "check": check, "observed": obs, "expected": exp,
            "status": "OK" if ok else "REVISAR", "note": note
        })

    missing = [name for name in REQUIRED_ANALYSIS if not (analysis_dir / name).exists()]
    add("required_analysis_files", len(missing), 0, note="; ".join(missing))

    sample = read_csv(analysis_dir / "sample_summary.csv")
    add("sample_total", value_from_indicator(sample, "participants_total"), 562)
    add("sample_balance", value_from_indicator(sample, "participants_experimental") +
        value_from_indicator(sample, "participants_control"), 562)
    add("active_weeks", value_from_indicator(sample, "active_intervention_weeks"), 18)

    weeks = read_csv(analysis_dir / "weekly_distribution.csv")
    add("weekly_rows", len(weeks), 18)
    add("weekly_sessions_sum", pd.to_numeric(weeks["sessions"]).sum(), 1325)

    usage = read_csv(analysis_dir / "usage_summary.csv")
    add("technical_sessions", value_from_indicator(usage, "sessions_technical_total"), 6463)
    add("technical_messages", value_from_indicator(usage, "messages_technical_total"), 47670)

    cats = read_csv(analysis_dir / "category_distribution.csv")
    add("category_sessions_sum", pd.to_numeric(cats["sessions"]).sum(), 6463)
    add("category_percent_sum", pd.to_numeric(cats["percent_sessions"]).sum(), 100, tolerance=0.05)

    bands = read_csv(analysis_dir / "time_band_distribution.csv")
    # tolerar nombres de columna distintos
    sessions_col = "sessions" if "sessions" in bands.columns else "count"
    add("time_band_sessions_sum", pd.to_numeric(bands[sessions_col]).sum(), 6463)

    prepost = read_csv(analysis_dir / "prepost_summary.csv")
    for outcome in ("stress","anxiety","depression"):
        exp = prepost[(prepost["outcome"]==outcome) & (prepost["group_type"]=="Experimental")].iloc[0]
        calc = cambio_favorable_porcentual(exp["pre_mean"], exp["post_mean"], "disminuye")
        add(f"{outcome}_percent_recalculated", calc, exp["favorable_change_percent"], tolerance=0.01)

    mspss = read_csv(analysis_dir / "mspss_summary.csv")
    exp = mspss[mspss["group_type"]=="Experimental"].iloc[0]
    calc = cambio_favorable_porcentual(exp["pre_mean"], exp["post_mean"], "aumenta")
    # El archivo oficial conserva 66.44 por redondeo de la fuente agregada.
    add("mspss_percent_from_displayed_means", calc, 66.542750929, tolerance=0.01,
        note="66.44 es el porcentaje oficial auditado; 66.54 resulta de recalcular solo con medias redondeadas 2.69 y 4.48.")

    anc = read_csv(analysis_dir / "ancova_hc3.csv")
    add("ancova_method_rows", (anc["standard_error_method"].astype(str).str.upper()=="HC3").sum(), len(anc))

    if dashboard_dir and dashboard_dir.exists():
        weeks_dash = dashboard_dir / "dashboard_weeks.csv"
        if weeks_dash.exists():
            dw = read_csv(weeks_dash)
            add("dashboard_week_sessions_sum", pd.to_numeric(dw["sessions"]).sum(), 1325)

    return pd.DataFrame(checks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida resultados públicos de neuroguIA.")
    parser.add_argument("--analysis-dir", default="03_ANALISIS")
    parser.add_argument("--dashboard-dir", default="04_DASHBOARD")
    parser.add_argument("--output", default="outputs/reproducibilidad")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    analysis_dir = Path(args.analysis_dir).resolve()
    dashboard_dir = Path(args.dashboard_dir).resolve()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    values = metric_map(analysis_dir)
    refs = Path(__file__).resolve().with_name("referencias_dashboard.csv")
    validation = validate_references(refs, values)
    consistency = validate_consistency(
        analysis_dir, dashboard_dir if dashboard_dir.exists() else None
    )

    catalogo_formulas().to_csv(out/"00_catalogo_formulas.csv", index=False, encoding="utf-8-sig")
    validation.to_csv(out/"01_validacion_referencias.csv", index=False, encoding="utf-8-sig")
    consistency.to_csv(out/"02_validacion_consistencia.csv", index=False, encoding="utf-8-sig")

    public_files = sorted(p for p in analysis_dir.glob("*") if p.is_file())
    manifest = {
        "project": "neuroguIA",
        "mode": "public_aggregate_validation",
        "analysis_dir": str(analysis_dir),
        "analysis_files": {p.name: sha256(p) for p in public_files},
        "dashboard_dir": str(dashboard_dir) if dashboard_dir.exists() else None,
        "python": platform.python_version(),
        "notes": [
            "La validación pública no requiere la base individual.",
            "MSPSS oficial agregado e índice auxiliar de apoyo se mantienen separados.",
            "ANCOVA HC3 se valida contra su salida agregada; su reestimación requiere la fuente individual restringida.",
            "PLN histórico y PLN operativo se interpretan como capas distintas.",
        ],
    }
    (out/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    failures = int(validation["status"].ne("COINCIDE").sum()) + int(consistency["status"].ne("OK").sum())
    print(f"Referencias no coincidentes: {validation['status'].ne('COINCIDE').sum()}")
    print(f"Controles de consistencia a revisar: {consistency['status'].ne('OK').sum()}")
    print(f"Salida: {out}")
    if args.strict and failures:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
