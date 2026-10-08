from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from src.input.keyboard import key_to_id
from src.ui.main_window import MainWindow

def event(key, text=""):
    return QKeyEvent(QKeyEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier, text)

def test_mappings():
    assert key_to_id(event(Qt.Key.Key_7, "7")) == "7"
    assert key_to_id(event(Qt.Key.Key_Enter)) == "equals"
    assert key_to_id(event(Qt.Key.Key_Left)) == "left"
    assert key_to_id(event(Qt.Key.Key_A, "a")) is None

def test_keyboard_to_controller(application):
    window = MainWindow()
    window.keyPressEvent(event(Qt.Key.Key_1, "1"))
    window.keyPressEvent(event(Qt.Key.Key_2, "2"))
    window.keyPressEvent(event(Qt.Key.Key_Backspace))
    assert window.controller.state.expression == "1"
    window.close()
