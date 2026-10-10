"""Comprehensive QA test suite for error conditions, domain boundary cases, and mode transitions.
Validates Casio fx-570ES PLUS-2 diagnostic error behaviors:
- Math ERROR: Division by zero, domain violations, overflow
- Syntax ERROR: Malformed expressions, unbalanced operators, empty arguments
- Dim ERROR: Matrix / Vector size mismatches and invalid operations
- Argument ERROR: Out-of-bounds CONST and CONV codes
- Can't Solve: Non-convergent numerical root searches
- Key blocking and error locus (◀ / ▶) navigation
"""
import pytest
from src.core.controller import Controller

def test_math_error_domain_violations():
    c = Controller()

    # 1. Division by zero: 1 ÷ 0
    c.press("1")
    c.press("divide")
    c.press("0")
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"

    # 2. ln(0) domain violation
    c.press("ac")
    c.press("ln")
    c.press("0")
    c.press("rparen")
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"

    # 3. asin(2) domain violation (|x| > 1)
    c.press("ac")
    c.press("shift")
    c.press("sin")
    c.press("2")
    c.press("rparen")
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"

    # 4. tan(90) in DEG mode (pole at 90°)
    c.press("ac")
    c.press("tan")
    c.press("9")
    c.press("0")
    c.press("rparen")
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"

    # 5. Negative factorial: (-1)!
    c.press("ac")
    c.press("lparen")
    c.press("negative")
    c.press("1")
    c.press("rparen")
    c.press("factorial")
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"

    # 6. √(-4) in COMP mode
    c.press("ac")
    c.press("sqrt")
    c.press("negative")
    c.press("4")
    c.press("rparen")
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"


def test_cmplx_mode_allows_complex_numbers():
    c = Controller()
    c.press("mode")
    c.press("2")  # CMPLX mode
    assert c.state.mode == "CMPLX"

    # In CMPLX mode, √(-4) should evaluate to 2i without Math ERROR
    c.press("sqrt")
    c.press("negative")
    c.press("4")
    c.press("rparen")
    c.press("equals")
    assert not c.state.error_state
    assert "2i" in c.state.result or "2*I" in c.state.result or "2" in c.state.result


def test_syntax_errors_and_error_locus():
    c = Controller()

    # Malformed syntax: 5 + × 2
    for k in ("5", "add", "multiply", "2", "equals"):
        c.press(k)
    assert c.state.error_state
    assert c.state.error_message == "Syntax ERROR"
    assert "[AC]:Cancel" in c.state.result

    # Error screen blocks normal keys
    pos_before = c.state.cursor_position
    expr_before = c.state.expression
    c.press("7")
    c.press("sin")
    assert c.state.error_state
    assert c.state.expression == expr_before

    # Press right (▶) jumps to error position and clears error screen
    c.press("right")
    assert not c.state.error_state
    assert c.state.error_message == ""
    assert c.state.cursor_position == 2  # At the '×' operator
    assert c.state.expression == expr_before

    # Test AC clears error and resets input
    c.press("multiply")
    c.press("equals")
    assert c.state.error_state
    c.press("ac")
    assert not c.state.error_state
    assert c.state.expression == ""
    assert c.state.cursor_position == 0


def test_dimension_errors_matrix_and_vector():
    c = Controller()

    # 1. MATRIX Mode Dim ERROR: Add 2x2 and 3x3
    c.press("mode")
    c.press("6")  # MATRIX mode
    assert c.state.mode == "MATRIX"
    c.matrix_engine.set_matrix("MatA", [[1, 2], [3, 4]])
    c.matrix_engine.set_matrix("MatB", [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    c.state.expression = "MatA+MatB"
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Dim ERROR"

    # 2. MATRIX Mode singular matrix inverse: Math ERROR
    c.press("ac")
    c.matrix_engine.set_matrix("MatC", [[1, 2], [2, 4]])  # Det = 0
    c.state.expression = "MatC⁻¹"
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Math ERROR"

    # 3. VECTOR Mode Dim ERROR: Add 2D and 3D
    c.press("ac")
    c.press("mode")
    c.press("8")  # VECTOR mode
    assert c.state.mode == "VECTOR"
    c.vector_engine.set_vector("VctA", [1, 2])
    c.vector_engine.set_vector("VctB", [1, 2, 3])
    c.state.expression = "VctA+VctB"
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Dim ERROR"

    # 4. VECTOR Mode Dim ERROR: Dot product between 2D and 3D
    c.press("ac")
    c.state.expression = "VctA • VctB"
    c.press("equals")
    assert c.state.error_state
    assert c.state.error_message == "Dim ERROR"


def test_argument_and_cant_solve_errors():
    c = Controller()

    # 1. CONST out of bounds: 99
    c.press("shift")
    c.press("7")  # CONST prompt
    assert c.state.prompt_name == "CONST"
    c.press("9")
    c.press("9")
    assert c.state.error_state
    assert c.state.error_message == "Argument ERROR"

    # 2. CONV out of bounds: 99
    c.press("ac")
    c.press("shift")
    c.press("8")  # CONV prompt
    assert c.state.prompt_name == "CONV"
    c.press("9")
    c.press("9")
    assert c.state.error_state
    assert c.state.error_message == "Argument ERROR"

    # 3. SOLVE on equation without X or impossible: 1 = 0
    c.press("ac")
    c.state.expression = "1=0"
    c.press("shift")
    c.press("calc")  # SOLVE
    assert c.state.error_state
    assert c.state.error_message == "Can't Solve"
