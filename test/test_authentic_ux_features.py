"""Tests for authentic Casio fx-570ES PLUS 2nd Edition UX, display and recurring decimal features."""
from fractions import Fraction
from PySide6.QtCore import Qt
from src.core.action import Action
from src.core.controller import Controller
from src.core.state import CalculatorState
from src.core.math.lexer import Lexer
from src.core.math.parser import Parser
from src.core.math.evaluator import Evaluator
from src.ui.main_window import MainWindow
from src.ui.calculator_display import CalculatorDisplay
from src.ui.natural_canvas import render_natural_result


def evaluate_str(expr_str: str, angle_unit: str = "DEG", memory: dict | None = None):
    tokens = Lexer(expr_str).tokenize()
    ast = Parser(tokens).parse()
    evaluator = Evaluator(angle_unit=angle_unit, memory=memory)
    return evaluator.evaluate(ast)


def test_recurring_decimal_to_fraction():
    """Verify recurring decimal conversion such as .0121111 -> 109/9000."""
    res1 = evaluate_str(".0121111")
    assert res1.exact == Fraction(109, 9000)

    res2 = evaluate_str("0.012111111111")
    assert res2.exact == Fraction(109, 9000)

    res3 = evaluate_str("0.3333333333")
    assert res3.exact == Fraction(1, 3)

    res4 = evaluate_str("0.1666666666")
    assert res4.exact == Fraction(1, 6)

    res5 = evaluate_str("0.125")
    assert res5.exact == Fraction(1, 8)


def test_input_capacity_limit_99_chars():
    """Verify input buffer limit of 99 characters matching physical Casio."""
    c = Controller()
    for _ in range(120):
        c.press("1")
    assert len(c.state.expression) == 99


def test_display_horizontal_scrolling_indicators(application):
    """Verify left/right arrow indicators appear when expression overflows display window."""
    disp = CalculatorDisplay()

    # Short expression - no overflow arrows
    disp.render(CalculatorState(expression="12345", cursor_position=5))
    assert "◀" not in disp.indicators.text()
    assert "▶" not in disp.indicators.text()

    # Long expression with cursor at the end: left arrow ◀ must show
    long_expr = "1234567890" * 4  # 40 chars > 26 MAX_VISIBLE
    disp.render(CalculatorState(expression=long_expr, cursor_position=40))
    assert "◀" in disp.indicators.text()
    assert "▶" not in disp.indicators.text()

    # Cursor at the beginning: right arrow ▶ must show
    disp.render(CalculatorState(expression=long_expr, cursor_position=0))
    assert "◀" not in disp.indicators.text()
    assert "▶" in disp.indicators.text()

    # Cursor in middle: both arrows show
    disp.render(CalculatorState(expression=long_expr, cursor_position=20))
    assert "◀" in disp.indicators.text()
    assert "▶" in disp.indicators.text()
    disp.close()


def test_casio_capacity_block_cursor_and_full_indicator(application):
    """Verify Casio hardware behavior: cursor switches to block ■ at <= 10 bytes remaining, and FULL status."""
    disp = CalculatorDisplay()

    # Standard cursor under 89 characters
    state_normal = CalculatorState(expression="1" * 50, cursor_position=50)
    disp.render(state_normal)
    assert "│" in disp.expression.text()
    assert "FULL" not in disp.indicators.text()

    # Approaching capacity (89 to 98 chars): cursor switches to solid block ■
    state_near_full = CalculatorState(expression="1" * 89, cursor_position=89)
    disp.render(state_near_full)
    assert "■" in disp.expression.text()
    assert "[89/99]" in disp.indicators.text()

    # Completely full (99 chars): cursor is ■ and FULL appears in status bar
    state_full = CalculatorState(expression="1" * 99, cursor_position=99)
    disp.render(state_full)
    assert "■" in disp.expression.text()
    assert "FULL" in disp.indicators.text()
    disp.close()


def test_home_and_end_navigation():
    """Verify Home and End actions jump to beginning and end of long input."""
    c = Controller()
    c.press("1")
    c.press("2")
    c.press("3")
    assert c.state.cursor_position == 3

    # Home jumps to 0
    c.dispatch(Action.command("home"))
    assert c.state.cursor_position == 0

    # End jumps to end (3)
    c.dispatch(Action.command("end"))
    assert c.state.cursor_position == 3


def test_display_history_indicators(application):
    """Verify up/down history indicators ▲ and ▼ show when history is available."""
    disp = CalculatorDisplay()
    state = CalculatorState(expression="5", cursor_position=1)
    state.history_has_prev = True
    state.history_has_next = True
    disp.render(state)
    assert "▲" in disp.indicators.text()
    assert "▼" in disp.indicators.text()
    disp.close()


def test_natural_stacked_fraction_rendering():
    """Verify 2D stacked fraction HTML generation in MthIO mode."""
    rendered = render_natural_result("109/9000", is_natural=True)
    assert "109" in rendered
    assert "9000" in rendered
    assert "border-bottom" in rendered

    # In LineIO mode, remains 109/9000
    rendered_line = render_natural_result("109/9000", is_natural=False)
    assert rendered_line == "109/9000"


def test_replay_pad_and_branding(application):
    """Verify Replay D-Pad and authentic Casio branding exist and operate."""
    win = MainWindow()
    assert win.findChild(type(win.keypad.buttons["up"])) is not None
    assert win.keypad.buttons["up"].text() == "▲"
    assert win.keypad.buttons["down"].text() == "▼"
    assert win.keypad.buttons["left"].text() == "◀"
    assert win.keypad.buttons["right"].text() == "▶"

    # Verify D-Pad clicks move cursor
    win.controller.press("1")
    win.controller.press("2")
    win.controller.press("3")
    assert win.controller.state.cursor_position == 3
    win.keypad.buttons["left"].click()
    assert win.controller.state.cursor_position == 2
    win.keypad.buttons["right"].click()
    assert win.controller.state.cursor_position == 3

    # Check authentic branding
    assert win.findChild(object, "brand_casio") is not None
    assert win.findChild(object, "brand_model") is not None
    assert win.findChild(object, "brand_vpam") is not None
    assert win.findChild(object, "brand_edition") is not None
    win.close()
