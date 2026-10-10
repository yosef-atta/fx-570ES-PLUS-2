"""Integration tests directly validating scenarios against the official Casio fx-570ES PLUS User's Guide."""
import pytest
from src.core.controller import Controller

def test_casio_basic_arithmetic_and_negation():
    c = Controller()
    for k in ("3", "add", "5", "multiply", "2", "equals"):
        c.press(k)
    assert c.state.result == "13"

    c.press("ac")
    for k in ("negative", "5", "add", "2", "equals"):
        c.press(k)
    assert c.state.result == "-3"

def test_casio_exact_fractions_and_sd_toggle():
    c = Controller()
    for k in ("1", "fraction", "2", "add", "1", "fraction", "3", "equals"):
        c.press(k)
    assert c.state.result == "5/6"

    # Press S⇔D
    c.press("sd")
    assert c.state.result.startswith("0.833333")

    # Press S⇔D again to return to fraction
    c.press("sd")
    assert c.state.result == "5/6"

def test_casio_exact_radical_simplification():
    c = Controller()
    for k in ("sqrt", "1", "2", "rparen", "equals"):
        c.press(k)
    assert "2√3" in c.state.result

def test_casio_trigonometry_deg_and_rad():
    c = Controller()
    assert c.state.angle_unit == "DEG"
    for k in ("sin", "3", "0", "rparen", "equals"):
        c.press(k)
    assert c.state.result == "1/2"

    # Change SETUP to RAD
    c.press("shift")
    c.press("mode")  # SETUP
    c.press("4")      # RAD
    assert c.state.angle_unit == "RAD"

    c.press("ac")
    for k in ("sin", "pi", "divide", "6", "rparen", "equals"):
        c.press(k)
    assert c.state.result == "1/2"

def test_casio_factorial_and_combinatorics():
    c = Controller()
    # 5!
    for k in ("5", "factorial", "equals"):
        c.press(k)
    assert c.state.result == "120"

    # 5 nPr 2
    c.press("ac")
    for k in ("5", "shift", "subtract", "2", "equals"):  # shift + subtract is nPr
        c.press(k)
    assert c.state.result == "20"

    # 5 nCr 2
    c.press("ac")
    for k in ("5", "shift", "add", "2", "equals"):       # shift + add is nCr
        c.press(k)
    assert c.state.result == "10"

def test_casio_engineering_notation():
    c = Controller()
    for k in ("1", "2", "3", "4", "5", "equals"):
        c.press(k)
    assert c.state.result == "12345"

    c.press("eng")
    assert "12.345×10^3" in c.state.result

    c.press("shift")
    c.press("eng")  # arrow_eng
    assert "0.012345×10^6" in c.state.result

def test_casio_variable_storage_and_ans_chaining():
    c = Controller()
    # 12 -> STO A
    for k in ("1", "2", "equals"):
        c.press(k)
    c.press("shift")
    c.press("rcl")  # STO
    c.press("negative")  # Variable A
    assert c.memory.get_var("A") == 12

    # A * 2 = 24
    c.press("ac")
    c.press("alpha")
    c.press("negative")  # A
    c.press("multiply")
    c.press("2")
    c.press("equals")
    assert c.state.result == "24"

    # Auto-Ans chaining: press + 6 -> Ans + 6 = 30
    c.press("add")
    assert c.state.expression == "Ans+"
    c.press("6")
    c.press("equals")
    assert c.state.result == "30"

def test_casio_numerical_calculus():
    c = Controller()
    # d/dx(X^2, 3)
    c.press("shift")
    c.press("integral")  # d/dx
    c.press("alpha")
    c.press("rparen")    # X
    c.press("square")    # ²
    c.press("comma")
    c.press("3")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "6"

    # ∫(X^2, 0, 3)
    c.press("ac")
    c.press("integral")
    c.press("alpha")
    c.press("rparen")    # X
    c.press("square")
    c.press("comma")
    c.press("0")
    c.press("comma")
    c.press("3")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "9"

def test_casio_solve_equation():
    c = Controller()
    # X^2 = 4 -> SOLVE
    c.press("alpha")
    c.press("rparen")  # X
    c.press("square")
    c.press("alpha")
    c.press("calc")    # =
    c.press("4")
    c.press("shift")
    c.press("calc")    # SOLVE
    assert "X=2" in c.state.result
    assert "L-R=0" in c.state.result

def test_casio_error_handling_and_goto():
    c = Controller()
    # 5 ÷ 0 =
    for k in ("5", "divide", "0", "equals"):
        c.press(k)
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"

    # Press Left to jump to error
    c.press("left")
    assert not c.state.error_state
    assert c.state.expression == "5÷0"
    assert c.state.cursor_position in (1, 2)  # At operator or divisor locus
