"""Controller for calculation engine, input dispatch, and interaction lifecycle across all 8 modes."""
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
from .modes.complex_engine import ComplexEngine
from .modes.stat_engine import StatEngine
from .modes.basen_engine import BaseNEngine
from .modes.eqn_engine import EqnEngine
from .modes.matrix_engine import MatrixEngine
from .modes.table_engine import TableEngine
from .modes.vector_engine import VectorEngine
from .modes.constants_conv import get_constant, convert_metric

SETUP = ("MthIO-MathO", "LineIO", "DEG", "RAD", "GRA", "Fix", "Sci", "Norm", "ab/c", "d/c", "CMPLX", "STAT")
CLR_OPTIONS = ("Setup", "Memory", "All")
CMPLX_OPTIONS = ("arg", "Conjg", "▶r∠θ", "▶a+bi")
STAT_OPTIONS = ("Type", "Data", "Sum", "Var", "Reg", "MinMax", "Distr")
STAT_TYPE_OPTIONS = ("1-VAR", "A+BX", "_+CX^2", "ln X", "e^X", "A•B^X", "A•X^B", "1/X")
STAT_SUM_OPTIONS = ("Σx²", "Σx", "n", "Σy²", "Σy", "Σxy")
STAT_VAR_OPTIONS = ("x̄", "σx", "sx", "ȳ", "σy", "sy")
STAT_REG_OPTIONS = ("A", "B", "r", "x̂", "ŷ")
STAT_MINMAX_OPTIONS = ("minX", "maxX", "minY", "maxY")
STAT_DISTR_OPTIONS = ("P(", "Q(", "R(", "▶t")
BASE_OPTIONS = ("and", "or", "xor", "xnor", "Not", "Neg", "d", "h", "b", "o")
EQN_OPTIONS = ("anX+bnY=cn", "anX+bnY+cnZ=dn", "aX²+bX+c=0", "aX³+bX²+cX+d=0")
MATRIX_OPTIONS = ("Dim", "Data", "MatA", "MatB", "MatC", "MatAns", "det", "Trn")
VECTOR_OPTIONS = ("Dim", "Data", "VctA", "VctB", "VctC", "VctAns", "Dot")

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

        # Phase 3 mode engines
        self.cmplx_engine = ComplexEngine(
            angle_unit=self.state.angle_unit,
            complex_format=self.state.complex_format
        )
        self.stat_engine = StatEngine()
        self.basen_engine = BaseNEngine(current_base=self.state.base_n_mode)
        self.eqn_engine = EqnEngine()
        self.matrix_engine = MatrixEngine()
        self.table_engine = TableEngine(angle_unit=self.state.angle_unit)
        self.vector_engine = VectorEngine()

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

        # Prompt input collection for CONST and CONV (e.g. 2 digits 01~40)
        if s.prompt_name in ("CONST", "CONV"):
            if key_id.isdigit():
                s.prompt_value += key_id
                if len(s.prompt_value) == 2:
                    code = int(s.prompt_value)
                    if s.prompt_name == "CONST":
                        try:
                            const_obj = get_constant(code)
                            self._insert_text(const_obj.symbol)
                        except Exception:
                            s.error_state = True
                            s.error_message = "Argument ERROR"
                    elif s.prompt_name == "CONV":
                        try:
                            if s.is_evaluated and s.result:
                                val = float(sp.N(self.memory.ans))
                                converted = convert_metric(code, val)
                                s.result = self.formatter.format_number(converted)
                                self.memory.store_result(f"CONV{code:02d}", sp.Float(converted), s.result)
                            else:
                                self._insert_text(f"CONV{code:02d}")
                        except Exception:
                            s.error_state = True
                            s.error_message = "Argument ERROR"
                    s.prompt_name = None
                    s.prompt_value = ""
                self.notify()
                return
            elif key_id in ("ac", "on"):
                s.prompt_name = None
                s.prompt_value = ""
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

        # Table Editor active navigation & entry
        if s.table_editor_active:
            if key_id == "ac":
                s.table_editor_active = False
                s.expression = ""
                s.cursor_position = 0
                s.result = ""
                s.is_evaluated = False
                self.notify()
                return
            elif key_id == "up":
                s.grid_row = max(0, s.grid_row - 1)
                self.notify()
                return
            elif key_id == "down":
                if s.grid_row + 1 < len(s.grid_data):
                    s.grid_row += 1
                elif s.mode == "STAT":
                    s.grid_data.append(["0"] * len(s.grid_headers))
                    s.grid_row += 1
                self.notify()
                return
            elif key_id == "left":
                s.grid_col = max(0, s.grid_col - 1)
                self.notify()
                return
            elif key_id == "right":
                if s.grid_headers:
                    s.grid_col = min(len(s.grid_headers) - 1, s.grid_col + 1)
                self.notify()
                return
            elif key_id == "equals":
                val = s.expression.strip() or "0"
                if 0 <= s.grid_row < len(s.grid_data) and 0 <= s.grid_col < len(s.grid_data[s.grid_row]):
                    s.grid_data[s.grid_row][s.grid_col] = val
                s.expression = ""
                s.cursor_position = 0
                if s.mode == "EQN":
                    if s.grid_col == len(s.grid_data[0]) - 1 and s.grid_row == len(s.grid_data) - 1:
                        self._solve_eqn()
                        self.notify()
                        return
                    elif s.grid_col + 1 < len(s.grid_data[0]):
                        s.grid_col += 1
                    else:
                        s.grid_col = 0
                        s.grid_row += 1
                elif s.mode == "STAT":
                    if s.grid_col + 1 < len(s.grid_headers):
                        s.grid_col += 1
                    else:
                        s.grid_col = 0
                        if s.grid_row + 1 < len(s.grid_data):
                            s.grid_row += 1
                        else:
                            s.grid_data.append(["0"] * len(s.grid_headers))
                            s.grid_row += 1
                self.notify()
                return

        # Direct Mode-specific keys
        if s.mode == "CMPLX":
            if key_id == "eng" and not s.shift_active and not s.alpha_active:
                self._insert_text("i")
                self.notify()
                return

        if s.mode == "BASE-N":
            if not s.shift_active and not s.alpha_active:
                if key_id == "square":
                    self._set_base("DEC")
                    self.notify()
                    return
                elif key_id == "power":
                    self._set_base("HEX")
                    self.notify()
                    return
                elif key_id == "log":
                    self._set_base("BIN")
                    self.notify()
                    return
                elif key_id == "ln":
                    self._set_base("OCT")
                    self.notify()
                    return
                elif key_id == "negative":
                    self._insert_text("A")
                    self.notify()
                    return
                elif key_id == "dms":
                    self._insert_text("B")
                    self.notify()
                    return
                elif key_id == "hyp":
                    self._insert_text("C")
                    self.notify()
                    return
                elif key_id == "sin":
                    self._insert_text("D")
                    self.notify()
                    return
                elif key_id == "cos":
                    self._insert_text("E")
                    self.notify()
                    return
                elif key_id == "tan":
                    self._insert_text("F")
                    self.notify()
                    return

        # Replay Navigation with ▲ / ▼
        if key_id == "up":
            if s.result_representations and len(s.result_representations) > 1:
                s.representation_index = (s.representation_index - 1) % len(s.result_representations)
                s.result = s.result_representations[s.representation_index]
                self.notify()
                return
            entry = self.memory.history_prev()
            if entry:
                s.expression = entry.expression
                s.cursor_position = len(entry.expression)
                s.result = entry.result
                s.is_evaluated = True
                self.notify()
                return
        elif key_id == "down":
            if s.result_representations and len(s.result_representations) > 1:
                s.representation_index = (s.representation_index + 1) % len(s.result_representations)
                s.result = s.result_representations[s.representation_index]
                self.notify()
                return
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
        elif action.name == "const":
            s.prompt_name = "CONST"
            s.prompt_value = ""
        elif action.name == "conv":
            s.prompt_name = "CONV"
            s.prompt_value = ""
        elif action.name == "arg":
            self._insert_text("arg(")
        elif action.name == "cmplx_menu":
            self._open_menu("CMPLX")
        elif action.name == "stat_menu":
            self._open_menu("STAT")
        elif action.name == "base_menu":
            self._open_menu("BASE")
        elif action.name == "matrix_menu":
            self._open_menu("MATRIX")
        elif action.name == "vector_menu":
            self._open_menu("VECTOR")
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

    def _set_base(self, base: str) -> None:
        self.state.base_n_mode = base
        self.basen_engine.current_base = base
        if self.state.is_evaluated and isinstance(self.memory.ans, int):
            self.state.result = self.basen_engine.format_value(self.memory.ans, base)

    def _sync_stat_engine(self) -> None:
        self.stat_engine.clear()
        for idx, row in enumerate(self.state.grid_data):
            if idx == len(self.state.grid_data) - 1 and row[0] in ("0", "") and len(self.state.grid_data) > 1:
                continue
            try:
                if len(row) == 1:
                    self.stat_engine.add_row(float(row[0].replace("−", "-")))
                elif len(row) == 2:
                    if "FREQ" in self.state.grid_headers:
                        self.stat_engine.add_row(float(row[0].replace("−", "-")), freq=int(float(row[1].replace("−", "-"))))
                    else:
                        self.stat_engine.add_row(float(row[0].replace("−", "-")), float(row[1].replace("−", "-")))
                elif len(row) >= 3:
                    self.stat_engine.add_row(float(row[0].replace("−", "-")), float(row[1].replace("−", "-")), freq=int(float(row[2].replace("−", "-"))))
            except Exception:
                pass

    def _solve_eqn(self) -> None:
        s = self.state
        sub = s.active_sub_mode

        def _fmt(val):
            if isinstance(val, (int, float)):
                if val == int(val):
                    return str(int(val))
                return f"{round(val, 9):.10f}".rstrip("0").rstrip(".")
            return str(val)

        try:
            if sub == "anX+bnY=cn" or (len(s.grid_data) == 2 and len(s.grid_data[0]) == 3):
                a1, b1, c1 = [float(x.replace("−", "-")) for x in s.grid_data[0]]
                a2, b2, c2 = [float(x.replace("−", "-")) for x in s.grid_data[1]]
                sol = self.eqn_engine.solve_linear_2(a1, b1, c1, a2, b2, c2)
                if sol.status != "Unique":
                    s.result = sol.status
                    s.result_representations = [sol.status]
                else:
                    reps = [f"X = {_fmt(sol.x)}", f"Y = {_fmt(sol.y)}"]
                    s.result_representations = reps
                    s.result = reps[0]
            elif sub == "anX+bnY+cnZ=dn" or (len(s.grid_data) == 3 and len(s.grid_data[0]) == 4):
                r1 = tuple(float(x.replace("−", "-")) for x in s.grid_data[0])
                r2 = tuple(float(x.replace("−", "-")) for x in s.grid_data[1])
                r3 = tuple(float(x.replace("−", "-")) for x in s.grid_data[2])
                sol = self.eqn_engine.solve_linear_3(r1, r2, r3)
                if sol.status != "Unique":
                    s.result = sol.status
                    s.result_representations = [sol.status]
                else:
                    reps = [f"X = {_fmt(sol.x)}", f"Y = {_fmt(sol.y)}", f"Z = {_fmt(sol.z)}"]
                    s.result_representations = reps
                    s.result = reps[0]
            elif sub == "aX²+bX+c=0" or (len(s.grid_data) == 1 and len(s.grid_data[0]) == 3):
                a, b, c = [float(x.replace("−", "-")) for x in s.grid_data[0]]
                sol = self.eqn_engine.solve_quadratic(a, b, c)
                reps = []
                for i, r in enumerate(sol.roots, 1):
                    reps.append(f"X{i} = {_fmt(r)}")
                if sol.x_vertex is not None and sol.y_vertex is not None:
                    reps.append(f"X-Value {sol.vertex_type} = {_fmt(sol.x_vertex)}")
                    reps.append(f"Y-Value {sol.vertex_type} = {_fmt(sol.y_vertex)}")
                s.result_representations = reps
                s.result = reps[0]
            elif sub == "aX³+bX²+cX+d=0" or (len(s.grid_data) == 1 and len(s.grid_data[0]) == 4):
                a, b, c, d = [float(x.replace("−", "-")) for x in s.grid_data[0]]
                sol = self.eqn_engine.solve_cubic(a, b, c, d)
                reps = [f"X{i} = {_fmt(r)}" for i, r in enumerate(sol.roots, 1)]
                s.result_representations = reps
                s.result = reps[0]
            s.is_evaluated = True
            s.table_editor_active = False
        except Exception:
            s.error_state = True
            s.error_message = "Math ERROR"
            s.result = "[AC]:Cancel  [◀][▶]:Goto"

    def _evaluate(self) -> None:
        s = self.state
        expr = s.expression.strip()
        if not expr:
            return

        # Base-N Mode evaluation
        if s.mode == "BASE-N":
            try:
                res_int = self.basen_engine.evaluate_expression(
                    expr,
                    ans=self.memory.ans if isinstance(self.memory.ans, int) else 0
                )
                s.result = self.basen_engine.format_value(res_int, s.base_n_mode)
                s.is_evaluated = True
                self.memory.store_result(expr, res_int, s.result)
                return
            except CalculatorError as e:
                s.error_state = True
                s.error_message = e.display_name
                s.result = "[AC]:Cancel  [◀][▶]:Goto"
                return
            except Exception:
                s.error_state = True
                s.error_message = "Math ERROR"
                s.result = "[AC]:Cancel  [◀][▶]:Goto"
                return

        # Matrix Mode evaluation
        if s.mode == "MATRIX":
            try:
                res_mat = self.matrix_engine.evaluate_expression(expr)
                s.result = self.matrix_engine.format_matrix(res_mat) if isinstance(res_mat, sp.Matrix) else str(res_mat)
                s.is_evaluated = True
                self.memory.store_result(expr, res_mat if isinstance(res_mat, (int, float, sp.Expr)) else 0, s.result)
                return
            except Exception as e:
                s.error_state = True
                s.error_message = "Dim ERROR" if "Dim" in str(e) else "Math ERROR"
                s.result = "[AC]:Cancel  [◀][▶]:Goto"
                return

        # Vector Mode evaluation
        if s.mode == "VECTOR":
            try:
                res_vct = self.vector_engine.evaluate_expression(expr)
                s.result = self.vector_engine.format_vector(res_vct) if isinstance(res_vct, list) else str(round(res_vct, 9))
                s.is_evaluated = True
                self.memory.store_result(expr, res_vct if not isinstance(res_vct, list) else 0, s.result)
                return
            except Exception as e:
                s.error_state = True
                s.error_message = "Dim ERROR" if "Dim" in str(e) else "Math ERROR"
                s.result = "[AC]:Cancel  [◀][▶]:Goto"
                return

        # Table Mode evaluation
        if s.mode == "TABLE":
            f_expr = expr[5:].strip() if expr.startswith("f(X)=") else expr
            try:
                rows = self.table_engine.generate(f_expr, start=1.0, end=5.0, step=1.0)
                s.grid_headers = ["", "X", "F(X)"]
                s.grid_data = [[str(r.row_num), str(r.x), str(r.f_val)] for r in rows]
                s.table_editor_active = True
                s.grid_row = 0
                s.grid_col = 0
                s.result = "Table Generated"
                s.is_evaluated = True
                return
            except Exception:
                s.error_state = True
                s.error_message = "Math ERROR"
                s.result = "[AC]:Cancel  [◀][▶]:Goto"
                return

        # General COMP / CMPLX / STAT Mode evaluation
        try:
            tokens = Lexer(expr).tokenize()
            ast = Parser(tokens).parse()
            evaluator = Evaluator(
                angle_unit=s.angle_unit,
                memory=self.memory.as_dict(),
                mode=s.mode
            )
            res = evaluator.evaluate(ast)
            self.formatter.number_format = s.number_format
            self.formatter.display_format = s.display_format
            reps = self.formatter.get_representations(res)

            s.result_representations = reps
            s.representation_index = 0
            s.result = reps[0]

            # In CMPLX mode, if polar format selected
            if s.mode == "CMPLX" and s.complex_format == "r∠θ" and len(reps) > 1:
                s.result = reps[1]
                s.representation_index = 1

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

    def _get_menu_options(self, menu_name: str) -> tuple[str, ...]:
        if menu_name == "MODE":
            return MODES
        elif menu_name == "SETUP":
            return SETUP
        elif menu_name == "CLR":
            return CLR_OPTIONS
        elif menu_name == "CMPLX":
            return CMPLX_OPTIONS
        elif menu_name == "STAT":
            return STAT_OPTIONS
        elif menu_name == "STAT_TYPE":
            return STAT_TYPE_OPTIONS
        elif menu_name == "STAT_SUM":
            return STAT_SUM_OPTIONS
        elif menu_name == "STAT_VAR":
            return STAT_VAR_OPTIONS
        elif menu_name == "STAT_REG":
            return STAT_REG_OPTIONS
        elif menu_name == "STAT_MINMAX":
            return STAT_MINMAX_OPTIONS
        elif menu_name == "STAT_DISTR":
            return STAT_DISTR_OPTIONS
        elif menu_name == "BASE":
            return BASE_OPTIONS
        elif menu_name == "EQN_TYPE":
            return EQN_OPTIONS
        elif menu_name == "MATRIX":
            return MATRIX_OPTIONS
        elif menu_name == "VECTOR":
            return VECTOR_OPTIONS
        return ()

    def _menu_key(self, key_id: str) -> None:
        s = self.state
        options = self._get_menu_options(s.active_menu or "")
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
            val = int(key_id)
            index_paged = s.menu_page * PAGE_SIZE + val - 1
            if val <= PAGE_SIZE and index_paged < len(options):
                self._select(options[index_paged])
                return
            if val - 1 < len(options):
                self._select(options[val - 1])
                return
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
        menu_name = s.active_menu

        if menu_name == "MODE":
            s.mode = option
            s.expression, s.cursor_position, s.result = "", 0, ""
            s.is_evaluated = False
            s.table_editor_active = False
            if option == "STAT":
                s.stat_type = "1-VAR"
                s.grid_headers = ["X"]
                s.grid_data = [["0"]]
                s.table_editor_active = True
            elif option == "EQN":
                s.active_sub_mode = "anX+bnY=cn"
                s.grid_headers = ["a", "b", "c"]
                s.grid_data = [["0", "0", "0"], ["0", "0", "0"]]
                s.table_editor_active = True
            elif option == "BASE-N":
                s.base_n_mode = "DEC"
            elif option == "TABLE":
                s.expression = "f(X)="
                s.cursor_position = len("f(X)=")
            s.active_menu, s.menu_page, s.menu_selection = None, 0, 0
            return
        elif menu_name == "STAT_TYPE":
            s.stat_type = option
            if option == "1-VAR":
                s.grid_headers = ["X"] if not s.stat_frequency_on else ["X", "FREQ"]
                s.grid_data = [["0"] * len(s.grid_headers)]
            else:
                s.grid_headers = ["X", "Y"] if not s.stat_frequency_on else ["X", "Y", "FREQ"]
                s.grid_data = [["0"] * len(s.grid_headers)]
            s.table_editor_active = True
            s.grid_row = 0
            s.grid_col = 0
        elif menu_name == "EQN_TYPE":
            s.active_sub_mode = option
            if option == "anX+bnY=cn":
                s.grid_headers = ["a", "b", "c"]
                s.grid_data = [["0", "0", "0"], ["0", "0", "0"]]
            elif option == "anX+bnY+cnZ=dn":
                s.grid_headers = ["a", "b", "c", "d"]
                s.grid_data = [["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"]]
            elif option == "aX²+bX+c=0":
                s.grid_headers = ["a", "b", "c"]
                s.grid_data = [["0", "0", "0"]]
            elif option == "aX³+bX²+cX+d=0":
                s.grid_headers = ["a", "b", "c", "d"]
                s.grid_data = [["0", "0", "0", "0"]]
            s.table_editor_active = True
            s.grid_row = 0
            s.grid_col = 0
        elif menu_name == "CMPLX":
            if option == "arg":
                self._insert_text("arg(")
            elif option == "Conjg":
                self._insert_text("Conjg(")
            elif option == "▶r∠θ":
                s.complex_format = "r∠θ"
                if s.is_evaluated and s.result:
                    s.result = self.cmplx_engine.format_complex(self.memory.ans, "r∠θ")
            elif option == "▶a+bi":
                s.complex_format = "a+bi"
                if s.is_evaluated and s.result:
                    s.result = self.cmplx_engine.format_complex(self.memory.ans, "a+bi")
        elif menu_name == "BASE":
            if option in ("Not", "Neg"):
                self._insert_text(f"{option}(")
            elif option in ("and", "or", "xor", "xnor"):
                self._insert_text(f" {option} ")
            elif option in ("d", "h", "b", "o"):
                self._insert_text(option)
        elif menu_name == "STAT":
            if option == "Type":
                self._open_menu("STAT_TYPE")
                return
            elif option == "Data":
                s.table_editor_active = True
            elif option == "Sum":
                self._open_menu("STAT_SUM")
                return
            elif option == "Var":
                self._open_menu("STAT_VAR")
                return
            elif option == "Reg":
                self._open_menu("STAT_REG")
                return
            elif option == "MinMax":
                self._open_menu("STAT_MINMAX")
                return
            elif option == "Distr":
                self._open_menu("STAT_DISTR")
                return
        elif menu_name == "STAT_SUM":
            self._sync_stat_engine()
            try:
                if option == "Σx": val = self.stat_engine.sum_x()
                elif option == "Σx²": val = self.stat_engine.sum_x2()
                elif option == "n": val = float(self.stat_engine.n())
                elif option == "Σy": val = self.stat_engine.sum_y()
                elif option == "Σy²": val = self.stat_engine.sum_y2()
                elif option == "Σxy": val = self.stat_engine.sum_xy()
                else: val = 0.0
                s.result = self.formatter.format_number(val)
                s.is_evaluated = True
                self.memory.store_result(option, sp.Float(val), s.result)
            except Exception:
                s.error_state = True
                s.error_message = "Math ERROR"
        elif menu_name == "STAT_VAR":
            self._sync_stat_engine()
            try:
                if option == "x̄": val = self.stat_engine.mean_x()
                elif option == "σx": val = self.stat_engine.sigma_x()
                elif option == "sx": val = self.stat_engine.sx()
                elif option == "ȳ": val = self.stat_engine.mean_y()
                elif option == "σy": val = self.stat_engine.sigma_y()
                elif option == "sy": val = self.stat_engine.sy()
                else: val = 0.0
                s.result = self.formatter.format_number(val)
                s.is_evaluated = True
                self.memory.store_result(option, sp.Float(val), s.result)
            except Exception:
                s.error_state = True
                s.error_message = "Math ERROR"
        elif menu_name == "STAT_REG":
            self._sync_stat_engine()
            try:
                a_val, b_val, r_val = self.stat_engine.linear_reg()
                if option == "A": val = a_val
                elif option == "B": val = b_val
                elif option == "r": val = r_val
                else: val = 0.0
                s.result = self.formatter.format_number(val)
                s.is_evaluated = True
                self.memory.store_result(option, sp.Float(val), s.result)
            except Exception:
                s.error_state = True
                s.error_message = "Math ERROR"
        elif menu_name == "STAT_MINMAX":
            self._sync_stat_engine()
            try:
                if option == "minX": val = self.stat_engine.min_x()
                elif option == "maxX": val = self.stat_engine.max_x()
                elif option == "minY": val = self.stat_engine.min_y()
                elif option == "maxY": val = self.stat_engine.max_y()
                else: val = 0.0
                s.result = self.formatter.format_number(val)
                s.is_evaluated = True
                self.memory.store_result(option, sp.Float(val), s.result)
            except Exception:
                s.error_state = True
                s.error_message = "Math ERROR"
        elif menu_name == "MATRIX":
            if option in ("MatA", "MatB", "MatC", "MatAns"):
                self._insert_text(option)
            elif option == "det":
                self._insert_text("det(")
            elif option == "Trn":
                self._insert_text("Trn(")
            elif option in ("Dim", "Data"):
                s.grid_headers = ["1", "2"]
                s.grid_data = [["0", "0"], ["0", "0"]]
                s.table_editor_active = True
                s.grid_row = 0
                s.grid_col = 0
        elif menu_name == "VECTOR":
            if option in ("VctA", "VctB", "VctC", "VctAns"):
                self._insert_text(option)
            elif option == "Dot":
                self._insert_text("•")
            elif option in ("Dim", "Data"):
                s.grid_headers = ["X", "Y", "Z"]
                s.grid_data = [["0", "0", "0"]]
                s.table_editor_active = True
                s.grid_row = 0
                s.grid_col = 0
        elif menu_name == "CLR":
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
