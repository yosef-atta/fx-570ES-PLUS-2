"""Top-level native calculator window for Casio fx-570ES PLUS 2nd Edition."""
import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
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
from src.core.preferences import PreferencesManager
from src.input.keyboard import key_to_id
from .calculator_display import CalculatorDisplay
from .keypad import Keypad
from .menu_view import MenuView
from .table_view import TableView
from .style import STYLESHEET


class MainWindow(QMainWindow):
    def __init__(
        self,
        controller: Controller | None = None,
        preferences: PreferencesManager | None = None,
    ):
        super().__init__()
        self.preferences = (
            preferences if preferences is not None else PreferencesManager()
        )
        self.controller = controller if controller is not None else Controller()

        # Load persisted preferences into controller state
        self.preferences.load_into_state(self.controller.state)

        self.setWindowTitle("Scientific Calculator")
        self.setMinimumSize(470, 690)

        # Restore saved window geometry if available, otherwise default
        saved_geom = self.preferences.get_window_geometry()
        if saved_geom:
            self.resize(saved_geom["width"], saved_geom["height"])
            if saved_geom["x"] is not None and saved_geom["y"] is not None:
                self.move(saved_geom["x"], saved_geom["y"])
        else:
            self.resize(500, 780)

        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

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
        # Persist updated configuration
        self.preferences.save_state(state)

    def keyPressEvent(self, event):
        key = key_to_id(event)
        if key == "setup_shortcut":
            self.controller.dispatch(Action.command("setup"))
        elif key:
            self.controller.press(key)
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """Save window position, dimensions, and state on exit."""
        self.preferences.save_window_geometry(
            self.width(), self.height(), self.x(), self.y()
        )
        self.preferences.save_state(self.controller.state)
        super().closeEvent(event)
