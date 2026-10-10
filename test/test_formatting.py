"""Tests for result formatting, S⇔D switching, Fix/Sci/Norm, and ENG notation."""
import sympy as sp
from src.core.math.evaluator import EvaluationResult
from src.core.math.formatter import Formatter

def test_sd_switching_rational():
    # 7/3 has 3 representations: 7/3 (improper), 2 1/3 (mixed), 2.333333333 (decimal)
    res = EvaluationResult(sp.Rational(7, 3))
    formatter = Formatter()
    reps = formatter.get_representations(res)
    assert reps[0] == "7/3"
    assert reps[1] == "2 1/3"
    assert reps[2].startswith("2.333333")

def test_sd_switching_radicals():
    # 2√3 has 2 representations: 2√3, 3.464101615
    res = EvaluationResult(2 * sp.sqrt(3))
    formatter = Formatter()
    reps = formatter.get_representations(res)
    assert "2√3" in reps[0]
    assert reps[1].startswith("3.4641")

def test_fix_format():
    fmt = Formatter(number_format="Fix 3")
    assert fmt.format_number(1.23456) == "1.235"
    assert fmt.format_number(0) == "0.000"

def test_sci_format():
    fmt = Formatter(number_format="Sci 3")
    assert fmt.format_number(1234.5) == "1.23×10^3"

def test_norm_format():
    fmt1 = Formatter(number_format="Norm 1")
    # In Norm 1, 0.005 is < 10^-2 so formatted in scientific notation
    assert "×10^-3" in fmt1.format_number(0.005)

    fmt2 = Formatter(number_format="Norm 2")
    # In Norm 2, 0.005 is not < 10^-9 so formatted in decimal
    assert fmt2.format_number(0.005) == "0.005"

def test_engineering_notation_shifts():
    fmt = Formatter()
    # 12345 in standard ENG has exponent 3: 12.345×10^3
    assert fmt.format_number(12345, eng_shift=0) == "12.345×10^3"
    # eng_shift = -1 -> 12345×10^0
    assert fmt.format_number(12345, eng_shift=-1) == "12345×10^0"
    # eng_shift = 1 -> 0.012345×10^6
    assert fmt.format_number(12345, eng_shift=1) == "0.012345×10^6"
