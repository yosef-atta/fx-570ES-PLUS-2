"""Unit tests for STAT Mode (statistics, regression, and distributions)."""
import math
from src.core.modes.stat_engine import StatEngine

def test_stat_1var_statistics():
    engine = StatEngine(stat_type="1-VAR")
    # Dataset: 2, 4, 6, 8
    for val in (2, 4, 6, 8):
        engine.add_row(x=val)

    assert engine.n() == 4
    assert engine.sum_x() == 20.0
    assert engine.sum_x2() == 120.0
    assert engine.mean_x() == 5.0
    # Population std dev = sqrt(((9+1+1+9)/4)) = sqrt(5) ≈ 2.236067977
    assert round(engine.sigma_x(), 5) == round(math.sqrt(5), 5)
    # Sample std dev = sqrt(20/3) ≈ 2.581988897
    assert round(engine.sx(), 5) == round(math.sqrt(20/3), 5)
    assert engine.min_x() == 2.0
    assert engine.max_x() == 8.0

def test_stat_linear_regression():
    engine = StatEngine(stat_type="A+BX")
    # Data: (1, 2), (2, 4), (3, 6) -> y = 0 + 2x, r = 1
    engine.add_row(1, 2)
    engine.add_row(2, 4)
    engine.add_row(3, 6)

    a, b, r = engine.linear_reg()
    assert round(a, 6) == 0.0
    assert round(b, 6) == 2.0
    assert round(r, 6) == 1.0

    # Estimations
    assert engine.estimate_y(5) == 10.0
    assert engine.estimate_x(8) == 4.0

def test_stat_normal_distribution():
    # P(0) = 0.5, Q(0) = 0, R(0) = 0.5
    assert round(StatEngine.norm_p(0.0), 4) == 0.5000
    assert round(StatEngine.norm_q(0.0), 4) == 0.0000
    assert round(StatEngine.norm_r(0.0), 4) == 0.5000
    # P(1.96) ≈ 0.975
    assert round(StatEngine.norm_p(1.96), 3) == 0.975
