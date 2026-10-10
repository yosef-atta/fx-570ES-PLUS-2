"""Tests for SOLVE equation root finder and CALC variable extraction."""
import pytest
from src.core.math.errors import CantSolveError
from src.core.math.lexer import Lexer
from src.core.math.parser import Parser
from src.core.math.solver import Solver

def parse_expr(s: str):
    tokens = Lexer(s).tokenize()
    return Parser(tokens).parse()

def test_solve_linear_equation():
    # 2X − 6 = 0 -> X = 3
    node = parse_expr("2X − 6 = 0")
    solver = Solver()
    res = solver.solve(node, initial_guess=0.0)
    assert round(res.solution, 4) == 3.0
    assert abs(res.residual) < 1e-6

def test_solve_quadratic_equation():
    # X^2 = 4 -> X = 2 (with guess=1.0)
    node = parse_expr("X^2 = 4")
    solver = Solver()
    res = solver.solve(node, initial_guess=1.0)
    assert round(res.solution, 4) == 2.0
    assert abs(res.residual) < 1e-6

def test_extract_variables_for_calc():
    node = parse_expr("3A + 2B − X")
    vars_found = Solver.extract_variables(node)
    assert vars_found == ["A", "B", "X"]

def test_cant_solve_error():
    # X^2 + 10 = 0 (no real root in COMP)
    node = parse_expr("X^2 + 10 = 0")
    solver = Solver()
    with pytest.raises(CantSolveError):
        solver.solve(node, initial_guess=0.0)
