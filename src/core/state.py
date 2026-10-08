"""Interaction state, with no UI dependencies."""
from dataclasses import dataclass, field

MODES = ("COMP", "CMPLX", "STAT", "BASE-N", "EQN", "MATRIX", "TABLE", "VECTOR")
ANGLES = ("DEG", "RAD", "GRA")

@dataclass
class CalculatorState:
    expression: str = ""
    cursor_position: int = 0
    result: str = ""
    mode: str = "COMP"
    angle_unit: str = "DEG"
    display_format: str = "MthIO-MathO"
    number_format: str = "Norm 1"
    shift_active: bool = False
    alpha_active: bool = False
    active_menu: str | None = None
    menu_page: int = 0
    menu_selection: int = 0
    input_mode: str = "Insert"
    power_on: bool = True
    last_action: str = ""
    deferred_actions: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if self.mode not in MODES or self.angle_unit not in ANGLES:
            raise ValueError("Invalid mode or angle unit")
        if not 0 <= self.cursor_position <= len(self.expression):
            raise ValueError("Cursor out of bounds")
        if self.shift_active and self.alpha_active:
            raise ValueError("Both modifiers active")
