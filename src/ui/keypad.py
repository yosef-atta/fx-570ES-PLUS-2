"""Visual key layout matching physical Casio fx-570ES PLUS 2nd Edition."""
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QSizePolicy,
)
from src.core.key_registry import KEYS
from .calculator_key import CalculatorKey


class ReplayPad(QFrame):
    """Circular Replay D-Pad with 4 directional buttons and center label."""

    def __init__(self, up_btn, down_btn, left_btn, right_btn, parent=None):
        super().__init__(parent)
        self.setObjectName("replay_pad")
        self.setFixedSize(108, 78)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        grid = QGridLayout(self)
        grid.setContentsMargins(4, 3, 4, 3)
        grid.setSpacing(2)

        center_lbl = QLabel("REPLAY")
        center_lbl.setObjectName("replay_center_label")
        center_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        grid.addWidget(up_btn, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(left_btn, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(center_lbl, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(right_btn, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(down_btn, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)


class Keypad(QWidget):
    triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("keypad_container")

        # 1. Instantiate every registered key to maintain 100% test compatibility
        self.buttons = {}
        for spec in KEYS:
            btn = CalculatorKey(spec, self)
            btn.triggered.connect(self.triggered.emit)
            self.buttons[spec.id] = btn

        # 2. Authentic styling adjustments for specific keys
        fact_btn = self.buttons.get("factorial")
        if fact_btn:
            fact_btn.main_lbl.setText("log■□")
            fact_btn.shift_lbl.setText("Σ")
            fact_btn.setToolTip("log■□ | SHIFT: Σ")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(4, 4, 4, 4)
        root_layout.setSpacing(6)

        # -------------------------------------------------------------
        # Tier 1: Top Control & Navigation (Left 2x2, Replay D-Pad, Right 2x2)
        # -------------------------------------------------------------
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(8)

        # Left 2x2: SHIFT, ALPHA / CALC, ∫
        left_grid = QGridLayout()
        left_grid.setContentsMargins(0, 0, 0, 0)
        left_grid.setSpacing(4)
        left_grid.addWidget(self.buttons["shift"], 0, 0)
        left_grid.addWidget(self.buttons["alpha"], 0, 1)
        left_grid.addWidget(self.buttons["calc"], 1, 0)
        left_grid.addWidget(self.buttons["integral"], 1, 1)
        top_row.addLayout(left_grid, stretch=1)

        # Center: Circular Replay Pad
        replay = ReplayPad(
            self.buttons["up"],
            self.buttons["down"],
            self.buttons["left"],
            self.buttons["right"],
            self,
        )
        top_row.addWidget(replay, alignment=Qt.AlignmentFlag.AlignCenter)

        # Right 2x2: MODE, ON / x⁻¹, log■□
        right_grid = QGridLayout()
        right_grid.setContentsMargins(0, 0, 0, 0)
        right_grid.setSpacing(4)
        right_grid.addWidget(self.buttons["mode"], 0, 0)
        right_grid.addWidget(self.buttons["on"], 0, 1)
        right_grid.addWidget(self.buttons["reciprocal"], 1, 0)
        if "factorial" in self.buttons:
            right_grid.addWidget(self.buttons["factorial"], 1, 1)
        top_row.addLayout(right_grid, stretch=1)

        root_layout.addLayout(top_row)

        # -------------------------------------------------------------
        # Tier 2: Scientific Function Tier (3 rows x 6 columns)
        # -------------------------------------------------------------
        func_grid = QGridLayout()
        func_grid.setContentsMargins(0, 2, 0, 2)
        func_grid.setSpacing(4)

        func_rows = [
            ["fraction", "sqrt", "square", "power", "log", "ln"],
            ["negative", "dms", "hyp", "sin", "cos", "tan"],
            ["rcl", "eng", "lparen", "rparen", "sd", "mplus"],
        ]

        for r_idx, row_keys in enumerate(func_rows):
            for c_idx, key_id in enumerate(row_keys):
                if key_id in self.buttons:
                    func_grid.addWidget(self.buttons[key_id], r_idx, c_idx)

        root_layout.addLayout(func_grid)

        # -------------------------------------------------------------
        # Tier 3: Numbers, Operators & Execution (4 rows x 5 columns)
        # -------------------------------------------------------------
        num_grid = QGridLayout()
        num_grid.setContentsMargins(0, 2, 0, 2)
        num_grid.setSpacing(4)

        num_rows = [
            ["7", "8", "9", "del", "ac"],
            ["4", "5", "6", "multiply", "divide"],
            ["1", "2", "3", "add", "subtract"],
            ["0", "dot", "exp10", "ans", "equals"],
        ]

        for r_idx, row_keys in enumerate(num_rows):
            for c_idx, key_id in enumerate(row_keys):
                if key_id in self.buttons:
                    num_grid.addWidget(self.buttons[key_id], r_idx, c_idx)

        root_layout.addLayout(num_grid)

        # -------------------------------------------------------------
        # Hidden extra keys container (retaining full REGISTRY membership)
        # -------------------------------------------------------------
        self._extra_container = QWidget(self)
        extra_layout = QHBoxLayout(self._extra_container)
        for key_id in ("percent", "pi", "comma", "random"):
            if key_id in self.buttons:
                extra_layout.addWidget(self.buttons[key_id])
        self._extra_container.hide()
        root_layout.addWidget(self._extra_container)
