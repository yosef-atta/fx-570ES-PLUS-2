"""Unit tests for MATRIX Mode (matrix storage and operations)."""
import sympy as sp
from src.core.modes.matrix_engine import MatrixEngine

def test_matrix_addition_and_multiplication():
    engine = MatrixEngine()
    engine.set_matrix("MatA", [[1, 2], [3, 4]])
    engine.set_matrix("MatB", [[5, 6], [7, 8]])

    # MatA + MatB = [[6, 8], [10, 12]]
    m_sum = engine.add("MatA", "MatB")
    assert m_sum.tolist() == [[6, 8], [10, 12]]

    # MatA * MatB = [[19, 22], [43, 50]]
    m_prod = engine.mul("MatA", "MatB")
    assert m_prod.tolist() == [[19, 22], [43, 50]]

def test_matrix_determinant_transpose_inverse():
    engine = MatrixEngine()
    engine.set_matrix("MatA", [[1, 2], [3, 4]])

    # det(MatA) = 1*4 - 2*3 = -2
    assert engine.det("MatA") == -2

    # Trn(MatA) = [[1, 3], [2, 4]]
    assert engine.trn("MatA").tolist() == [[1, 3], [2, 4]]

    # MatA^-1 = [[-2, 1], [1.5, -0.5]]
    inv_m = engine.inverse("MatA")
    assert inv_m.tolist() == [[-2, 1], [sp.Rational(3, 2), sp.Rational(-1, 2)]]
