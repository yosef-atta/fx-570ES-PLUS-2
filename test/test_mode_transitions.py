"""Comprehensive integration tests for mode transitions and end-to-end calculations across all 8 modes."""
import sympy as sp
from src.core.controller import Controller

def test_cmplx_mode_workflow():
    c = Controller()
    # 1. Switch to CMPLX mode (Mode 2)
    c.press("mode")
    c.press("2")
    assert c.state.mode == "CMPLX"

    # 2. Enter complex calculation: 2 + 3i + 4 - 5i = 6 - 2i
    c.press("2")
    c.press("add")
    c.press("3")
    c.press("eng")  # In CMPLX mode, eng enters 'i'
    assert c.state.expression == "2+3i"
    c.press("add")
    c.press("4")
    c.press("subtract")
    c.press("5")
    c.press("eng")
    assert c.state.expression == "2+3i+4−5i"

    # Evaluate
    c.press("equals")
    assert c.state.is_evaluated
    assert c.state.result == "6-2i"

    # Toggle S<=>D for polar representation
    c.press("sd")
    assert "∠" in c.state.result

    # 3. Calculate modulus: Abs(3 + 4i) = 5
    c.press("ac")
    c.press("shift")
    c.press("lparen")  # Abs(
    c.press("3")
    c.press("add")
    c.press("4")
    c.press("eng")  # i
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "5"

    # 4. Calculate argument: arg(1 + i) = 45 in DEG mode
    c.press("ac")
    c.press("shift")
    c.press("negative")  # arg(
    c.press("1")
    c.press("add")
    c.press("eng")  # i
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "45"

    # 5. Complex conjugate: Conjg(5 - 2i) = 5 + 2i
    c.press("ac")
    c.press("shift")
    c.press("2")  # CMPLX menu
    c.press("2")  # Conjg
    c.press("5")
    c.press("subtract")
    c.press("2")
    c.press("eng")
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "5+2i"


def test_basen_mode_workflow():
    c = Controller()
    # 1. Switch to BASE-N mode (Mode 4)
    c.press("mode")
    c.press("4")
    assert c.state.mode == "BASE-N"
    assert c.state.base_n_mode == "DEC"

    # 2. Switch base to HEX using power (x^) key
    c.press("power")
    assert c.state.base_n_mode == "HEX"

    # 3. Enter hex values directly without ALPHA: FF + 1
    c.press("tan")  # F
    c.press("tan")  # F
    c.press("add")
    c.press("1")
    c.press("equals")
    assert c.state.result == "100"

    # 4. Switch result to DEC (x² key)
    c.press("square")
    assert c.state.base_n_mode == "DEC"
    assert c.state.result == "256"

    # 5. Switch result to BIN (log key)
    c.press("log")
    assert c.state.base_n_mode == "BIN"
    assert c.state.result == "100000000"

    # 6. Switch result to OCT (ln key)
    c.press("ln")
    assert c.state.base_n_mode == "OCT"
    assert c.state.result == "400"

    # 7. Bitwise operation: 1010 AND 1100 = 1000 in BIN
    c.press("ac")
    c.press("log")  # Switch to BIN
    c.press("1")
    c.press("0")
    c.press("1")
    c.press("0")
    c.press("shift")
    c.press("3")  # BASE menu
    c.press("1")  # and
    c.press("1")
    c.press("1")
    c.press("0")
    c.press("0")
    c.press("equals")
    assert c.state.result == "1000"


def test_stat_mode_workflow():
    c = Controller()
    # 1. Switch to STAT mode (Mode 3)
    c.press("mode")
    c.press("3")
    assert c.state.mode == "STAT"
    assert c.state.table_editor_active

    # 2. Enter 3 data points: 10, 20, 30
    c.press("1")
    c.press("0")
    c.press("equals")
    c.press("2")
    c.press("0")
    c.press("equals")
    c.press("3")
    c.press("0")
    c.press("equals")

    # 3. Leave editor with AC
    c.press("ac")
    assert not c.state.table_editor_active

    # 4. Calculate Mean x̄ via STAT menu (Shift + 1 -> Var -> x̄)
    c.press("shift")
    c.press("1")  # STAT menu
    c.press("4")  # Var
    c.press("1")  # x̄
    assert c.state.result == "20"

    # 5. Calculate Sum Σx via STAT menu (Shift + 1 -> Sum -> Σx)
    c.press("shift")
    c.press("1")  # STAT menu
    c.press("3")  # Sum
    c.press("2")  # Σx
    assert c.state.result == "60"

    # 6. Calculate Sample Std Dev sx via STAT menu (Shift + 1 -> Var -> sx)
    c.press("shift")
    c.press("1")
    c.press("4")  # Var
    c.press("3")  # sx
    assert c.state.result == "10"


