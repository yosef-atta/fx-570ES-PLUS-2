"""Top-level native calculator window for Casio fx-570ES PLUS 2nd Edition."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)
from src.core.controller import Controller
from src.core.action import Action
from src.input.keyboard import key_to_id
from .calculator_display import CalculatorDisplay
from .keypad import Keypad
from .menu_view import MenuView
from .table_view import TableView
from .style import STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self, controller: Controller | None = None):
        super().__init__()
        self.controller = controller if controller is not None else Controller()
        self.setWindowTitle("Scientific Calculator")
        self.setMinimumSize(470, 690)
        self.resize(500, 780)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet(STYLESHEET)

        # Outer calculator casing
        shell = QWidget()
        shell.setObjectName("shell")
        layout = QVBoxLayout(shell)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        # -------------------------------------------------------------
        # Header: Authentic Casio Branding
        # -------------------------------------------------------------
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(4, 2, 4, 2)
        header_layout.setSpacing(1)

        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        casio_lbl = QLabel("CASIO")
        casio_lbl.setObjectName("brand_casio")
        model_lbl = QLabel("fx-570ES PLUS")
        model_lbl.setObjectName("brand_model")
        row1.addWidget(casio_lbl)
        row1.addStretch()
        row1.addWidget(model_lbl)
        header_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        vpam_lbl = QLabel("NATURAL-V.P.A.M.")
        vpam_lbl.setObjectName("brand_vpam")
        edition_lbl = QLabel("2nd edition")
        edition_lbl.setObjectName("brand_edition")
        row2.addWidget(vpam_lbl)
        row2.addStretch()
        row2.addWidget(edition_lbl)
        header_layout.addLayout(row2)

        layout.addLayout(header_layout)

        # -------------------------------------------------------------
        # Recessed Screen Housing
        # -------------------------------------------------------------
        lcd_frame = QFrame()
        lcd_frame.setObjectName("lcd_frame")
        lcd_layout = QVBoxLayout(lcd_frame)
        lcd_layout.setContentsMargins(5, 5, 5, 5)
        lcd_layout.setSpacing(2)

        self.display = CalculatorDisplay()
        self.table_view = TableView()
        self.menu = MenuView()

        lcd_layout.addWidget(self.display)
        lcd_layout.addWidget(self.table_view)
        lcd_layout.addWidget(self.menu)

        layout.addWidget(lcd_frame)

        # -------------------------------------------------------------
        # Physical Keypad
        # -------------------------------------------------------------
        self.keypad = Keypad()
        layout.addWidget(self.keypad)

        self.setCentralWidget(shell)

        # Event connections
        self.keypad.triggered.connect(self.controller.press)
        self.controller.subscribe(self.refresh)

    def refresh(self, state):
        self.display.render(state)
        self.table_view.update_grid(state)
        self.menu.render(state)

    def keyPressEvent(self, event):
        key = key_to_id(event)
        if key == "setup_shortcut":
            self.controller.dispatch(Action.command("setup"))
        elif key:
            self.controller.press(key)
        else:
            super().keyPressEvent(event)
