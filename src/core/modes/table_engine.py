"""Function table generation (TABLE Mode) for f(X) and optional g(X)."""
from dataclasses import dataclass
import sympy as sp
from src.core.math.errors import MathError
from src.core.math.evaluator import Evaluator
from src.core.math.lexer import Lexer
from src.core.math.parser import Parser

MAX_TABLE_ROWS = 30

@dataclass
class TableRow:
    row_num: int
    x: float
    f_val: str
    g_val: str | None = None


class TableEngine:
    """Generates numerical tables for mathematical functions."""

    def __init__(self, angle_unit: str = "DEG"):
        self.angle_unit = angle_unit

    def generate(
        self,
        f_expr_str: str,
        start: float,
        end: float,
        step: float,
        g_expr_str: str | None = None
    ) -> list[TableRow]:
        """Generates table rows from start to end with step interval."""
        if step <= 0 or start > end:
            raise MathError("TABLE: invalid range or step <= 0")

        num_steps = int(round((end - start) / step)) + 1
        if num_steps > MAX_TABLE_ROWS:
            raise MathError("Insufficient MEM (max 30 table rows)")

        # Parse ASTs
        f_ast = Parser(Lexer(f_expr_str).tokenize()).parse()
        g_ast = Parser(Lexer(g_expr_str).tokenize()).parse() if g_expr_str else None

        rows: list[TableRow] = []

        for i in range(num_steps):
            x_val = start + i * step
            # Avoid float drift
            x_val = round(x_val, 8)

            # Evaluate f(X)
            mem_f = {"X": x_val}
            evaluator_f = Evaluator(angle_unit=self.angle_unit, memory=mem_f)
            try:
                res_f = evaluator_f.evaluate(f_ast)
                f_str = f"{float(res_f.numeric):.5f}".rstrip("0").rstrip(".") if res_f.numeric is not None else str(res_f.exact)
                if not f_str:
                    f_str = "0"
            except Exception:
                f_str = "ERROR"

            # Evaluate g(X) if provided
            g_str = None
            if g_ast:
                mem_g = {"X": x_val}
                evaluator_g = Evaluator(angle_unit=self.angle_unit, memory=mem_g)
                try:
                    res_g = evaluator_g.evaluate(g_ast)
                    g_str = f"{float(res_g.numeric):.5f}".rstrip("0").rstrip(".") if res_g.numeric is not None else str(res_g.exact)
                    if not g_str:
                        g_str = "0"
                except Exception:
                    g_str = "ERROR"

            rows.append(TableRow(row_num=i + 1, x=x_val, f_val=f_str, g_val=g_str))

        return rows
