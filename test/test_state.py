import pytest
from src.core.state import CalculatorState

def test_defaults():
    s = CalculatorState()
    s.validate()
    assert (s.mode, s.angle_unit, s.expression) == ("COMP", "DEG", "")

def test_invalid_cursor():
    s = CalculatorState(cursor_position=1)
    with pytest.raises(ValueError):
        s.validate()

def test_exclusive_modifiers():
    s = CalculatorState(shift_active=True, alpha_active=True)
    with pytest.raises(ValueError):
        s.validate()
