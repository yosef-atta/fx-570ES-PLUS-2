"""Tests for expression parsing and operator precedence."""
import pytest
from src.core.math.ast_nodes import (
    BinaryOpNode, UnaryOpNode, NumberNode, VariableNode,
    FunctionCallNode, EquationNode, MultiStatementNode,
    DerivativeNode, IntegralNode, SummationNode, PostfixOpNode
)
from src.core.math.errors import SyntaxError
from src.core.math.lexer import Lexer
from src.core.math.parser import Parser

def parse_str(text: str):
    tokens = Lexer(text).tokenize()
    return Parser(tokens).parse()

def test_precedence_addition_and_multiplication():
    # 3 + 5 × 2 -> (+) with left=3, right=(5 × 2)
    node = parse_str("3 + 5 × 2")
    assert isinstance(node, BinaryOpNode)
    assert node.op == "+"
    assert isinstance(node.left, NumberNode) and node.left.value == "3"
    assert isinstance(node.right, BinaryOpNode) and node.right.op == "×"
    assert node.right.left.value == "5"
    assert node.right.right.value == "2"

def test_powers_precedence_over_unary_minus():
    # −3^2 -> UnaryOp(−, (3 ^ 2))
    node = parse_str("−3^2")
    assert isinstance(node, UnaryOpNode)
    assert node.op == "−"
    assert isinstance(node.operand, BinaryOpNode)
    assert node.operand.op == "^"
    assert node.operand.left.value == "3"
    assert node.operand.right.value == "2"

def test_parenthesized_negation():
    # (−3)^2 -> BinaryOp(^, UnaryOp(−, 3), 2)
    node = parse_str("(−3)^2")
    assert isinstance(node, BinaryOpNode)
    assert node.op == "^"
    assert isinstance(node.left, UnaryOpNode)
    assert node.left.operand.value == "3"
    assert node.right.value == "2"

def test_auto_closing_parentheses():
    # sin(30 -> FunctionCallNode(sin, [30])
    node = parse_str("sin(30")
    assert isinstance(node, FunctionCallNode)
    assert node.name == "sin"
    assert len(node.args) == 1
    assert node.args[0].value == "30"

def test_multi_statement_and_equation():
    # A=5 : X^2 = 4
    node = parse_str("A=5 : X^2 = 4")
    assert isinstance(node, MultiStatementNode)
    assert len(node.statements) == 2
    eq1 = node.statements[0]
    eq2 = node.statements[1]
    assert isinstance(eq1, EquationNode)
    assert isinstance(eq1.left, VariableNode) and eq1.left.name == "A"
    assert isinstance(eq2, EquationNode)
    assert isinstance(eq2.left, BinaryOpNode) and eq2.left.op == "^"

def test_combinatorics_precedence():
    # 2 + 5nPr2 -> (+) left=2, right=(5 nPr 2)
    node = parse_str("2 + 5nPr2")
    assert isinstance(node, BinaryOpNode)
    assert node.op == "+"
    assert isinstance(node.right, BinaryOpNode)
    assert node.right.op == "nPr"

def test_calculus_nodes():
    # d/dx(X^2, 3)
    d = parse_str("d/dx(X^2, 3)")
    assert isinstance(d, DerivativeNode)
    assert d.variable == "X"
    assert d.at_point.value == "3"

    # ∫(X^2, 0, 3)
    integ = parse_str("∫(X^2, 0, 3)")
    assert isinstance(integ, IntegralNode)
    assert integ.lower.value == "0"
    assert integ.upper.value == "3"

    # Σ(X, 1, 10)
    sigma = parse_str("Σ(X, 1, 10)")
    assert isinstance(sigma, SummationNode)
    assert sigma.lower.value == "1"
    assert sigma.upper.value == "10"

def test_syntax_error_unbalanced_parenthesis():
    with pytest.raises(SyntaxError):
        parse_str("(2 + 3 ×")
