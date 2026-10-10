"""Equation solver (SOLVE) using Newton-Raphson method and CALC expression evaluation."""
from dataclasses import dataclass
import sympy as sp
from .ast_nodes import ASTNode, VariableNode, EquationNode
from .errors import CantSolveError
from .evaluator import Evaluator

@dataclass
class SolveResult:
    solution: float
    residual: float  # L - R residual error


class Solver:
    """Solves algebraic equations and manages CALC variable extraction."""

    def __init__(self, angle_unit: str = "DEG"):
        self.angle_unit = angle_unit

    def solve(
        self,
        node: ASTNode,
        initial_guess: float = 0.0,
        memory: dict[str, sp.Expr | float] | None = None,
        max_iter: int = 100,
        tol: float = 1e-10
    ) -> SolveResult:
        """Finds numerical root of an equation f(X)=0 or f(X)=g(X) for variable X."""
        mem = dict(memory) if memory else {}

        # Define residual function F(x) = LHS - RHS
        def f(x_val: float) -> float:
            mem["X"] = x_val
            evaluator = Evaluator(angle_unit=self.angle_unit, memory=mem)
            try:
                res = evaluator.evaluate(node)
                return float(res.numeric) if res.numeric is not None else float(sp.N(res.exact))
            except Exception:
                return float("nan")

        x = initial_guess
        h = 1e-7

        for _ in range(max_iter):
            fx = f(x)
            if fx != fx:  # NaN
                x += 0.1
                continue

            if abs(fx) < tol:
                return SolveResult(solution=round(x, 10), residual=round(fx, 12))

            # Numerical derivative via central difference
            f_plus = f(x + h)
            f_minus = f(x - h)
            df = (f_plus - f_minus) / (2 * h)

            if abs(df) < 1e-14 or df != df:
                # Derivative too small or NaN, perturb guess
                x += 0.5
                continue

            delta = fx / df
            x_new = x - delta

            if abs(delta) < 1e-11 and abs(fx) < 1e-6:
                return SolveResult(solution=round(x_new, 10), residual=round(f(x_new), 12))

            x = x_new

        # Final check
        fx = f(x)
        if abs(fx) < 1e-5:
            return SolveResult(solution=round(x, 10), residual=round(fx, 12))

        raise CantSolveError("Can't Solve")

    @staticmethod
    def extract_variables(node: ASTNode) -> list[str]:
        """Finds all distinct variables present in an AST."""
        found: set[str] = set()

        def visit(n: ASTNode):
            if n is None:
                return
            if isinstance(n, VariableNode):
                found.add(n.name.upper())
            # Recursively inspect child attributes
            for attr in dir(n):
                if attr.startswith("_"):
                    continue
                val = getattr(n, attr, None)
                if isinstance(val, ASTNode):
                    visit(val)
                elif isinstance(val, (list, tuple)):
                    for item in val:
                        if isinstance(item, ASTNode):
                            visit(item)

        visit(node)
        return sorted(list(found))
