"""Mode/setup overlay embedded above the keypad."""
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from src.core.controller import SETUP, PAGE_SIZE
from src.core.state import MODES, CalculatorState

class MenuView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("lcd")
        layout = QVBoxLayout(self)
        self.heading = QLabel()
        self.options = QLabel()
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
        self.heading.setText(f"{state.active_menu}  ·  {page + 1}/{(len(values) + PAGE_SIZE - 1) // PAGE_SIZE}")
        self.options.setText("     ".join(f"{i + 1}: {value}" for i, value in enumerate(visible)))
        self.show()
