"""Comprehensive tests for Mixed Fraction entry, parsing, arithmetic, and LCD display."""
import pytest
from src.core.controller import Controller
from src.core.math.lexer import Lexer
from src.core.math.parser import Parser
from src.core.math.evaluator import Evaluator
from src.core.math.ast_nodes import MixedFractionNode, FractionNode
from src.ui.natural_canvas import render_natural_math, render_natural_result


def test_mixed_fraction_lexer():
    """Verify that the Lexer tokenizes mixed fraction keywords and symbols without syntax errors."""
    for text in ["2mixed/1/3", "2 mixed/ 1/3", "2⌟1/3", "2⌟1⌟3", "2_1/3"]:
        tokens = Lexer(text).tokenize()
        assert any(t.value in ("mixed/", "⌟", "_") for t in tokens)


def test_mixed_fraction_parser_ast():
    """Verify that Parser generates MixedFractionNode correctly for various formats."""
    # 1. Infix standard mixed/
    ast1 = Parser(Lexer("2mixed/1/3").tokenize()).parse()
    assert isinstance(ast1, MixedFractionNode)
    assert ast1.whole.value == "2"
    assert ast1.numerator.value == "1"
    assert ast1.denominator.value == "3"

    # 2. Infix Casio ⌟
    ast2 = Parser(Lexer("2⌟1/3").tokenize()).parse()
    assert isinstance(ast2, MixedFractionNode)

    # 3. Infix Casio double ⌟ (2⌟1⌟3)
    ast3 = Parser(Lexer("2⌟1⌟3").tokenize()).parse()
    assert isinstance(ast3, MixedFractionNode)

    # 4. Infix underscore
    ast4 = Parser(Lexer("2_1/3").tokenize()).parse()
    assert isinstance(ast4, MixedFractionNode)

    # 5. Single separator 1⌟3 produces FractionNode(1, 3)
    ast5 = Parser(Lexer("1⌟3").tokenize()).parse()
    assert isinstance(ast5, FractionNode)
    assert ast5.numerator.value == "1"
    assert ast5.denominator.value == "3"

    # 6. Prefix mixed/ 2/1/3 and mixed/(2, 1, 3)
    ast6 = Parser(Lexer("mixed/2/1/3").tokenize()).parse()
    assert isinstance(ast6, MixedFractionNode)

    ast7 = Parser(Lexer("mixed/(2, 1, 3)").tokenize()).parse()
    assert isinstance(ast7, MixedFractionNode)


def test_mixed_fraction_evaluation():
    """Verify exact mathematical evaluation of mixed fractions."""
    ev = Evaluator()

    # 2 1/3 = 7/3
    res1 = ev.evaluate(Parser(Lexer("2mixed/1/3").tokenize()).parse())
    assert str(res1.exact) == "7/3"

    # 1 1/2 + 2 3/4 = 17/4
    res2 = ev.evaluate(Parser(Lexer("1⌟1/2 + 2⌟3/4").tokenize()).parse())
    assert str(res2.exact) == "17/4"

    # 5 1/3 - 2 2/3 = 8/3
    res3 = ev.evaluate(Parser(Lexer("5⌟1/3 - 2⌟2/3").tokenize()).parse())
    assert str(res3.exact) == "8/3"

    # 2 1/2 * 1 1/5 = 3
    res4 = ev.evaluate(Parser(Lexer("2⌟1/2 * 1⌟1/5").tokenize()).parse())
    assert str(res4.exact) == "3"

    # 3 1/2 / 1 3/4 = 2
    res5 = ev.evaluate(Parser(Lexer("3⌟1/2 ÷ 1⌟3/4").tokenize()).parse())
    assert str(res5.exact) == "2"

    # Negation: -2 1/3 = -7/3
    res6 = ev.evaluate(Parser(Lexer("−2⌟1/3").tokenize()).parse())
    assert str(res6.exact) == "-7/3"

    # Power: (1 1/2)^2 = 9/4
    res7 = ev.evaluate(Parser(Lexer("(1⌟1/2)^2").tokenize()).parse())
    assert str(res7.exact) == "9/4"


def test_mixed_fraction_controller_workflow():
    """Test full controller interaction through button presses."""
    c = Controller()

    # Enter 2 [SHIFT][■□/□] 1 [□/□] 3 [=]
    c.press("2")
    c.press("shift")
    c.press("fraction")  # Inserts ⌟
    c.press("1")
    c.press("fraction")  # Inserts /
    c.press("3")
    assert "⌟" in c.state.expression

    c.press("equals")
    assert not c.state.error_state
    # In MthIO mode, first exact representation is 7/3
    assert c.state.result == "7/3"
    assert "2 1/3" in c.state.result_representations

    # S<=>D toggles to mixed fraction 2 1/3
    c.press("sd")
    assert c.state.result == "2 1/3"

    # S<=>D toggles to decimal 2.333333333
    c.press("sd")
    assert "2.333333333" in c.state.result

    # SHIFT + S<=>D (a b/c <=> d/c) directly toggles to mixed fraction
    c.press("shift")
    c.press("sd")
    assert c.state.result == "2 1/3"

    # SHIFT + S<=>D again toggles back to improper fraction
    c.press("shift")
    c.press("sd")
    assert c.state.result == "7/3"


def test_mixed_fraction_natural_display():
    """Verify natural LCD rendering for mixed fractions."""
    # Input line formatting
    rendered_input = render_natural_math("2mixed/1/3", 0)
    assert "⌟" in rendered_input

    # Result line formatting for mixed fraction
    html_res = render_natural_result("2 1/3")
    assert "2&nbsp;" in html_res
    assert "1" in html_res
    assert "3" in html_res
    assert "border-bottom:2px solid" in html_res

    # Result line formatting for negative mixed fraction
    html_neg = render_natural_result("-2 1/3")
    assert "-2&nbsp;" in html_neg
