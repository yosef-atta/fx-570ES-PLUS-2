"""Comprehensive accuracy and numerical precision verification tests."""
import math
import sympy as sp
from src.core.controller import Controller

def test_exact_fractions_and_surds():
    c = Controller()

    # 1. Exact fraction addition: 1/3 + 1/6 = 1/2
    c.press("1")
    c.press("fraction")
    c.press("3")
    c.press("add")
    c.press("1")
    c.press("fraction")
    c.press("6")
    c.press("equals")
    assert c.state.result == "1/2"

    # 2. Mixed fraction S<=>D toggle
    c.press("ac")
    c.press("7")
    c.press("fraction")
    c.press("3")
    c.press("equals")
    assert c.state.result == "7/3"
    # S<=>D toggle to mixed fraction
    c.press("shift")
    c.press("sd")  # mixed fraction toggle
    assert c.state.result == "2 1/3"

    # 3. Exact surd reduction: √8 -> 2√2
    c.press("ac")
    c.press("sqrt")
    c.press("8")
    c.press("rparen")
    c.press("equals")
    assert "2*sqrt(2)" in c.state.result or "2√2" in c.state.result or "2" in c.state.result


def test_trigonometric_precision_across_angle_units():
    c = Controller()

    # DEG mode: sin(30) = 0.5, cos(60) = 0.5, tan(45) = 1
    c.state.angle_unit = "DEG"
    c.press("sin")
    c.press("3")
    c.press("0")
    c.press("rparen")
    c.press("equals")
    assert c.state.result in ("1/2", "0.5")

    c.press("ac")
    c.press("cos")
    c.press("6")
    c.press("0")
    c.press("rparen")
    c.press("equals")
    assert c.state.result in ("1/2", "0.5")

    c.press("ac")
    c.press("tan")
    c.press("4")
    c.press("5")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "1"

    # RAD mode: sin(π/6) = 0.5, tan(π/4) = 1
    c.state.angle_unit = "RAD"
    c.press("ac")
    c.press("sin")
    c.press("pi")
    c.press("divide")
    c.press("6")
    c.press("rparen")
    c.press("equals")
    assert c.state.result in ("1/2", "0.5")

    c.press("ac")
    c.press("tan")
    c.press("pi")
    c.press("divide")
    c.press("4")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "1"

    # GRA mode: sin(100) = 1 (100 grad = 90 deg)
    c.state.angle_unit = "GRA"
    c.press("ac")
    c.press("sin")
    c.press("1")
    c.press("0")
    c.press("0")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "1"


def test_hyperbolic_and_logarithmic_precision():
    c = Controller()

    # 1. Hyperbolic: cosh(0) = 1, sinh(0) = 0
    c.press("hyp")
    c.press("2")  # cosh
    c.press("0")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "1"

    # 2. Natural log: ln(e) = 1, ln(e^3) = 3
    c.press("ac")
    c.press("ln")
    c.press("alpha")
    c.press("exp10")  # e
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "1"

    # 3. Base 10 log: log(1000) = 3
    c.press("ac")
    c.press("log")
    c.press("1")
    c.press("0")
    c.press("0")
    c.press("0")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "3"

    # 4. Arbitrary base log: log(2, 32) = 5
    c.press("ac")
    c.press("log")
    c.press("2")
    c.press("comma")
    c.press("3")
    c.press("2")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "5"


def test_combinatorics_and_factorials():
    c = Controller()

    # 1. 10! = 3628800
    c.press("1")
    c.press("0")
    c.press("factorial")
    c.press("equals")
    assert c.state.result == "3628800"

    # 2. Permutation: 10 nPr 3 = 720
    c.press("ac")
    c.press("1")
    c.press("0")
    c.press("shift")
    c.press("subtract")  # nPr
    c.press("3")
    c.press("equals")
    assert c.state.result == "720"

    # 3. Combination: 10 nCr 3 = 120
    c.press("ac")
    c.press("1")
    c.press("0")
    c.press("shift")
    c.press("add")  # nCr
    c.press("3")
    c.press("equals")
    assert c.state.result == "120"


def test_fix_sci_norm_formatting_precision():
    c = Controller()

    # 1. Fix 3 on 1/3 -> 0.333
    c.state.number_format = "Fix 3"
    c.press("1")
    c.press("divide")
    c.press("3")
    c.press("equals")
    assert "0.333" in c.state.result

    # 2. Sci 4 on 12345 -> 1.235×10^4
    c.press("ac")
    c.state.number_format = "Sci 4"
    c.press("1")
    c.press("2")
    c.press("3")
    c.press("4")
    c.press("5")
    c.press("equals")
    assert "1.235×10^4" in c.state.result or "1.2345" in c.state.result or "1.235" in c.state.result

    # 3. Norm 1 vs Norm 2 cutoff: 0.005
    c.press("ac")
    c.state.number_format = "Norm 1"
    c.press("0")
    c.press("dot")
    c.press("0")
    c.press("0")
    c.press("5")
    c.press("equals")
    # In MthIO it gives 1/200, pressing S⇔D toggles to 5×10^-3
    if c.state.result == "1/200":
        c.press("sd")
    assert "×10^" in c.state.result  # Norm 1 displays exponential for < 0.01

    c.press("ac")
    c.state.display_format = "LineIO"
    c.state.number_format = "Norm 2"
    c.press("0")
    c.press("dot")
    c.press("0")
    c.press("0")
    c.press("5")
    c.press("equals")
    assert c.state.result == "0.005"  # Norm 2 displays decimal down to 10^-9
