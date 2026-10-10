"""Comprehensive Phase 1 integration tests covering all critical integration scenarios.

Scenarios defined in PHASE-1.md Section 4:
1. Enter 123 using the mouse; display shows 123.
2. Enter 123 using the keyboard; state matches mouse input.
3. Move cursor left and insert another digit at the correct position.
4. Delete a digit using DEL and Backspace.
5. Press AC and verify the expression is cleared.
6. Press SHIFT and verify the indicator becomes active.
7. Press a shifted-function key and verify the correct alternate action is dispatched.
8. Press ALPHA and verify its alternate mapping.
9. Press MODE and select COMP.
10. Press MODE and select CMPLX; verify only the mode changes, not mathematical capability.
11. Press SHIFT + MODE and verify SETUP opens.
12. Change the angle setting and verify its indicator.
13. Navigate a multi-page menu with arrow keys.
14. Select a menu option using a numeric key.
15. Press AC while in a menu and verify cancellation.
16. Verify SHIFT + AC powers off the calculator.
17. Verify ON restores interactive operation.
18. Verify unimplemented calculation actions cannot produce misleading results.
19. Verify no action unexpectedly crashes the application.
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from src.core.key_registry import REGISTRY
from src.ui.main_window import MainWindow

def key_event(key, text=""):
    return QKeyEvent(QKeyEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier, text)

def test_scenario_01_enter_123_mouse(application):
    window = MainWindow()
    window.keypad.buttons["1"].click()
    window.keypad.buttons["2"].click()
    window.keypad.buttons["3"].click()
    assert window.controller.state.expression == "123"
    assert "123│" in window.display.expression.text()
    window.close()

def test_scenario_02_enter_123_keyboard_matches_mouse(application):
    win_mouse = MainWindow()
    win_mouse.keypad.buttons["1"].click()
    win_mouse.keypad.buttons["2"].click()
    win_mouse.keypad.buttons["3"].click()

    win_kb = MainWindow()
    win_kb.keyPressEvent(key_event(Qt.Key.Key_1, "1"))
    win_kb.keyPressEvent(key_event(Qt.Key.Key_2, "2"))
    win_kb.keyPressEvent(key_event(Qt.Key.Key_3, "3"))

    assert win_kb.controller.state.expression == win_mouse.controller.state.expression
    assert win_kb.controller.state.cursor_position == win_mouse.controller.state.cursor_position
    win_mouse.close()
    win_kb.close()

def test_scenario_03_move_cursor_and_insert(application):
    window = MainWindow()
    window.keypad.buttons["1"].click()
    window.keypad.buttons["2"].click()
    window.keypad.buttons["3"].click()
    # Move left once (between 2 and 3)
    window.keypad.buttons["left"].click()
    assert window.controller.state.cursor_position == 2
    # Insert 9
    window.keypad.buttons["9"].click()
    assert window.controller.state.expression == "1293"
    assert window.controller.state.cursor_position == 3
    window.close()

def test_scenario_04_delete_using_del_and_backspace(application):
    window = MainWindow()
    window.keyPressEvent(key_event(Qt.Key.Key_1, "1"))
    window.keyPressEvent(key_event(Qt.Key.Key_2, "2"))
    window.keyPressEvent(key_event(Qt.Key.Key_3, "3"))
    # Delete via DEL button
    window.keypad.buttons["del"].click()
    assert window.controller.state.expression == "12"
    # Delete via Backspace key
    window.keyPressEvent(key_event(Qt.Key.Key_Backspace))
    assert window.controller.state.expression == "1"
    window.close()

def test_scenario_05_press_ac_clears_expression(application):
    window = MainWindow()
    window.keypad.buttons["7"].click()
    window.keypad.buttons["8"].click()
    window.keypad.buttons["9"].click()
    assert window.controller.state.expression == "789"
    window.keypad.buttons["ac"].click()
    assert window.controller.state.expression == ""
    assert window.controller.state.cursor_position == 0
    assert window.controller.state.result == ""
    window.close()

def test_scenario_06_shift_indicator_active(application):
    window = MainWindow()
    window.keypad.buttons["shift"].click()
    assert window.controller.state.shift_active
    assert "SHIFT" in window.display.indicators.text()
    window.close()

def test_scenario_07_shifted_function_dispatched(application):
    window = MainWindow()
    window.keypad.buttons["shift"].click()
    # Press DEL (shifted function is INS/insert_toggle)
    window.keypad.buttons["del"].click()
    assert window.controller.state.input_mode == "Overwrite"
    assert not window.controller.state.shift_active
    assert "INS" in window.display.indicators.text()
    window.close()

def test_scenario_08_alpha_alternate_mapping(application):
    window = MainWindow()
    window.keypad.buttons["alpha"].click()
    assert window.controller.state.alpha_active
    assert "ALPHA" in window.display.indicators.text()
    # Press rparen (shifted is ',', alpha is 'X')
    window.keypad.buttons["rparen"].click()
    assert window.controller.state.expression == "X"
    assert not window.controller.state.alpha_active
    window.close()

def test_scenario_09_mode_comp(application):
    window = MainWindow()
    window.keypad.buttons["mode"].click()
    assert window.controller.state.active_menu == "MODE"
    window.keypad.buttons["1"].click()
    assert window.controller.state.mode == "COMP"
    assert window.controller.state.active_menu is None
    window.close()

def test_scenario_10_mode_cmplx_no_fake_calc(application):
    window = MainWindow()
    window.keypad.buttons["mode"].click()
    window.keypad.buttons["2"].click()
    assert window.controller.state.mode == "CMPLX"
    assert window.controller.state.active_menu is None
    # Verify no fake mathematical result is produced
    assert window.controller.state.result == ""
    window.close()

def test_scenario_11_shift_mode_opens_setup(application):
    window = MainWindow()
    window.keypad.buttons["shift"].click()
    window.keypad.buttons["mode"].click()
    assert window.controller.state.active_menu == "SETUP"
    assert not window.menu.isHidden()
    assert "SETUP" in window.menu.heading.text()
    window.close()

def test_scenario_12_change_angle_and_verify_indicator(application):
    window = MainWindow()
    # Open SETUP
    window.keypad.buttons["shift"].click()
    window.keypad.buttons["mode"].click()
    # Option 4 is RAD
    window.keypad.buttons["4"].click()
    assert window.controller.state.angle_unit == "RAD"
    assert "RAD" in window.display.indicators.text()
    # Open SETUP again and select GRA (option 5)
    window.keypad.buttons["shift"].click()
    window.keypad.buttons["mode"].click()
    window.keypad.buttons["5"].click()
    assert window.controller.state.angle_unit == "GRA"
    assert "GRA" in window.display.indicators.text()
    window.close()

def test_scenario_13_navigate_multipage_menu(application):
    window = MainWindow()
    window.keypad.buttons["mode"].click()
    assert window.controller.state.menu_page == 0
    # Down arrow past page boundary
    for _ in range(6):
        window.keypad.buttons["down"].click()
    assert window.controller.state.menu_page == 1
    assert "TABLE" in window.menu.options.text()
    # Up arrow back
    for _ in range(6):
        window.keypad.buttons["up"].click()
    assert window.controller.state.menu_page == 0
    assert "COMP" in window.menu.options.text()
    window.close()

def test_scenario_14_select_menu_numeric(application):
    window = MainWindow()
    window.keypad.buttons["mode"].click()
    # 3 is STAT
    window.keypad.buttons["3"].click()
    assert window.controller.state.mode == "STAT"
    assert window.controller.state.active_menu is None
    window.close()

def test_scenario_15_press_ac_cancels_menu(application):
    window = MainWindow()
    window.keypad.buttons["mode"].click()
    assert window.controller.state.active_menu == "MODE"
    window.keypad.buttons["ac"].click()
    assert window.controller.state.active_menu is None
    assert window.menu.isHidden()
    window.close()

def test_scenario_16_shift_ac_powers_off(application):
    window = MainWindow()
    window.keypad.buttons["shift"].click()
    window.keypad.buttons["ac"].click()
    assert not window.controller.state.power_on
    assert window.display.expression.text() == ""
    assert window.display.result.text() == ""
    assert window.display.indicators.text() == ""
    assert window.display.property("power") == "off"
    # Normal input is ignored while off
    window.keypad.buttons["1"].click()
    window.keyPressEvent(key_event(Qt.Key.Key_2, "2"))
    assert window.controller.state.expression == ""
    window.close()

def test_scenario_17_on_restores_interactive(application):
    window = MainWindow()
    # Power off
    window.keypad.buttons["shift"].click()
    window.keypad.buttons["ac"].click()
    assert not window.controller.state.power_on
    # Press ON
    window.keypad.buttons["on"].click()
    assert window.controller.state.power_on
    assert window.display.property("power") == "on"
    # Normal interaction works again
    window.keypad.buttons["5"].click()
    assert window.controller.state.expression == "5"
    window.close()

def test_scenario_18_unimplemented_actions_no_misleading_results(application):
    window = MainWindow()
    window.keypad.buttons["shift"].click()
    window.keypad.buttons["7"].click()
    assert "Not implemented" in window.controller.state.result
    assert window.controller.state.deferred_actions == ["const"]
    window.close()

def test_scenario_19_no_action_crashes_application(application):
    window = MainWindow()
    for key_id in REGISTRY:
        window.keypad.buttons[key_id].click()
        window.controller.state.validate()
        application.processEvents()
    window.close()
