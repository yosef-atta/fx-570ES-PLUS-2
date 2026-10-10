from src.core.action import Action
from src.core.controller import Controller
from src.core.key_registry import REGISTRY

def test_insert_move_delete_and_clear():
    c = Controller()
    for key in ("1", "2", "3", "left", "9"):
        c.press(key)
    assert c.state.expression == "1293"
    c.press("del")
    assert c.state.expression == "123"
    c.press("ac")
    assert c.state.expression == "" and c.state.cursor_position == 0

def test_shift_setup_angle():
    c = Controller()
    c.press("shift")
    c.press("mode")
    assert c.state.active_menu == "SETUP"
    c.press("4")
    assert c.state.angle_unit == "RAD" and c.state.active_menu is None

def test_mode_selection():
    c = Controller()
    c.press("mode")
    c.press("2")
    assert c.state.mode == "CMPLX"

def test_off_and_on():
    c = Controller()
    c.press("shift")
    c.press("ac")
    assert not c.state.power_on
    c.press("1")
    assert c.state.expression == ""
    # Direct dispatch while off is ignored
    c.dispatch(Action.insert("9"))
    assert c.state.expression == ""
    c.press("on")
    assert c.state.power_on

def test_deferred_is_never_a_fake_result():
    c = Controller()
    c.press("shift")
    c.press("7")  # CONST deferred to Phase 3
    assert c.state.deferred_actions == ["const"]
    assert "Not implemented" in c.state.result

def test_modifiers_are_exclusive_and_one_shot():
    c = Controller()
    c.press("shift")
    c.press("alpha")
    assert c.state.alpha_active and not c.state.shift_active
    c.press("7")
    assert not c.state.alpha_active

def test_modifier_toggle_off():
    c = Controller()
    c.press("shift")
    assert c.state.shift_active
    c.press("shift")
    assert not c.state.shift_active
    c.press("alpha")
    assert c.state.alpha_active
    c.press("alpha")
    assert not c.state.alpha_active

def test_alpha_variable_input():
    c = Controller()
    c.press("alpha")
    c.press("rparen")  # ALPHA + ) -> X
    assert c.state.expression == "X"
    c.press("alpha")
    c.press("negative")  # ALPHA + (-) -> A
    assert c.state.expression == "XA"

def test_shift_symbol_input():
    c = Controller()
    c.press("shift")
    c.press("exp10")  # SHIFT + ×10ˣ -> π
    assert c.state.expression == "π"

def test_menu_cancel():
    c = Controller()
    c.press("mode")
    assert c.state.active_menu == "MODE"
    c.press("ac")
    assert c.state.active_menu is None
    # Cancel via ON key
    c.press("mode")
    assert c.state.active_menu == "MODE"
    c.press("on")
    assert c.state.active_menu is None

def test_menu_arrow_and_equals_selection():
    c = Controller()
    c.press("mode")
    assert c.state.active_menu == "MODE"
    c.press("right")  # Moves to selection 1 (CMPLX)
    c.press("equals")
    assert c.state.mode == "CMPLX"
    assert c.state.active_menu is None

def test_menu_invalid_key_handling():
    c = Controller()
    c.press("mode")
    assert c.state.active_menu == "MODE"
    c.press("sin")  # invalid menu key
    assert c.state.active_menu == "MODE"
    c.press("0")  # 0 is not a valid menu choice (1-6 are)
    assert c.state.active_menu == "MODE"
    c.press("ac")
    assert c.state.active_menu is None

def test_overwrite_mode():
    c = Controller()
    c.press("1")
    c.press("2")
    c.press("3")
    c.press("left")
    c.press("left")  # cursor at position 1 (between 1 and 2)
    # Enable Overwrite mode via SHIFT + DEL
    c.press("shift")
    c.press("del")
    assert c.state.input_mode == "Overwrite"
    c.press("9")
    assert c.state.expression == "193"
    assert c.state.cursor_position == 2
    # Toggle back to Insert mode
    c.press("shift")
    c.press("del")
    assert c.state.input_mode == "Insert"

def test_cursor_boundary_limits():
    c = Controller()
    c.press("1")
    # Move left past 0
    c.press("left")
    c.press("left")
    assert c.state.cursor_position == 0
    # Delete at position 0
    c.press("del")
    assert c.state.expression == "1"
    assert c.state.cursor_position == 0
    # Move right past end
    c.press("right")
    c.press("right")
    assert c.state.cursor_position == 1

def test_all_registry_keys_can_be_pressed():
    for key_id in REGISTRY:
        c = Controller()
        c.press(key_id)
        # Verify state is valid
        c.state.validate()

