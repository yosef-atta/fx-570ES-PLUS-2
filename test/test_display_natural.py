"""Tests for Natural Textbook Display rendering and 2D math layout."""
from src.core.state import CalculatorState
from src.ui.calculator_display import CalculatorDisplay
from src.ui.natural_canvas import render_natural_math

def test_natural_math_rendering_powers_and_roots():
    # Power
    rendered = render_natural_math("X^2", 3, is_natural=True)
    assert "<sup>2</sup>" in rendered

    # Square symbol
    rendered_sq = render_natural_math("5²", 2, is_natural=True)
    assert "<sup>2</sup>" in rendered_sq

    # Radical
    rendered_sqrt = render_natural_math("√(16)", 5, is_natural=True)
    assert "&radic;" in rendered_sqrt

def test_line_io_rendering():
    # In LineIO, no HTML tags added
    rendered = render_natural_math("X^2", 3, is_natural=False)
    assert "<sup>" not in rendered
    assert "X^2" in rendered

def test_display_render_indicators(application):
    disp = CalculatorDisplay()
    state = CalculatorState()
    state.has_memory = True
    state.number_format = "Fix 3"
    disp.render(state)
    assert "M" in disp.indicators.text()
    assert "FIX" in disp.indicators.text()
    disp.close()

def test_display_render_error_screen(application):
    disp = CalculatorDisplay()
    state = CalculatorState()
    state.error_state = True
    state.error_message = "Math ERROR"
    state.result = "[AC]:Cancel  [◀][▶]:Goto"
    disp.render(state)
    assert "Math ERROR" in disp.expression.text()
    assert "Goto" in disp.result.text()
    disp.close()
