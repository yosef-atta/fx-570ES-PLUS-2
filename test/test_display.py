from src.core.state import CalculatorState
from src.ui.calculator_display import CalculatorDisplay

def test_display_shows_cursor_and_indicators(application):
    display = CalculatorDisplay()
    display.render(CalculatorState(expression="12", cursor_position=1, shift_active=True))
    assert display.expression.text() == "1│2"
    assert "SHIFT" in display.indicators.text()
    display.close()
