"""Interaction state with multi-mode calculator support, with no UI dependencies."""
from dataclasses import dataclass, field

MODES = ("COMP", "CMPLX", "STAT", "BASE-N", "EQN", "MATRIX", "TABLE", "VECTOR")
ANGLES = ("DEG", "RAD", "GRA")
DISPLAY_FORMATS = ("MthIO-MathO", "MthIO-LineO", "LineIO")
NUMBER_FORMATS = ("Norm 1", "Norm 2", "Fix", "Sci")
BASE_N_BASES = ("DEC", "HEX", "BIN", "OCT")

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

    # Phase 2 fields
    is_evaluated: bool = False
    error_state: bool = False
    error_message: str = ""
    error_position: int | None = None
    has_memory: bool = False
    result_representations: list[str] = field(default_factory=list)
    representation_index: int = 0
    eng_shift: int | None = None
    prompt_name: str | None = None
    prompt_value: str = ""
    pending_memory_op: str | None = None  # "STO" or "RCL"

    # Phase 3 fields
    complex_format: str = "a+bi"          # "a+bi" or "r∠θ"
    base_n_mode: str = "DEC"              # "DEC", "HEX", "BIN", "OCT"
    stat_type: str | None = None          # "1-VAR", "A+BX", etc.
    stat_frequency_on: bool = False
    table_editor_active: bool = False
    active_sub_mode: str | None = None
    grid_data: list[list[str]] = field(default_factory=list)
    grid_headers: list[str] = field(default_factory=list)
    grid_row: int = 0
    grid_col: int = 0

    def validate(self) -> None:
        if self.mode not in MODES or self.angle_unit not in ANGLES:
            raise ValueError("Invalid mode or angle unit")
        if not 0 <= self.cursor_position <= len(self.expression):
            raise ValueError("Cursor out of bounds")
        if self.shift_active and self.alpha_active:
            raise ValueError("Both modifiers active")
        if self.base_n_mode not in BASE_N_BASES:
            raise ValueError("Invalid Base-N base")

    def reset(self) -> None:
        self.expression = ""
        self.cursor_position = 0
        self.result = ""
        self.shift_active = False
        self.alpha_active = False
        self.active_menu = None
        self.menu_page = 0
        self.menu_selection = 0
        self.last_action = ""
        self.is_evaluated = False
        self.error_state = False
        self.error_message = ""
        self.error_position = None
        self.result_representations = []
        self.representation_index = 0
        self.eng_shift = None
        self.prompt_name = None
        self.prompt_value = ""
        self.pending_memory_op = None
        self.table_editor_active = False
        self.grid_data = []
        self.grid_headers = []
        self.grid_row = 0
        self.grid_col = 0
