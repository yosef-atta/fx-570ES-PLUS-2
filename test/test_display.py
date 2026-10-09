from src.core.state import CalculatorState
from src.ui.calculator_display import CalculatorDisplay

def test_display_shows_cursor_and_indicators(application):
    display = CalculatorDisplay()
    display.render(CalculatorState(expression="12", cursor_position=1, shift_active=True))
    assert display.expression.text() == "1│2"
    assert "SHIFT" in display.indicators.text()
    assert "Math" in display.indicators.text()
    assert "DEG" in display.indicators.text()
    display.close()

def test_display_alpha_and_overwrite_indicators(application):
    display = CalculatorDisplay()
    display.render(CalculatorState(alpha_active=True, input_mode="Overwrite", angle_unit="RAD"))
    assert "ALPHA" in display.indicators.text()
    assert "INS" in display.indicators.text()
    assert "RAD" in display.indicators.text()
    display.close()

def test_display_fix_and_sci_indicators(application):
    display = CalculatorDisplay()
    display.render(CalculatorState(number_format="Fix 3", angle_unit="GRA"))
    assert "FIX" in display.indicators.text()
    assert "GRA" in display.indicators.text()

    display.render(CalculatorState(number_format="Sci 2"))
    assert "SCI" in display.indicators.text()
    display.close()

def test_display_result(application):
    display = CalculatorDisplay()
    display.render(CalculatorState(expression="5+5", cursor_position=3, result="10"))
    assert display.expression.text() == "5+5│"
    assert display.result.text() == "10"
    display.close()

def test_display_long_expression_overflow(application):
    display = CalculatorDisplay()
    long_expr = "1234567890" * 8  # 80 characters
    # Cursor at beginning
    display.render(CalculatorState(expression=long_expr, cursor_position=0))
    assert "│" in display.expression.text()
    # Cursor at end
    display.render(CalculatorState(expression=long_expr, cursor_position=len(long_expr)))
    assert "│" in display.expression.text()
    display.close()

def test_display_power_off(application):
    display = CalculatorDisplay()
    display.render(CalculatorState(expression="999", result="999", power_on=False))
    assert display.expression.text() == ""
    assert display.result.text() == ""
    assert display.indicators.text() == ""
    assert display.property("power") == "off"
    display.close()

