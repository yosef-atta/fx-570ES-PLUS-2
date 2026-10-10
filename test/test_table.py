"""Unit tests for TABLE Mode (function table generator)."""
from src.core.modes.table_engine import TableEngine

def test_table_single_function_generation():
    engine = TableEngine(angle_unit="DEG")
    # f(X) = X^2 + 1, from 1 to 3, step 1 -> (1, 2), (2, 5), (3, 10)
    rows = engine.generate("X^2 + 1", start=1, end=3, step=1)
    assert len(rows) == 3
    assert rows[0].x == 1.0 and rows[0].f_val == "2"
    assert rows[1].x == 2.0 and rows[1].f_val == "5"
    assert rows[2].x == 3.0 and rows[2].f_val == "10"

def test_table_dual_function_generation():
    engine = TableEngine(angle_unit="DEG")
    # f(X) = 2X, g(X) = 3X, from 0 to 2, step 1
    rows = engine.generate("2X", start=0, end=2, step=1, g_expr_str="3X")
    assert len(rows) == 3
    assert rows[0].f_val == "0" and rows[0].g_val == "0"
    assert rows[1].f_val == "2" and rows[1].g_val == "3"
    assert rows[2].f_val == "4" and rows[2].g_val == "6"
