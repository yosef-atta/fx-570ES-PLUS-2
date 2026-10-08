"""Controller for Phase 1 input and interaction state."""
from collections.abc import Callable
from .action import Action, Kind
from .key_registry import REGISTRY, resolve
from .state import ANGLES, MODES, CalculatorState

SETUP = ("MthIO-MathO", "LineIO", "DEG", "RAD", "GRA", "Fix", "Sci", "Norm", "ab/c", "d/c", "CMPLX", "STAT")
PAGE_SIZE = 6

class Controller:
    def __init__(self, state: CalculatorState | None = None):
        self.state = state if state is not None else CalculatorState()
        self.listeners: list[Callable[[CalculatorState], None]] = []

    def subscribe(self, callback: Callable[[CalculatorState], None]) -> None:
        self.listeners.append(callback)
        callback(self.state)

    def notify(self) -> None:
        self.state.validate()
        for callback in self.listeners:
            callback(self.state)

    def press(self, key_id: str) -> None:
        if key_id not in REGISTRY:
            raise KeyError(key_id)
        s = self.state
        if not s.power_on:
            if key_id == "on":
                s.power_on = True
                self.notify()
            return
        if s.active_menu:
            self._menu_key(key_id)
            self.notify()
            return
        if key_id in ("shift", "alpha"):
            if key_id == "shift":
                s.shift_active, s.alpha_active = not s.shift_active, False
            else:
                s.alpha_active, s.shift_active = not s.alpha_active, False
            self.notify()
            return
        modifier = "shift" if s.shift_active else "alpha" if s.alpha_active else None
        action = resolve(key_id, modifier)
        s.shift_active = s.alpha_active = False
        self.dispatch(action)

    def dispatch(self, action: Action) -> None:
        s = self.state
        s.last_action = action.name
        if action.kind is Kind.INSERT:
            position = s.cursor_position
            if s.input_mode == "Overwrite" and position < len(s.expression):
                s.expression = s.expression[:position] + action.text + s.expression[position + 1:]
            else:
                s.expression = s.expression[:position] + action.text + s.expression[position:]
            s.cursor_position += len(action.text)
            s.result = ""
        elif action.kind is Kind.DEFERRED:
            s.deferred_actions.append(action.name)
            s.result = "Not implemented (Phase 2/3)"
        elif action.name == "del":
            p = s.cursor_position
            if p:
                s.expression = s.expression[:p - 1] + s.expression[p:]
                s.cursor_position -= 1
            s.result = ""
        elif action.name == "ac":
            s.expression, s.cursor_position, s.result = "", 0, ""
        elif action.name == "left":
            s.cursor_position = max(0, s.cursor_position - 1)
        elif action.name == "right":
            s.cursor_position = min(len(s.expression), s.cursor_position + 1)
        elif action.name == "mode":
            self._open_menu("MODE")
        elif action.name == "setup":
            self._open_menu("SETUP")
        elif action.name == "off":
            s.power_on = False
            s.active_menu = None
        elif action.name == "on":
            s.power_on = True
        elif action.name == "insert_toggle":
            s.input_mode = "Overwrite" if s.input_mode == "Insert" else "Insert"
        self.notify()

    def _open_menu(self, name: str) -> None:
        s = self.state
        s.active_menu, s.menu_page, s.menu_selection = name, 0, 0

    def _menu_key(self, key_id: str) -> None:
        s = self.state
        options = MODES if s.active_menu == "MODE" else SETUP
        if key_id == "ac":
            s.active_menu = None
            return
        if key_id in ("left", "up"):
            s.menu_selection = max(0, s.menu_selection - 1)
        elif key_id in ("right", "down"):
            s.menu_selection = min(len(options) - 1, s.menu_selection + 1)
        elif key_id.isdigit() and key_id != "0":
            index = s.menu_page * PAGE_SIZE + int(key_id) - 1
            if int(key_id) <= PAGE_SIZE and index < len(options):
                self._select(options[index])
            return
        elif key_id == "equals":
            self._select(options[s.menu_selection])
            return
        else:
            return
        s.menu_page = s.menu_selection // PAGE_SIZE

    def _select(self, option: str) -> None:
        s = self.state
        if s.active_menu == "MODE":
            s.mode = option
        elif option in ANGLES:
            s.angle_unit = option
        elif option in ("MthIO-MathO", "LineIO"):
            s.display_format = option
        elif option in ("Fix", "Sci", "Norm"):
            s.number_format = option
        else:
            s.last_action = "setup:" + option
        s.active_menu, s.menu_page, s.menu_selection = None, 0, 0
