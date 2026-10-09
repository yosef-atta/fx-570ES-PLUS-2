"""Mode/setup overlay embedded above the keypad."""
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from src.core.controller import SETUP, PAGE_SIZE
from src.core.state import MODES, CalculatorState

class MenuView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("lcd")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        self.heading = QLabel()
        self.heading.setObjectName("menu_heading")
        self.options = QLabel()
        self.options.setObjectName("menu_options")
        self.options.setWordWrap(True)
        layout.addWidget(self.heading)
        layout.addWidget(self.options)
        self.hide()

    def render(self, state: CalculatorState) -> None:
        if not state.active_menu or not state.power_on:
            self.hide()
            return
        values = MODES if state.active_menu == "MODE" else SETUP
        page = state.menu_page
        start = page * PAGE_SIZE
        visible = values[start:start + PAGE_SIZE]
        total_pages = (len(values) + PAGE_SIZE - 1) // PAGE_SIZE
        arrows = ""
        if page > 0:
            arrows += "▲"
        if start + PAGE_SIZE < len(values):
            arrows += (" " if arrows else "") + "▼"
        self.heading.setText(f"{state.active_menu}  [{page + 1}/{total_pages}]  {arrows}".strip())
        
        lines = []
        for row_start in range(0, len(visible), 2):
            row_items = []
            for col in range(2):
                idx = row_start + col
                if idx < len(visible):
                    global_idx = start + idx
                    prefix = "▶ " if global_idx == state.menu_selection else "  "
                    row_items.append(f"{prefix}{idx + 1}: {visible[idx]:<12}")
            lines.append("     ".join(row_items))
        self.options.setText("\n".join(lines))
        self.show()
