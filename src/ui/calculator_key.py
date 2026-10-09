"""One button per physical key, with no calculator state logic."""
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from src.core.key_registry import Key

class CalculatorKey(QPushButton):
    triggered = Signal(str)

    def __init__(self, specification: Key, parent=None):
        super().__init__(parent)
        self.specification = specification
        self.setObjectName("key_" + specification.id)
        self.setProperty("category", specification.category)
        self.setMinimumWidth(58)
        self.setMinimumHeight(44)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setToolTip(" | ".join(x for x in (specification.label,
                        "SHIFT: " + specification.shift_label if specification.shift else "",
                        "ALPHA: " + specification.alpha_label if specification.alpha else "") if x))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 3)
        layout.setSpacing(0)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(2)

        self.shift_lbl = QLabel(specification.shift_label or "")
        self.shift_lbl.setObjectName("shift_sublabel")
        self.shift_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        top_layout.addWidget(self.shift_lbl, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        top_layout.addStretch()

        self.alpha_lbl = QLabel(specification.alpha_label or "")
        self.alpha_lbl.setObjectName("alpha_sublabel")
        self.alpha_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        top_layout.addWidget(self.alpha_lbl, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        layout.addLayout(top_layout)

        self.main_lbl = QLabel(specification.label)
        self.main_lbl.setObjectName("main_key_label")
        self.main_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        layout.addWidget(self.main_lbl)

        self.clicked.connect(lambda: self.triggered.emit(specification.id))

    def text(self) -> str:
        return self.specification.label

