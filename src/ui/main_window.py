"""Top-level native calculator window."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QLabel
from src.core.controller import Controller
from src.core.action import Action
from src.input.keyboard import key_to_id
from .calculator_display import CalculatorDisplay
from .keypad import Keypad
from .menu_view import MenuView
from .style import STYLESHEET

class MainWindow(QMainWindow):
    def __init__(self, controller: Controller | None = None):
        super().__init__()
        self.controller = controller if controller is not None else Controller()
        self.setWindowTitle("Scientific Calculator")
        self.setMinimumSize(470, 690)
        self.resize(560, 760)
        self.setStyleSheet(STYLESHEET)
        shell = QWidget()
        shell.setObjectName("shell")
        layout = QVBoxLayout(shell)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        brand = QLabel("SCIENTIFIC   /   570")
        brand.setObjectName("brand")
        subtitle = QLabel("OFFLINE  •  WINDOWS  •  SCIENTIFIC")
        subtitle.setObjectName("subtitle")
        self.display = CalculatorDisplay()
        self.menu = MenuView()
        self.keypad = Keypad()
        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addWidget(self.display)
        layout.addWidget(self.menu)
        layout.addWidget(self.keypad)
        self.setCentralWidget(shell)
        self.keypad.triggered.connect(self.controller.press)
        self.controller.subscribe(self.refresh)

    def refresh(self, state):
        self.display.render(state)
        self.menu.render(state)

    def keyPressEvent(self, event):
        key = key_to_id(event)
        if key == "setup_shortcut":
            self.controller.dispatch(Action.command("setup"))
        elif key:
            self.controller.press(key)
        else:
            super().keyPressEvent(event)
