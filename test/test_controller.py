from src.core.controller import Controller

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
    c.press("on")
    assert c.state.power_on

def test_deferred_is_never_a_fake_result():
    c = Controller()
    c.press("sin")
    assert c.state.deferred_actions == ["sin"]
    assert "Not implemented" in c.state.result

def test_modifiers_are_exclusive_and_one_shot():
    c = Controller()
    c.press("shift")
    c.press("alpha")
    assert c.state.alpha_active and not c.state.shift_active
    c.press("7")
    assert not c.state.alpha_active

def test_menu_cancel():
    c = Controller()
    c.press("mode")
    c.press("ac")
    assert c.state.active_menu is None