def test_eqn_mode_workflow():
    c = Controller()
    # 1. Switch to EQN mode (Mode 5)
    c.press("mode")
    c.press("5")
    assert c.state.mode == "EQN"
    assert c.state.table_editor_active

    # 2. Select quadratic: aX² + bX + c = 0
    c.state.active_sub_mode = "aX²+bX+c=0"
    c.state.grid_headers = ["a", "b", "c"]
    c.state.grid_data = [["0", "0", "0"]]
    c.state.grid_row = 0
    c.state.grid_col = 0

    # Solve X² - 5X + 6 = 0: a=1, b=-5, c=6
    c.press("1")
    c.press("equals")
    c.press("negative")
    c.press("5")
    c.press("equals")
    c.press("6")
    c.press("equals")  # Triggers solve

    assert not c.state.table_editor_active
    assert c.state.is_evaluated
    assert "X1 = 3" in c.state.result_representations
    assert "X2 = 2" in c.state.result_representations


def test_matrix_mode_workflow():
    c = Controller()
    # 1. Switch to MATRIX mode (Mode 6)
    c.press("mode")
    c.press("6")
    assert c.state.mode == "MATRIX"

    # Populate MatA and MatB
    c.matrix_engine.set_matrix("MatA", [[1, 2], [3, 4]])
    c.matrix_engine.set_matrix("MatB", [[5, 6], [7, 8]])

    # 2. Calculate MatA + MatB
    c.press("shift")
    c.press("4")  # MATRIX menu
    c.press("3")  # MatA
    c.press("add")
    c.press("shift")
    c.press("4")
    c.press("4")  # MatB
    c.press("equals")
    assert c.state.result == "[[6, 8], [10, 12]]"

    # 3. Calculate det(MatA)
    c.press("ac")
    c.press("shift")
    c.press("4")  # MATRIX menu
    c.press("7")  # det(
    c.press("shift")
    c.press("4")
    c.press("3")  # MatA
    c.press("rparen")
    c.press("equals")
    assert c.state.result == "-2"


def test_vector_mode_workflow():
    c = Controller()
    # 1. Switch to VECTOR mode (Mode 8)
    c.press("mode")
    for _ in range(7):
        c.press("down")
    c.press("2")  # 8 is VECTOR on page 1
    assert c.state.mode == "VECTOR"

    # Populate VctA and VctB
    c.vector_engine.set_vector("VctA", [1, 2, 3])
    c.vector_engine.set_vector("VctB", [4, 5, 6])

    # 2. Dot Product: VctA • VctB = 32
    c.press("shift")
    c.press("5")  # VECTOR menu
    c.press("3")  # VctA
    c.press("shift")
    c.press("5")
    c.press("7")  # Dot
    c.press("shift")
    c.press("5")
    c.press("4")  # VctB
    c.press("equals")
    assert float(c.state.result) == 32.0

    # 3. Cross Product: VctA × VctB = [-3, 6, -3]
    c.press("ac")
    c.press("shift")
    c.press("5")  # VctA
    c.press("3")
    c.press("multiply")
    c.press("shift")
    c.press("5")
    c.press("4")  # VctB
    c.press("equals")
    assert c.state.result == "[-3, 6, -3]"


def test_table_mode_workflow():
    c = Controller()
    # 1. Switch to TABLE mode (Mode 7)
    c.press("mode")
    for _ in range(6):
        c.press("down")
    c.press("1")  # TABLE
    assert c.state.mode == "TABLE"

    # 2. Enter function f(X) = X^2
    c.press("alpha")
    c.press("rparen")  # X
    c.press("square")  # ^2
    c.press("equals")

    assert c.state.table_editor_active
    assert c.state.grid_headers == ["", "X", "F(X)"]
    assert len(c.state.grid_data) == 5  # Start=1, End=5, Step=1
    assert c.state.grid_data[0] == ["1", "1.0", "1"]
    assert c.state.grid_data[1] == ["2", "2.0", "4"]
    assert c.state.grid_data[2] == ["3", "3.0", "9"]
