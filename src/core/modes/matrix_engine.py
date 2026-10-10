"""Matrix calculations (MATRIX Mode) supporting dimensions up to 3x3, det, Trn, and inverse."""
import sympy as sp
from src.core.math.errors import MathError

class MatrixEngine:
    """Manages matrix storage (MatA, MatB, MatC, MatAns) and algebraic operations."""

    def __init__(self):
        self.matrices: dict[str, sp.Matrix | None] = {
            "MATA": None,
            "MATB": None,
            "MATC": None,
            "MATANS": None,
        }

    def set_matrix(self, name: str, data: list[list[float | int]]) -> None:
        name_upper = name.upper()
        if not (1 <= len(data) <= 3 and all(1 <= len(row) <= 3 for row in data)):
            raise MathError("Matrix dimension must be between 1x1 and 3x3")
        self.matrices[name_upper] = sp.Matrix(data)

    def get_matrix(self, name: str) -> sp.Matrix:
        name_upper = name.upper()
        m = self.matrices.get(name_upper)
        if m is None:
            raise MathError(f"Matrix {name} is empty")
        return m

    def add(self, a_name: str, b_name: str) -> sp.Matrix:
        m1 = self.get_matrix(a_name)
        m2 = self.get_matrix(b_name)
        if m1.shape != m2.shape:
            raise MathError("Dim ERROR (matrices must have same dimensions)")
        res = m1 + m2
        self.matrices["MATANS"] = res
        return res

    def sub(self, a_name: str, b_name: str) -> sp.Matrix:
        m1 = self.get_matrix(a_name)
        m2 = self.get_matrix(b_name)
        if m1.shape != m2.shape:
            raise MathError("Dim ERROR (matrices must have same dimensions)")
        res = m1 - m2
        self.matrices["MATANS"] = res
        return res

    def mul(self, a_name: str, b_name: str) -> sp.Matrix:
        m1 = self.get_matrix(a_name)
        m2 = self.get_matrix(b_name)
        if m1.shape[1] != m2.shape[0]:
            raise MathError("Dim ERROR (inner dimensions must match)")
        res = m1 * m2
        self.matrices["MATANS"] = res
        return res

    def scalar_mul(self, k: float, a_name: str) -> sp.Matrix:
        m = self.get_matrix(a_name)
        res = k * m
        self.matrices["MATANS"] = res
        return res

    def det(self, a_name: str) -> float | sp.Expr:
        m = self.get_matrix(a_name)
        if m.shape[0] != m.shape[1]:
            raise MathError("Dim ERROR (matrix must be square)")
        return m.det()

    def trn(self, a_name: str) -> sp.Matrix:
        m = self.get_matrix(a_name)
        res = m.T
        self.matrices["MATANS"] = res
        return res

    def inverse(self, a_name: str) -> sp.Matrix:
        m = self.get_matrix(a_name)
        if m.shape[0] != m.shape[1]:
            raise MathError("Dim ERROR (matrix must be square)")
        det_val = m.det()
        if abs(float(sp.N(det_val))) < 1e-12:
            raise MathError("Math ERROR (singular matrix has no inverse)")
        res = m.inv()
        self.matrices["MATANS"] = res
        return res

    def power(self, a_name: str, p: int) -> sp.Matrix:
        m = self.get_matrix(a_name)
        if m.shape[0] != m.shape[1]:
            raise MathError("Dim ERROR (matrix must be square)")
        res = m ** p
        self.matrices["MATANS"] = res
        return res

    def format_matrix(self, m: sp.Matrix) -> str:
        rows = m.tolist()
        return "[" + ", ".join("[" + ", ".join(str(val) for val in row) + "]" for row in rows) + "]"

    def evaluate_expression(self, expr_str: str) -> sp.Matrix | sp.Expr:
        """Parses and evaluates algebraic matrix expression using SymPy."""
        s = expr_str.replace("×", "*").replace("÷", "/").replace("−", "-")
        s = s.replace("²", "**2").replace("³", "**3").replace("⁻¹", "**(-1)")
        local_dict = {
            "MATA": self.get_matrix("MATA") if self.matrices["MATA"] is not None else None,
            "MATB": self.get_matrix("MATB") if self.matrices["MATB"] is not None else None,
            "MATC": self.get_matrix("MATC") if self.matrices["MATC"] is not None else None,
            "MATANS": self.matrices["MATANS"],
            "MatA": self.get_matrix("MATA") if self.matrices["MATA"] is not None else None,
            "MatB": self.get_matrix("MATB") if self.matrices["MATB"] is not None else None,
            "MatC": self.get_matrix("MATC") if self.matrices["MATC"] is not None else None,
            "MatAns": self.matrices["MATANS"],
            "det": lambda m: m.det() if hasattr(m, "det") else sp.Matrix(m).det(),
            "Trn": lambda m: m.T if hasattr(m, "T") else sp.Matrix(m).T,
            "trn": lambda m: m.T if hasattr(m, "T") else sp.Matrix(m).T,
        }
        try:
            res = sp.sympify(s, locals=local_dict)
        except Exception as e:
            err_str = str(e)
            if "size mismatch" in err_str or "ShapeError" in type(e).__name__ or "NonSquareMatrix" in type(e).__name__:
                raise MathError("Dim ERROR")
            raise MathError(err_str)
        if isinstance(res, sp.Matrix):
            self.matrices["MATANS"] = res
        return res

