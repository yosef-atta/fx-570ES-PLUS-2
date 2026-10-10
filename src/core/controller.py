"""Controller for calculation engine, input dispatch, and interaction lifecycle."""
from collections.abc import Callable
import sympy as sp
from .action import Action, Kind
from .key_registry import REGISTRY, resolve
from .math.errors import CalculatorError, MathError, SyntaxError
from .math.evaluator import Evaluator
from .math.formatter import Formatter
from .math.lexer import Lexer
from .math.memory import MemoryManager
from .math.parser import Parser
from .math.solver import Solver
from .state import ANGLES, MODES, CalculatorState

SETUP = ("MthIO-MathO", "LineIO", "DEG", "RAD", "GRA", "Fix", "Sci", "Norm", "ab/c", "d/c", "CMPLX", "STAT")
CLR_OPTIONS = ("Setup", "Memory", "All")
PAGE_SIZE = 6

OPERATOR_PREFIXES = ("+", "−", "-", "×", "*", "÷", "/", "^", "²", "³", "⁻¹", "!", "%")


class Controller:
    def __init__(self, state: CalculatorState | None = None):
        self.state = state if state is not None else CalculatorState()
        self.memory = MemoryManager()
        self.formatter = Formatter(
            number_format=self.state.number_format,
            display_format=self.state.display_format
        )
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

        # Handle calculator powered off
        if not s.power_on:
            if key_id == "on":
                s.power_on = True
                s.shift_active = False
                s.alpha_active = False
                s.active_menu = None
                self.notify()
            return

        # Power On button always resets expression and state
        if key_id == "on":
            s.power_on = True
            s.active_menu = None
            s.shift_active = False
            s.alpha_active = False
            s.reset()
            self.notify()
            return

        # Handle Error Screen: only AC or ◀/▶
        if s.error_state:
            if key_id == "ac":
                s.error_state = False
                s.error_message = ""
                s.expression = ""
                s.cursor_position = 0
                s.result = ""
                self.notify()
                return
            elif key_id in ("left", "right"):
                # Goto error locus
                s.error_state = False
                s.error_message = ""
                s.result = ""
                if s.error_position is not None:
                    s.cursor_position = min(len(s.expression), max(0, s.error_position))
                self.notify()
                return
            else:
                return

        # Handle Menu input
        if s.active_menu:
            self._menu_key(key_id)
            self.notify()
            return

        # Handle STO / RCL pending operations
        if s.pending_memory_op:
            act = resolve(key_id, "alpha")
            s.shift_active = s.alpha_active = False
            var_name = act.text.upper() if act.text else key_id.upper()
            if var_name in ("A", "B", "C", "D", "E", "F", "X", "Y", "M"):
                if s.pending_memory_op == "STO":
                    if not s.is_evaluated and s.expression:
                        self._evaluate()
                    self.memory.set_var(var_name, self.memory.ans)
                    s.result = f"{var_name} = {self.memory.get_var(var_name)}"
                elif s.pending_memory_op == "RCL":
                    val_str = str(self.memory.get_var(var_name))
                    self._insert_text(val_str)
            s.pending_memory_op = None
            self.notify()
            return

        # Replay Navigation with ▲ / ▼
        if key_id == "up":
            entry = self.memory.history_prev()
            if entry:
                s.expression = entry.expression
                s.cursor_position = len(entry.expression)
                s.result = entry.result
                s.is_evaluated = True
                self.notify()
                return
        elif key_id == "down":
            entry = self.memory.history_next()
            if entry:
                s.expression = entry.expression
                s.cursor_position = len(entry.expression)
                s.result = entry.result
                s.is_evaluated = True
            else:
                s.expression = ""
                s.cursor_position = 0
                s.result = ""
                s.is_evaluated = False
            self.notify()
            return

        # Toggle SHIFT and ALPHA
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
        if not s.power_on and action.name != "on":
            return
        s.last_action = action.name

        # Auto-Ans chaining when evaluated
        if s.is_evaluated and action.kind is Kind.INSERT:
            if action.text.startswith(OPERATOR_PREFIXES):
                s.expression = "Ans"
                s.cursor_position = len("Ans")
                s.result = ""
                s.is_evaluated = False
            else:
                s.expression = ""
                s.cursor_position = 0
                s.result = ""
                s.is_evaluated = False
                s.result_representations = []
                s.representation_index = 0
                s.eng_shift = None

        if action.kind is Kind.INSERT:
            self._insert_text(action.text)
        elif action.name == "evaluate":
            self._evaluate()
        elif action.name == "sd":
            self._toggle_sd()
        elif action.name == "mixed_sd":
            self._toggle_mixed_sd()
        elif action.name == "eng":
            self._shift_eng(0 if s.eng_shift is None else -1)
        elif action.name == "arrow_eng":
            self._shift_eng(+1)
        elif action.name == "mplus":
            self._m_plus()
        elif action.name == "mminus":
            self._m_minus()
        elif action.name == "sto":
            s.pending_memory_op = "STO"
        elif action.name == "rcl":
            s.pending_memory_op = "RCL"
        elif action.name == "clr":
            self._open_menu("CLR")
        elif action.name == "calc":
            self._evaluate()
        elif action.name == "solve":
            self._solve()
        elif action.name == "del":
            p = s.cursor_position
            if p:
                s.expression = s.expression[:p - 1] + s.expression[p:]
                s.cursor_position -= 1
            s.result = ""
            s.is_evaluated = False
        elif action.name == "ac":
            s.expression, s.cursor_position, s.result = "", 0, ""
            s.is_evaluated = False
            s.error_state = False
            s.error_message = ""
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
            s.shift_active = False
            s.alpha_active = False
        elif action.name == "on":
            s.power_on = True
            s.reset()
        elif action.name == "insert_toggle":
            s.input_mode = "Overwrite" if s.input_mode == "Insert" else "Insert"
        elif action.kind is Kind.DEFERRED:
            s.deferred_actions.append(action.name)
            s.result = f"Not implemented: {action.name}"

        self.notify()

    def _insert_text(self, text: str) -> None:
        s = self.state
        position = s.cursor_position
        if s.input_mode == "Overwrite" and position < len(s.expression):
            end_pos = min(len(s.expression), position + len(text))
            s.expression = s.expression[:position] + text + s.expression[end_pos:]
        else:
            s.expression = s.expression[:position] + text + s.expression[position:]
        s.cursor_position += len(text)
        s.result = ""
        s.is_evaluated = False

    def _evaluate(self) -> None:
        s = self.state
        expr = s.expression.strip()
        if not expr:
            return

        try:
            tokens = Lexer(expr).tokenize()
            ast = Parser(tokens).parse()
            evaluator = Evaluator(
                angle_unit=s.angle_unit,
                memory=self.memory.as_dict()
            )
            res = evaluator.evaluate(ast)
            self.formatter.number_format = s.number_format
            self.formatter.display_format = s.display_format
            reps = self.formatter.get_representations(res)

            s.result_representations = reps
            s.representation_index = 0
            s.result = reps[0]
            s.is_evaluated = True
            s.eng_shift = None

            # Store in memory and history
            self.memory.store_result(expr, res.exact, s.result)

        except CalculatorError as e:
            s.error_state = True
            s.error_message = e.display_name
            s.error_position = e.position
            s.result = "[AC]:Cancel  [◀][▶]:Goto"
        except Exception:
            s.error_state = True
            s.error_message = "Math ERROR"
            s.error_position = 0
            s.result = "[AC]:Cancel  [◀][▶]:Goto"

    def _toggle_sd(self) -> None:
        s = self.state
        if s.result_representations:
            s.representation_index = (s.representation_index + 1) % len(s.result_representations)
            s.result = s.result_representations[s.representation_index]

    def _toggle_mixed_sd(self) -> None:
        s = self.state
        if len(s.result_representations) >= 2:
            s.representation_index = 1 if s.representation_index == 0 else 0
            s.result = s.result_representations[s.representation_index]

    def _shift_eng(self, delta: int) -> None:
        s = self.state
        if s.eng_shift is None:
            s.eng_shift = delta
        else:
            s.eng_shift += delta

        if s.is_evaluated:
            try:
                val = float(sp.N(self.memory.ans))
                s.result = self.formatter.format_number(val, eng_shift=s.eng_shift)
            except Exception:
                pass

    def _m_plus(self) -> None:
        s = self.state
        self._evaluate()
        if not s.error_state:
            self.memory.m_plus(self.memory.ans)
            s.has_memory = self.memory.has_independent_memory

    def _m_minus(self) -> None:
        s = self.state
        self._evaluate()
        if not s.error_state:
            self.memory.m_minus(self.memory.ans)
            s.has_memory = self.memory.has_independent_memory

    def _solve(self) -> None:
        s = self.state
        try:
            tokens = Lexer(s.expression).tokenize()
            ast = Parser(tokens).parse()
            solver = Solver(angle_unit=s.angle_unit)
            guess = float(self.memory.get_var("X"))
            res = solver.solve(ast, initial_guess=guess, memory=self.memory.as_dict())
            s.result = f"X={res.solution}  L-R={res.residual}"
            s.is_evaluated = True
            self.memory.set_var("X", res.solution)
            self.memory.store_result(s.expression, sp.Float(res.solution), s.result)
        except CalculatorError as e:
            s.error_state = True
            s.error_message = e.display_name
            s.error_position = e.position
            s.result = "[AC]:Cancel  [◀][▶]:Goto"
        except Exception:
            s.error_state = True
            s.error_message = "Can't Solve"
            s.error_position = 0
            s.result = "[AC]:Cancel  [◀][▶]:Goto"

    def _open_menu(self, name: str) -> None:
        s = self.state
        s.active_menu, s.menu_page, s.menu_selection = name, 0, 0

    def _menu_key(self, key_id: str) -> None:
        s = self.state
        options = MODES if s.active_menu == "MODE" else CLR_OPTIONS if s.active_menu == "CLR" else SETUP
        if key_id in ("ac", "on"):
            s.active_menu = None
            s.menu_page = 0
            s.menu_selection = 0
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
            if 0 <= s.menu_selection < len(options):
                self._select(options[s.menu_selection])
            return
        else:
            return
        s.menu_page = s.menu_selection // PAGE_SIZE

    def _select(self, option: str) -> None:
        s = self.state
        if s.active_menu == "MODE":
            s.mode = option
        elif s.active_menu == "CLR":
            if option == "Setup":
                s.angle_unit = "DEG"
                s.number_format = "Norm 1"
                s.display_format = "MthIO-MathO"
            elif option == "Memory":
                self.memory.clear_memory()
                s.has_memory = False
            elif option == "All":
                self.memory.clear_all()
                s.has_memory = False
                s.reset()
        elif option in ANGLES:
            s.angle_unit = option
        elif option in ("MthIO-MathO", "LineIO"):
            s.display_format = option
        elif option in ("Fix", "Sci", "Norm"):
            s.number_format = option
        else:
            s.last_action = "setup:" + option
        s.active_menu, s.menu_page, s.menu_selection = None, 0, 0
