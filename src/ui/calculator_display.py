"""Read-only LCD display with natural textbook rendering, cursor, and mode indicators."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from src.core.state import CalculatorState
from .natural_canvas import render_natural_math, render_natural_result

class CalculatorDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("lcd")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(2)
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
        self.result.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.result)

        self.setMinimumHeight(115)

    def render(self, state: CalculatorState) -> None:
        if not state.power_on:
            self.setProperty("power", "off")
            for widget in (self.indicators, self.expression, self.result):
                widget.setText("")
            self.style().unpolish(self)
            self.style().polish(self)
            return

        self.setProperty("power", "on")
        
        # Calculate horizontal scrolling window for expression (expanded to 26 for wider Casio LCD)
        MAX_VISIBLE = 26
        expr = state.expression
        pos = state.cursor_position
        total_len = len(expr)
        
        if total_len <= MAX_VISIBLE:
            visible_expr = expr
            cursor_idx = pos
            has_left = False
            has_right = False
        else:
            half = MAX_VISIBLE // 2
            start = pos - half
            start = max(0, min(total_len - MAX_VISIBLE, start))
            end = start + MAX_VISIBLE
            visible_expr = expr[start:end]
            cursor_idx = pos - start
            has_left = (start > 0)
            has_right = (end < total_len)

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
        if has_left:
            flags.append("◀")
        if has_right:
            flags.append("▶")
        if getattr(state, "history_has_prev", False):
            flags.append("▲")
        if getattr(state, "history_has_next", False):
            flags.append("▼")
        # Capacity indicator matching physical Casio notification
        if total_len >= 99:
            flags.append("FULL")
        elif total_len >= 89:
            flags.append(f"[{total_len}/99]")
        self.indicators.setText("   ".join(flags))

        # Error State rendering
        if state.error_state:
            self.expression.setText(f"<b>{state.error_message}</b>")
            self.result.setText(state.result)
            self.style().unpolish(self)
            self.style().polish(self)
            return

        # Normal mathematical display rendering
        # Casio hardware switches cursor from '│' to solid block '■' when capacity remaining <= 10
        cursor_char = "■" if total_len >= 89 else "│"
        is_natural = state.display_format.startswith("MthIO")
        rendered_expr = render_natural_math(visible_expr, cursor_idx, is_natural=is_natural, cursor_char=cursor_char)
        self.expression.setText(rendered_expr)
        
        rendered_result = render_natural_result(state.result, is_natural=is_natural)
        self.result.setText(rendered_result)
        self.style().unpolish(self)
        self.style().polish(self)
