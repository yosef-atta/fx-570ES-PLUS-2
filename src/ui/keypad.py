"""Visual key layout generated from registry definitions."""
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout
from src.core.key_registry import KEYS
from .calculator_key import CalculatorKey

class Keypad(QWidget):
    triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.buttons = {}
        for specification in KEYS:
            button = CalculatorKey(specification, self)
            button.triggered.connect(self.triggered.emit)
            self.buttons[specification.id] = button
            layout.addWidget(button, specification.row, specification.column)
