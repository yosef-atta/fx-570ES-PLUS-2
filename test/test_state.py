import pytest
from src.core.state import CalculatorState

def test_defaults():
    s = CalculatorState()
    s.validate()
    assert (s.mode, s.angle_unit, s.expression) == ("COMP", "DEG", "")
    assert s.power_on is True
    assert s.cursor_position == 0
    assert s.input_mode == "Insert"

def test_invalid_cursor():
    s = CalculatorState(expression="123", cursor_position=4)
    with pytest.raises(ValueError):
        s.validate()
    s2 = CalculatorState(expression="123", cursor_position=-1)
    with pytest.raises(ValueError):
        s2.validate()

def test_exclusive_modifiers():
    s = CalculatorState(shift_active=True, alpha_active=True)
    with pytest.raises(ValueError):
        s.validate()

def test_invalid_mode_or_angle():
    with pytest.raises(ValueError):
        CalculatorState(mode="INVALID").validate()
    with pytest.raises(ValueError):
        CalculatorState(angle_unit="TURN").validate()

def test_reset():
    s = CalculatorState(
        expression="123+4",
        cursor_position=3,
        result="5",
        shift_active=True,
        active_menu="MODE",
        menu_page=1,
        menu_selection=2,
    )
    s.reset()
    assert s.expression == ""
    assert s.cursor_position == 0
    assert s.result == ""
    assert s.shift_active is False
    assert s.alpha_active is False
    assert s.active_menu is None
    assert s.menu_page == 0
    assert s.menu_selection == 0
    # Mode and settings persist across reset
    assert s.mode == "COMP"

