"""One button per physical key, with no calculator state logic."""
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton
from src.core.key_registry import Key

class CalculatorKey(QPushButton):
    triggered = Signal(str)

    def __init__(self, specification: Key, parent=None):
        super().__init__(parent)
        self.specification = specification
        self.setObjectName("key_" + specification.id)
        self.setProperty("category", specification.category)
        self.setMinimumWidth(58)
        self.setToolTip(" | ".join(x for x in (specification.label,
                        "SHIFT: " + specification.shift_label if specification.shift else "",
                        "ALPHA: " + specification.alpha_label if specification.alpha else "") if x))
        self.setText(specification.label)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clicked.connect(lambda: self.triggered.emit(specification.id))
