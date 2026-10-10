"""Read-only LCD display with natural textbook rendering, cursor, and mode indicators."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from src.core.state import CalculatorState
from .natural_canvas import render_natural_math

class CalculatorDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("lcd")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        self.indicators = QLabel()
        self.indicators.setObjectName("indicators")
        self.expression = QLabel()
        self.expression.setObjectName("expression")
        self.result = QLabel()
        self.result.setObjectName("result")
        
        self.indicators.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.indicators.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        layout.addWidget(self.indicators)

        self.expression.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.expression.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.expression.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.expression)

        self.result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.result.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        layout.addWidget(self.result)

        self.setMinimumHeight(128)

    def render(self, state: CalculatorState) -> None:
        if not state.power_on:
            self.setProperty("power", "off")
            for widget in (self.indicators, self.expression, self.result):
                widget.setText("")
            self.style().unpolish(self)
            self.style().polish(self)
            return

        self.setProperty("power", "on")
        flags = [state.mode, state.angle_unit]
        if state.display_format.startswith("MthIO"):
            flags.append("Math")
        if state.has_memory:
            flags.append("M")
        if state.number_format.startswith("Fix"):
            flags.append("FIX")
        elif state.number_format.startswith("Sci"):
            flags.append("SCI")
        if state.shift_active:
            flags.append("SHIFT")
        if state.alpha_active:
            flags.append("ALPHA")
        if state.input_mode == "Overwrite":
            flags.append("INS")
        self.indicators.setText("   ".join(flags))

        # Error State rendering
        if state.error_state:
            self.expression.setText(f"<b>{state.error_message}</b>")
            self.result.setText(state.result)
            self.style().unpolish(self)
            self.style().polish(self)
            return

        # Normal mathematical display rendering
        is_natural = state.display_format.startswith("MthIO")
        rendered_expr = render_natural_math(state.expression, state.cursor_position, is_natural=is_natural)
        self.expression.setText(rendered_expr)
        self.result.setText(state.result)
        self.style().unpolish(self)
        self.style().polish(self)
