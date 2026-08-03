# -*- coding: utf-8 -*-
import math

import numpy as np

from formulas_neuroguia import (
    cambio_absoluto,
    cambio_favorable_porcentual,
    cohen_d_independiente,
    correlacion_spearman,
    diferencia_postest_grupos,
    metricas_clasificador,
    similitud_coseno,
)


def test_cambio_absoluto():
    assert cambio_absoluto(17.75, 12.66) == -5.09


def test_reduccion_estres_oficial():
    value = cambio_favorable_porcentual(17.75, 12.66, "disminuye")
    assert math.isclose(value, 28.676056338, rel_tol=0, abs_tol=1e-9)


def test_incremento_apoyo_oficial():
    value = cambio_favorable_porcentual(2.69, 4.48, "aumenta")
    assert math.isclose(value, 66.542750929, rel_tol=0, abs_tol=1e-9)


def test_diferencia_postest():
    assert math.isclose(diferencia_postest_grupos(12.66, 17.03), -4.37)


def test_cohen_d_no_se_multiplica_por_100():
    value = cohen_d_independiente(10, 8, 2, 2, 30, 30)
    assert math.isclose(value, 1.0)


def test_spearman_perfecta():
    rho, p, n = correlacion_spearman([1, 2, 3, 4], [10, 20, 30, 40])
    assert math.isclose(rho, 1.0)
    assert n == 4


def test_metricas_clasificador():
    metrics = metricas_clasificador(
        ["a", "a", "b", "b"],
        ["a", "b", "b", "b"],
    )
    assert math.isclose(metrics["accuracy"], 0.75)
    assert math.isclose(metrics["error_clasificacion"], 0.25)


def test_similitud_coseno():
    assert math.isclose(similitud_coseno([1, 0], [1, 0]), 1.0)
