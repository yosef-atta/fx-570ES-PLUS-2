from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from src.input.keyboard import key_to_id
from src.ui.main_window import MainWindow

def event(key, text=""):
    return QKeyEvent(QKeyEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier, text)

def test_mappings():
    assert key_to_id(event(Qt.Key.Key_7, "7")) == "7"
    assert key_to_id(event(Qt.Key.Key_Enter)) == "equals"
    assert key_to_id(event(Qt.Key.Key_Return)) == "equals"
    assert key_to_id(event(Qt.Key.Key_Equal, "=")) == "equals"
    assert key_to_id(event(Qt.Key.Key_Left)) == "left"
    assert key_to_id(event(Qt.Key.Key_Right)) == "right"
    assert key_to_id(event(Qt.Key.Key_Up)) == "up"
    assert key_to_id(event(Qt.Key.Key_Down)) == "down"
    assert key_to_id(event(Qt.Key.Key_Escape)) == "ac"
    assert key_to_id(event(Qt.Key.Key_F2)) == "shift"
    assert key_to_id(event(Qt.Key.Key_F3)) == "alpha"
    assert key_to_id(event(Qt.Key.Key_F4)) == "mode"
    assert key_to_id(event(Qt.Key.Key_F5)) == "setup_shortcut"
    assert key_to_id(event(Qt.Key.Key_Plus, "+")) == "add"
    assert key_to_id(event(Qt.Key.Key_Minus, "-")) == "subtract"
    assert key_to_id(event(Qt.Key.Key_Asterisk, "*")) == "multiply"
    assert key_to_id(event(Qt.Key.Key_Slash, "/")) == "divide"
    assert key_to_id(event(Qt.Key.Key_Period, ".")) == "dot"
    assert key_to_id(event(Qt.Key.Key_A, "a")) is None

def test_keyboard_to_controller(application):
    window = MainWindow()
    window.keyPressEvent(event(Qt.Key.Key_1, "1"))
    window.keyPressEvent(event(Qt.Key.Key_2, "2"))
    window.keyPressEvent(event(Qt.Key.Key_Backspace))
    assert window.controller.state.expression == "1"
    window.close()

def test_keyboard_expression_and_clear(application):
    window = MainWindow()
    # Type 1 + 2 * 3
    window.keyPressEvent(event(Qt.Key.Key_1, "1"))
    window.keyPressEvent(event(Qt.Key.Key_Plus, "+"))
    window.keyPressEvent(event(Qt.Key.Key_2, "2"))
    window.keyPressEvent(event(Qt.Key.Key_Asterisk, "*"))
    window.keyPressEvent(event(Qt.Key.Key_3, "3"))
    assert window.controller.state.expression == "1+2×3"
    # Escape clears all
    window.keyPressEvent(event(Qt.Key.Key_Escape))
    assert window.controller.state.expression == ""
    assert window.controller.state.cursor_position == 0
    window.close()

def test_keyboard_shortcuts(application):
    window = MainWindow()
    # F2 activates SHIFT
    window.keyPressEvent(event(Qt.Key.Key_F2))
    assert window.controller.state.shift_active
    # F3 switches to ALPHA
    window.keyPressEvent(event(Qt.Key.Key_F3))
    assert window.controller.state.alpha_active
    assert not window.controller.state.shift_active
    # Escape resets menu or modifiers
    window.keyPressEvent(event(Qt.Key.Key_Escape))
    # F4 opens MODE menu
    window.keyPressEvent(event(Qt.Key.Key_F4))
    assert window.controller.state.active_menu == "MODE"
    window.keyPressEvent(event(Qt.Key.Key_Escape))
    assert window.controller.state.active_menu is None
    # F5 opens SETUP menu
    window.keyPressEvent(event(Qt.Key.Key_F5))
    assert window.controller.state.active_menu == "SETUP"
    window.keyPressEvent(event(Qt.Key.Key_Escape))
    assert window.controller.state.active_menu is None
    window.close()

