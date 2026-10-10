"""Memory registers (A-F, X, Y, M, Ans, PreAns) and Replay History buffer."""
from dataclasses import dataclass, field
import sympy as sp

VARIABLE_NAMES = ("A", "B", "C", "D", "E", "F", "X", "Y", "M")
MAX_HISTORY_SIZE = 30


@dataclass
class HistoryEntry:
    expression: str
    result: str


class MemoryManager:
    """Manages calculator variables, independent memory, Ans, and replay history."""

    def __init__(self):
        self.variables: dict[str, sp.Expr] = {v: sp.Integer(0) for v in VARIABLE_NAMES}
        self.ans: sp.Expr = sp.Integer(0)
        self.pre_ans: sp.Expr = sp.Integer(0)
        self.history: list[HistoryEntry] = []
        self.history_index: int | None = None  # None when in live editing

    def get_var(self, name: str) -> sp.Expr:
        name_upper = name.upper()
        if name_upper == "ANS":
            return self.ans
        if name_upper == "PREANS":
            return self.pre_ans
        return self.variables.get(name_upper, sp.Integer(0))

    def set_var(self, name: str, value: sp.Expr | int | float) -> None:
        name_upper = name.upper()
        val_expr = sp.sympify(value)
        if name_upper in self.variables:
            self.variables[name_upper] = val_expr

    def store_result(self, expr_str: str, result_val: sp.Expr, formatted_result: str) -> None:
        """Stores a calculation result into Ans/PreAns and records it in history."""
        self.pre_ans = self.ans
        self.ans = result_val

        # Add to history if not empty
        if expr_str:
            # Avoid duplicate consecutive entries
            if not self.history or self.history[-1].expression != expr_str:
                self.history.append(HistoryEntry(expression=expr_str, result=formatted_result))
                if len(self.history) > MAX_HISTORY_SIZE:
                    self.history.pop(0)
        self.history_index = None

    def m_plus(self, val: sp.Expr | int | float) -> None:
        self.variables["M"] += sp.sympify(val)

    def m_minus(self, val: sp.Expr | int | float) -> None:
        self.variables["M"] -= sp.sympify(val)

    @property
    def has_independent_memory(self) -> bool:
        """Returns True if M != 0 (causes 'M' indicator to appear on LCD)."""
        return self.variables.get("M", 0) != 0

    def clear_memory(self) -> None:
        """Clears all variables and Ans/PreAns."""
        for v in VARIABLE_NAMES:
            self.variables[v] = sp.Integer(0)
        self.ans = sp.Integer(0)
        self.pre_ans = sp.Integer(0)

    def clear_all(self) -> None:
        """Clears variables, Ans, and calculation history."""
        self.clear_memory()
        self.history.clear()
        self.history_index = None

    def history_prev(self) -> HistoryEntry | None:
        """Navigates to the previous (older) history entry on Up arrow."""
        if not self.history:
            return None
        if self.history_index is None:
            self.history_index = len(self.history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        return self.history[self.history_index]

    def history_next(self) -> HistoryEntry | None:
        """Navigates to the next (newer) history entry on Down arrow."""
        if not self.history or self.history_index is None:
            return None
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            return self.history[self.history_index]
        else:
            self.history_index = None
            return None

    def as_dict(self) -> dict[str, sp.Expr]:
        """Exports variable mappings for the evaluator."""
        d = dict(self.variables)
        d["Ans"] = self.ans
        d["PreAns"] = self.pre_ans
        return d
