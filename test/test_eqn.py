"""Unit tests for EQN Mode (linear systems and polynomial roots)."""
from src.core.modes.eqn_engine import EqnEngine

def test_eqn_simultaneous_2_unknowns():
    # 2X + 3Y = 8
    # X - Y = -1
    # Solution: X = 1, Y = 2
    sol = EqnEngine.solve_linear_2(2, 3, 8, 1, -1, -1)
    assert sol.status == "Unique"
    assert round(sol.x, 4) == 1.0
    assert round(sol.y, 4) == 2.0

def test_eqn_simultaneous_3_unknowns():
    # X + Y + Z = 6
    # 2Y + 5Z = -4
    # 2X + 5Y - Z = 27
    sol = EqnEngine.solve_linear_3(
        (1, 1, 1, 6),
        (0, 2, 5, -4),
        (2, 5, -1, 27)
    )
    assert sol.status == "Unique"
    assert round(sol.x, 2) == 5.0
    assert round(sol.y, 2) == 3.0
    assert round(sol.z, 2) == -2.0

def test_eqn_quadratic_roots_and_vertex():
    # X² - 5X + 6 = 0 -> roots 3, 2. Vertex at X = 2.5, Y = -0.25 (Min)
    sol = EqnEngine.solve_quadratic(1, -5, 6)
    assert 3.0 in sol.roots
    assert 2.0 in sol.roots
    assert sol.x_vertex == 2.5
    assert sol.y_vertex == -0.25
    assert sol.vertex_type == "Min"

def test_eqn_quadratic_complex_roots():
    # X² + 1 = 0 -> roots i, -i
    sol = EqnEngine.solve_quadratic(1, 0, 1)
    assert 1j in sol.roots
    assert -1j in sol.roots

def test_eqn_cubic_roots():
    # X³ - 6X² + 11X - 6 = 0 -> roots 1, 2, 3
    sol = EqnEngine.solve_cubic(1, -6, 11, -6)
    rounded_roots = [round(r.real if isinstance(r, complex) else r, 2) for r in sol.roots]
    assert 1.0 in rounded_roots
    assert 2.0 in rounded_roots
    assert 3.0 in rounded_roots
