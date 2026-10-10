"""Equation calculations (EQN Mode) solving linear systems and polynomials."""
from dataclasses import dataclass
import sympy as sp
from src.core.math.errors import MathError

@dataclass
class LinearSystemSolution:
    x: float | sp.Expr
    y: float | sp.Expr
    z: float | sp.Expr | None = None
    status: str = "Unique"  # "Unique", "No Solution", "Infinite Sol"


@dataclass
class PolynomialSolution:
    roots: list[complex | float | sp.Expr]
    x_vertex: float | None = None
    y_vertex: float | None = None
    vertex_type: str | None = None  # "Min" or "Max"


class EqnEngine:
    """Solves simultaneous linear equations and 2nd/3rd degree polynomials."""

    @staticmethod
    def solve_linear_2(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float) -> LinearSystemSolution:
        """Solves a1*X + b1*Y = c1, a2*X + b2*Y = c2."""
        d = (a1 * b2) - (a2 * b1)
        dx = (c1 * b2) - (c2 * b1)
        dy = (a1 * c2) - (a2 * c1)

        if abs(d) < 1e-12:
            if abs(dx) < 1e-12 and abs(dy) < 1e-12:
                return LinearSystemSolution(x=0, y=0, status="Infinite Sol")
            return LinearSystemSolution(x=0, y=0, status="No Solution")

        x_sol = dx / d
        y_sol = dy / d
        return LinearSystemSolution(x=round(x_sol, 10), y=round(y_sol, 10))

    @staticmethod
    def solve_linear_3(
        row1: tuple[float, float, float, float],
        row2: tuple[float, float, float, float],
        row3: tuple[float, float, float, float]
    ) -> LinearSystemSolution:
        """Solves 3x3 linear system."""
        a1, b1, c1, d1 = row1
        a2, b2, c2, d2 = row2
        a3, b3, c3, d3 = row3

        m = sp.Matrix([
            [a1, b1, c1],
            [a2, b2, c2],
            [a3, b3, c3]
        ])
        det_m = m.det()

        if abs(float(det_m)) < 1e-12:
            # Check augmented matrix rank
            aug = sp.Matrix([
                [a1, b1, c1, d1],
                [a2, b2, c2, d2],
                [a3, b3, c3, d3]
            ])
            if aug.rank() == m.rank():
                return LinearSystemSolution(x=0, y=0, z=0, status="Infinite Sol")
            return LinearSystemSolution(x=0, y=0, z=0, status="No Solution")

        b_vec = sp.Matrix([d1, d2, d3])
        sol = m.LUsolve(b_vec)

        return LinearSystemSolution(
            x=round(float(sol[0]), 10),
            y=round(float(sol[1]), 10),
            z=round(float(sol[2]), 10)
        )

    @staticmethod
    def solve_quadratic(a: float, b: float, c: float) -> PolynomialSolution:
        """Solves aX² + bX + c = 0 and computes vertex coordinates."""
        if a == 0:
            raise MathError("EQN: coefficient a cannot be zero")

        disc = (b ** 2) - (4 * a * c)
        roots: list[complex | float] = []

        if abs(disc) < 1e-14:
            # Single repeated root
            r = -b / (2 * a)
            roots = [round(r, 10)]
        elif disc > 0:
            # Two real roots
            sqrt_d = disc ** 0.5
            r1 = (-b + sqrt_d) / (2 * a)
            r2 = (-b - sqrt_d) / (2 * a)
            roots = [round(r1, 10), round(r2, 10)]
        else:
            # Two complex conjugate roots
            sqrt_d = (-disc) ** 0.5
            real = -b / (2 * a)
            imag = sqrt_d / (2 * a)
            roots = [complex(round(real, 10), round(imag, 10)), complex(round(real, 10), round(-imag, 10))]

        # Parabola vertex coordinates
        x_v = -b / (2 * a)
        y_v = c - (b ** 2) / (4 * a)
        v_type = "Min" if a > 0 else "Max"

        return PolynomialSolution(
            roots=roots,
            x_vertex=round(x_v, 10),
            y_vertex=round(y_v, 10),
            vertex_type=v_type
        )

    @staticmethod
    def solve_cubic(a: float, b: float, c: float, d: float) -> PolynomialSolution:
        """Solves aX³ + bX² + cX + d = 0."""
        if a == 0:
            raise MathError("EQN: coefficient a cannot be zero")

        x = sp.Symbol("x")
        poly = a * x**3 + b * x**2 + c * x + d
        sol_roots = sp.roots(poly)

        roots_list: list[complex | float] = []
        for r, mult in sol_roots.items():
            for _ in range(mult):
                c_val = complex(sp.N(r))
                if abs(c_val.imag) < 1e-10:
                    roots_list.append(round(c_val.real, 10))
                else:
                    roots_list.append(complex(round(c_val.real, 10), round(c_val.imag, 10)))

        # Fallback if symbolic roots returned fewer than 3
        if len(roots_list) < 3:
            num_roots = sp.nroots(poly)
            roots_list = [complex(r) if abs(complex(r).imag) > 1e-10 else round(complex(r).real, 10) for r in num_roots]

        return PolynomialSolution(roots=roots_list)
