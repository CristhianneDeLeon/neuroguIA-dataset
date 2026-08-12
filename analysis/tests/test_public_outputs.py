# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "03_ANALISIS"


def _csv(name):
    return pd.read_csv(ANALYSIS / name, encoding="utf-8-sig")


def test_required_public_files_exist():
    required = [
        "sample_summary.csv",
        "prepost_summary.csv",
        "mspss_summary.csv",
        "ancova_hc3.csv",
        "usage_summary.csv",
        "weekly_distribution.csv",
        "usage_correlations.csv",
        "nlp_metrics_historical.csv",
    ]
    missing = [name for name in required if not (ANALYSIS/name).exists()]
    assert missing == []


def test_sample_is_562_and_balanced():
    df = _csv("sample_summary.csv")
    values = dict(zip(df["indicator"], df["value"]))
    assert int(values["participants_total"]) == 562
    assert int(values["participants_experimental"]) == 281
    assert int(values["participants_control"]) == 281
    assert int(values["active_intervention_weeks"]) == 18


def test_active_weeks_sum_1325():
    df = _csv("weekly_distribution.csv")
    assert len(df) == 18
    assert int(df["sessions"].sum()) == 1325


def test_mspss_official():
    df = _csv("mspss_summary.csv")
    exp = df[df["group_type"]=="Experimental"].iloc[0]
    con = df[df["group_type"]=="Control"].iloc[0]
    assert float(exp["pre_mean"]) == 2.69
    assert float(exp["post_mean"]) == 4.48
    assert float(con["pre_mean"]) == 2.69
    assert float(con["post_mean"]) == 2.73


def test_ancova_method_is_hc3():
    df = _csv("ancova_hc3.csv")
    assert (df["standard_error_method"].astype(str).str.upper() == "HC3").all()


def test_experimental_usage_correlations_are_not_significant():
    df = _csv("usage_correlations.csv")
    msg = df[df["predictor"]=="messages"].iloc[0]
    weeks = df[df["predictor"]=="active_weeks"].iloc[0]
    assert abs(float(msg["spearman_rho"]) - 0.021) < 0.005
    assert float(msg["p_value"]) > 0.05
    assert abs(float(weeks["spearman_rho"]) - 0.002) < 0.005
    assert float(weeks["p_value"]) > 0.05
