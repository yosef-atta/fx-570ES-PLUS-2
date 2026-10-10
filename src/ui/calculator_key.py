"""Individual physical calculator button component for fx-570ES PLUS-2."""
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from src.core.key_registry import Key

BASE_N_LABELS = {
    "square": "DEC",
    "power": "HEX",
    "log": "BIN",
    "ln": "OCT",
}

class CalculatorKey(QPushButton):
    triggered = Signal(str)

    def __init__(self, specification: Key, parent=None, is_dpad: bool = False):
        super().__init__(parent)
        self.specification = specification
        self.setObjectName("key_" + specification.id)
        self.setProperty("category", specification.category)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Mark special key types for styling
        if specification.id in ("shift", "alpha", "mode", "on"):
            self.setProperty("shape", "oval")
            self.setMinimumWidth(44)
            self.setMinimumHeight(28)
        elif specification.id in ("up", "down", "left", "right") or is_dpad:
            self.setProperty("shape", "dpad")
            self.setMinimumWidth(26)
            self.setMinimumHeight(24)
        elif specification.id in ("del", "ac"):
            self.setProperty("accent", "green")
            self.setMinimumWidth(50)
            self.setMinimumHeight(38)
        elif specification.category == "number":
            self.setProperty("is_number", "true")
            self.setMinimumWidth(50)
            self.setMinimumHeight(38)
        else:
            self.setMinimumWidth(46)
            self.setMinimumHeight(32)

        tooltip_parts = [specification.label]
        if specification.shift:
            tooltip_parts.append("SHIFT: " + specification.shift_label)
        if specification.alpha:
            tooltip_parts.append("ALPHA: " + specification.alpha_label)
        if specification.id in BASE_N_LABELS:
            tooltip_parts.append("BASE: " + BASE_N_LABELS[specification.id])
        self.setToolTip(" | ".join(tooltip_parts))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 1, 3, 2)
        layout.setSpacing(0)

        # Top sub-labels row (SHIFT in gold, BASE/ALPHA in cyan/pink)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(1)

        self.shift_lbl = QLabel(specification.shift_label or "")
        self.shift_lbl.setObjectName("shift_sublabel")
        self.shift_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        top_layout.addWidget(self.shift_lbl, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        top_layout.addStretch()

        # Extra label (e.g. Base-N like DEC, HEX)
        if specification.id in BASE_N_LABELS:
            self.base_lbl = QLabel(BASE_N_LABELS[specification.id])
            self.base_lbl.setObjectName("base_sublabel")
            self.base_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            top_layout.addWidget(self.base_lbl, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            top_layout.addStretch()
        else:
            self.base_lbl = None

        self.alpha_lbl = QLabel(specification.alpha_label or "")
        self.alpha_lbl.setObjectName("alpha_sublabel")
        self.alpha_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        top_layout.addWidget(self.alpha_lbl, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        layout.addLayout(top_layout)

        # Main key label
        self.main_lbl = QLabel(specification.label)
        self.main_lbl.setObjectName("main_key_label")
        self.main_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        layout.addWidget(self.main_lbl)

        self.clicked.connect(lambda: self.triggered.emit(specification.id))

    def text(self) -> str:
        return self.specification.label
