"""Stress and UX integration tests for Casio fx-570ES PLUS-2 desktop calculator.
Tests layout scaling, rapid sequential inputs, mouse click sequences,
physical keyboard scientific shortcuts, and multi-statement evaluations.
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QKeyEvent
from src.input.keyboard import key_to_id
from src.ui.main_window import MainWindow
from src.core.controller import Controller

def qkey(key, text=""):
    return QKeyEvent(QKeyEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier, text)

def test_window_resize_scaling(application):
    window = MainWindow()
    window.show()
    application.processEvents()

    # Test scaling at various window dimensions
    sizes = [
        QSize(470, 690),   # Min size
        QSize(600, 850),   # Medium
        QSize(800, 1100),  # Large
        QSize(480, 720),   # Restored
    ]

    for size in sizes:
        window.resize(size)
        application.processEvents()
        assert window.isVisible()
        assert window.display.isVisible()
        assert window.keypad.isVisible()
        assert window.width() >= 470
        assert window.height() >= 690

    window.close()
    application.processEvents()


def test_keypad_rapid_mouse_clicks(application):
    window = MainWindow()
    keypad = window.keypad
    controller = window.controller

    # Rapid sequence of 40 clicks: build expression (1+2+3...)+9
    keypad.buttons["1"].click()
    for _ in range(15):
        keypad.buttons["add"].click()
        keypad.buttons["2"].click()
    application.processEvents()

    # Total: 1 + 2 * 15 = 31
    keypad.buttons["equals"].click()
    application.processEvents()

    assert not controller.state.error_state
    assert controller.state.result == "31"

    # Rapid AC
    keypad.buttons["ac"].click()
    application.processEvents()
    assert controller.state.expression == ""
    assert controller.state.result == ""

    window.close()


def test_keyboard_scientific_shortcuts_and_eval(application):
    window = MainWindow()
    c = window.controller

    # Shortcut: s for sin
    window.keyPressEvent(qkey(Qt.Key.Key_S, "s"))
    window.keyPressEvent(qkey(Qt.Key.Key_3, "3"))
    window.keyPressEvent(qkey(Qt.Key.Key_0, "0"))
    window.keyPressEvent(qkey(Qt.Key.Key_ParenRight, ")"))
    window.keyPressEvent(qkey(Qt.Key.Key_Return))
    application.processEvents()

    assert not c.state.error_state
    assert c.state.result in ("1/2", "0.5")

    # Shortcut: Escape to AC
    window.keyPressEvent(qkey(Qt.Key.Key_Escape))
    assert c.state.expression == ""

    # Shortcut: r for sqrt
    window.keyPressEvent(qkey(Qt.Key.Key_R, "r"))
    window.keyPressEvent(qkey(Qt.Key.Key_9, "9"))
    window.keyPressEvent(qkey(Qt.Key.Key_ParenRight, ")"))
    window.keyPressEvent(qkey(Qt.Key.Key_Return))
    application.processEvents()

    assert c.state.result == "3"
    window.close()


def test_multi_statement_colon_evaluation():
    c = Controller()

    # Multi-statement variable chaining: A=5 : B=7 : A+B
    c.press("alpha")
    c.press("negative")  # 'A'
    c.press("alpha")
    c.press("calc")      # '='
    c.press("5")
    c.press("alpha")
    c.press("integral")  # ':'
    c.press("alpha")
    c.press("dms")       # 'B'
    c.press("alpha")
    c.press("calc")      # '='
    c.press("7")
    c.press("alpha")
    c.press("integral")  # ':'
    c.press("alpha")
    c.press("negative")  # 'A'
    c.press("add")
    c.press("alpha")
    c.press("dms")       # 'B'

    assert c.state.expression == "A=5:B=7:A+B"

    # Evaluation evaluates multi-statement pipeline and returns final result
    c.press("equals")
    assert not c.state.error_state
    assert c.state.result == "12"
    assert c.memory.get_var("A") == 5
    assert c.memory.get_var("B") == 7


def test_high_frequency_calculation_stress():
    c = Controller()

    for i in range(1, 51):
        c.press("ac")
        for ch in str(i):
            c.press(ch)
        c.press("multiply")
        c.press("2")
        c.press("add")
        c.press("3")
        c.press("equals")

        expected = str(i * 2 + 3)
        assert c.state.result == expected
        assert not c.state.error_state
