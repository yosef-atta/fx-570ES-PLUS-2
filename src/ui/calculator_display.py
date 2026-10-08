"""Read-only LCD display with cursor and mode indicators."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from src.core.state import CalculatorState

class CalculatorDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("lcd")
        layout = QVBoxLayout(self)
        self.indicators = QLabel()
        self.indicators.setObjectName("indicators")
        self.expression = QLabel()
        self.expression.setObjectName("expression")
        self.result = QLabel()
        self.result.setObjectName("result")
        for widget in (self.indicators, self.expression, self.result):
            widget.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            widget.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            layout.addWidget(widget)
        self.setMinimumHeight(128)

    def render(self, state: CalculatorState) -> None:
        if not state.power_on:
            for widget in (self.indicators, self.expression, self.result):
                widget.setText("")
            return
        flags = [state.mode, state.angle_unit]
        if state.shift_active:
            flags.append("SHIFT")
        if state.alpha_active:
            flags.append("ALPHA")
        if state.input_mode == "Overwrite":
            flags.append("INS")
        self.indicators.setText("  ".join(flags))
        pos = state.cursor_position
        # Text-only editing cursor; Phase 2 replaces this with structured rendering.
        text = state.expression[:pos] + "│" + state.expression[pos:]
        self.expression.setText(text[-55:])
        self.result.setText(state.result)
