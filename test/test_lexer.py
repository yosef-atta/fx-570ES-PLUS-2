"""Tests for lexer and mathematical tokenization."""
import pytest
from src.core.math.errors import SyntaxError
from src.core.math.lexer import Lexer
from src.core.math.tokens import TokenType

def test_tokenize_basic_numbers_and_arithmetic():
    lexer = Lexer("12 + 34.5 − 6 × 7 ÷ 8")
    tokens = lexer.tokenize()
    types = [t.type for t in tokens]
    assert types == [
        TokenType.NUMBER, TokenType.PLUS,
        TokenType.NUMBER, TokenType.MINUS,
        TokenType.NUMBER, TokenType.MULTIPLY,
        TokenType.NUMBER, TokenType.DIVIDE,
        TokenType.NUMBER, TokenType.EOF
    ]
    assert tokens[0].value == "12"
    assert tokens[2].value == "34.5"

def test_tokenize_unary_minus():
    lexer = Lexer("−5 + (−3) × −2")
    tokens = lexer.tokenize()
    # Initial minus is NEG
    assert tokens[0].type == TokenType.NEG
    # After ( is NEG
    assert tokens[4].type == TokenType.NEG
    # After × is NEG
    assert tokens[8].type == TokenType.NEG

def test_implicit_multiplication():
    # 2π
    t1 = Lexer("2π").tokenize()
    assert [t.type for t in t1] == [TokenType.NUMBER, TokenType.MULTIPLY, TokenType.PI, TokenType.EOF]

    # 3X
    t2 = Lexer("3X").tokenize()
    assert [t.type for t in t2] == [TokenType.NUMBER, TokenType.MULTIPLY, TokenType.VARIABLE, TokenType.EOF]

    # 2(3)
    t3 = Lexer("2(3)").tokenize()
    assert [t.type for t in t3] == [
        TokenType.NUMBER, TokenType.MULTIPLY, TokenType.LPAREN, TokenType.NUMBER, TokenType.RPAREN, TokenType.EOF
    ]

    # (2)(3)
    t4 = Lexer("(2)(3)").tokenize()
    assert [t.type for t in t4] == [
        TokenType.LPAREN, TokenType.NUMBER, TokenType.RPAREN,
        TokenType.MULTIPLY,
        TokenType.LPAREN, TokenType.NUMBER, TokenType.RPAREN,
        TokenType.EOF
    ]

    # 2sin(30)
    t5 = Lexer("2sin(30)").tokenize()
    assert [t.type for t in t5] == [
        TokenType.NUMBER, TokenType.MULTIPLY, TokenType.SIN,
        TokenType.LPAREN, TokenType.NUMBER, TokenType.RPAREN,
        TokenType.EOF
    ]

def test_special_powers_and_postfix():
    # x², x³, x⁻¹
    t = Lexer("5² + 4³ − 2⁻¹").tokenize()
    assert tokens_to_str(t) == "5 ^ 2 + 4 ^ 3 - 2 ^ ( − 1 )"

def test_scientific_notation():
    t = Lexer("2.5×10^3").tokenize()
    assert [x.type for x in t] == [TokenType.NUMBER, TokenType.EXP10, TokenType.NUMBER, TokenType.EOF]

def test_calculus_and_symbols():
    t = Lexer("d/dx(X^2, 3) + ∫(X, 0, 1) + Σ(X, 1, 10)").tokenize()
    types = [x.type for x in t]
    assert TokenType.DERIVATIVE in types
    assert TokenType.INTEGRAL in types
    assert TokenType.SUMMATION in types

def test_invalid_character_raises_syntax_error():
    with pytest.raises(SyntaxError) as exc_info:
        Lexer("2 @ 3").tokenize()
    assert exc_info.value.position == 2

def test_multi_statement_and_relations():
    t = Lexer("A=5: B=A×2").tokenize()
    types = [x.type for x in t]
    assert TokenType.EQUALS in types
    assert TokenType.COLON in types

def test_combinatorics_and_random():
    t = Lexer("5nPr2 + 5nCr2 + Ran# + RanInt#(1, 6)").tokenize()
    types = [x.type for x in t]
    assert TokenType.NPR in types
    assert TokenType.NCR in types
    assert TokenType.RAN_HASH in types
    assert TokenType.RAN_INT in types

def test_dms_tokens():
    t = Lexer("2°20°30°").tokenize()
    types = [x.type for x in t]
    assert types.count(TokenType.DMS) == 3

def tokens_to_str(tokens):
    return " ".join(t.value for t in tokens if t.type != TokenType.EOF)
