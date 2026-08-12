# -*- coding: utf-8 -*-
import math

from formulas_neuroguia import (
    cambio_absoluto,
    cambio_favorable_porcentual,
    cohen_d_independiente,
    correlacion_spearman,
    diferencia_postest_grupos,
    metricas_clasificador,
    similitud_coseno,
)


def test_cambio_absoluto_estres_experimental():
    value = cambio_absoluto(17.88612099644128, 12.455516014234876)
    assert math.isclose(value, -5.430604982206404, abs_tol=1e-12)


def test_reduccion_estres_experimental():
    value = cambio_favorable_porcentual(
        17.88612099644128, 12.455516014234876, "disminuye"
    )
    assert math.isclose(value, 30.362116991643456, abs_tol=1e-10)


def test_incremento_mspss_desde_medias_redondeadas():
    value = cambio_favorable_porcentual(2.69, 4.48, "aumenta")
    assert math.isclose(value, 66.54275092936802, abs_tol=1e-10)


def test_diferencia_postest_estres():
    value = diferencia_postest_grupos(12.455516014234876, 18.160142348754448)
    assert math.isclose(value, -5.704626334519572, abs_tol=1e-12)


def test_cohen_d_estres_post_aproxima_salida_auditada():
    value = cohen_d_independiente(
        12.455516014234876, 18.160142348754448,
        6.114880547302489, 6.0017240363278885, 281, 281
    )
    assert math.isclose(value, -0.9414, abs_tol=0.002)


def test_spearman_perfecta():
    rho, _, n = correlacion_spearman([1,2,3,4], [10,20,30,40])
    assert math.isclose(rho, 1.0)
    assert n == 4


def test_metricas_clasificador():
    metrics = metricas_clasificador(["a","a","b","b"], ["a","b","b","b"])
    assert math.isclose(metrics["accuracy"], 0.75)
    assert math.isclose(metrics["error_clasificacion"], 0.25)


def test_similitud_coseno():
    assert math.isclose(similitud_coseno([1,0], [1,0]), 1.0)
