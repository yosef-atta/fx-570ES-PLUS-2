"""Tests for mathematical evaluator, exact arithmetic, and scientific functions."""
import math
import pytest
import sympy as sp
from src.core.math.errors import MathError, ArgumentError
from src.core.math.evaluator import Evaluator
from src.core.math.lexer import Lexer
from src.core.math.parser import Parser

def evaluate_str(expr_str: str, angle_unit: str = "DEG", memory: dict | None = None):
    tokens = Lexer(expr_str).tokenize()
    ast = Parser(tokens).parse()
    evaluator = Evaluator(angle_unit=angle_unit, memory=memory)
    return evaluator.evaluate(ast)

def test_basic_arithmetic_and_precedence():
    res = evaluate_str("3 + 5 × 2")
    assert res.exact == 13
    assert res.numeric == 13.0

def test_negative_numbers():
    res = evaluate_str("−5 + 2")
    assert res.exact == -3
    assert res.numeric == -3.0

def test_exact_fractions():
    res1 = evaluate_str("1/2 + 1/3")
    assert res1.exact == sp.Rational(5, 6)

    res2 = evaluate_str("7/3 − 1/3")
    assert res2.exact == 2

def test_exact_radicals():
    res = evaluate_str("√12")
    assert res.exact == 2 * sp.sqrt(3)

    res2 = evaluate_str("√2 + √8")
    assert res2.exact == 3 * sp.sqrt(2)

def test_trigonometry_in_different_angle_modes():
    # DEG
    res_deg = evaluate_str("sin(30)", angle_unit="DEG")
    assert res_deg.exact == sp.Rational(1, 2)

    res_cos45 = evaluate_str("cos(45)", angle_unit="DEG")
    assert res_cos45.exact == sp.sqrt(2) / 2

    res_tan45 = evaluate_str("tan(45)", angle_unit="DEG")
    assert res_tan45.exact == 1

    # RAD
    res_rad = evaluate_str("sin(π ÷ 6)", angle_unit="RAD")
    assert res_rad.exact == sp.Rational(1, 2)

    # GRA
    res_gra = evaluate_str("sin(50)", angle_unit="GRA")
    assert res_gra.exact == sp.sqrt(2) / 2

def test_inverse_trigonometry():
    res = evaluate_str("asin(0.5)", angle_unit="DEG")
    assert round(res.numeric, 2) == 30.0

def test_hyperbolic_functions():
    res_sinh = evaluate_str("sinh(0)")
    assert res_sinh.exact == 0
    res_cosh = evaluate_str("cosh(0)")
    assert res_cosh.exact == 1

def test_logarithms_and_exponentials():
    res_ln = evaluate_str("ln(e)")
    assert res_ln.exact == 1

    res_log = evaluate_str("log(100)")
    assert res_log.exact == 2

    # Arbitrary base log(base, value)
    res_log_base = evaluate_str("log(2, 8)")
    assert res_log_base.exact == 3

    res_exp = evaluate_str("eˣ(1)")
    assert res_exp.exact == sp.E

def test_factorials_and_combinatorics():
    assert evaluate_str("5!").exact == 120
    assert evaluate_str("0!").exact == 1
    assert evaluate_str("5nPr2").exact == 20
    assert evaluate_str("5nCr2").exact == 10

def test_percentages():
    assert evaluate_str("100 + 10%").exact == 110
    assert evaluate_str("100 − 10%").exact == 90
    assert evaluate_str("50 × 10%").exact == 5

def test_memory_variables_and_ans():
    mem = {"A": 10, "B": 20, "Ans": 5}
    assert evaluate_str("A + B", memory=mem).exact == 30
    assert evaluate_str("Ans × 2", memory=mem).exact == 10

def test_polar_and_rectangular_coordinates():
    mem = {}
    r = evaluate_str("Pol(1, 1)", angle_unit="DEG", memory=mem).numeric
    assert round(r, 6) == round(math.sqrt(2), 6)
    assert round(float(mem["X"]), 6) == round(math.sqrt(2), 6)
    assert round(float(mem["Y"]), 6) == 45.0

    x = evaluate_str("Rec(√2, 45)", angle_unit="DEG", memory=mem).numeric
    assert round(x, 6) == 1.0
    assert round(float(mem["X"]), 6) == 1.0
    assert round(float(mem["Y"]), 6) == 1.0

def test_calculus_derivative_integral_summation():
    # d/dx(X^2, 3) = 6
    diff_res = evaluate_str("d/dx(X^2, 3)")
    assert diff_res.exact == 6

    # ∫(X^2, 0, 3) = 9
    int_res = evaluate_str("∫(X^2, 0, 3)")
    assert int_res.exact == 9

    # Σ(X, 1, 10) = 55
    sum_res = evaluate_str("Σ(X, 1, 10)")
    assert sum_res.exact == 55

def test_domain_and_math_errors():
    with pytest.raises(MathError):
        evaluate_str("5 ÷ 0")

    with pytest.raises(MathError):
        evaluate_str("√(−4)")

    with pytest.raises(MathError):
        evaluate_str("tan(90)", angle_unit="DEG")

    with pytest.raises(MathError):
        evaluate_str("ln(0)")

    with pytest.raises(MathError):
        evaluate_str("70!")  # Over 69!
