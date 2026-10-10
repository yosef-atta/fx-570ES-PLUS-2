"""Vector calculations (VECTOR Mode) supporting 2D/3D vectors, dot, and cross products."""
import math
from src.core.math.errors import MathError

class VectorEngine:
    """Manages vector storage (VctA, VctB, VctC, VctAns) and 2D/3D vector operations."""

    def __init__(self):
        self.vectors: dict[str, list[float] | None] = {
            "VCTA": None,
            "VCTB": None,
            "VCTC": None,
            "VCTANS": None,
        }

    def set_vector(self, name: str, data: list[float]) -> None:
        name_upper = name.upper()
        if len(data) not in (2, 3):
            raise MathError("Vector dimension must be 2 or 3")
        self.vectors[name_upper] = [float(x) for x in data]

    def get_vector(self, name: str) -> list[float]:
        name_upper = name.upper()
        v = self.vectors.get(name_upper)
        if v is None:
            raise MathError(f"Vector {name} is empty")
        return list(v)

    def add(self, a_name: str, b_name: str) -> list[float]:
        v1 = self.get_vector(a_name)
        v2 = self.get_vector(b_name)
        if len(v1) != len(v2):
            raise MathError("Dim ERROR (vector dimensions must match)")
        res = [x + y for x, y in zip(v1, v2)]
        self.vectors["VCTANS"] = res
        return res

    def sub(self, a_name: str, b_name: str) -> list[float]:
        v1 = self.get_vector(a_name)
        v2 = self.get_vector(b_name)
        if len(v1) != len(v2):
            raise MathError("Dim ERROR (vector dimensions must match)")
        res = [x - y for x, y in zip(v1, v2)]
        self.vectors["VCTANS"] = res
        return res

    def scalar_mul(self, k: float, a_name: str) -> list[float]:
        v = self.get_vector(a_name)
        res = [k * x for x in v]
        self.vectors["VCTANS"] = res
        return res

    def dot(self, a_name: str, b_name: str) -> float:
        """Dot product: VctA • VctB."""
        v1 = self.get_vector(a_name)
        v2 = self.get_vector(b_name)
        if len(v1) != len(v2):
            raise MathError("Dim ERROR (vector dimensions must match)")
        return sum(x * y for x, y in zip(v1, v2))

    def cross(self, a_name: str, b_name: str) -> list[float]:
        """Cross product: VctA × VctB (3D only)."""
        v1 = self.get_vector(a_name)
        v2 = self.get_vector(b_name)
        if len(v1) != 3 or len(v2) != 3:
            raise MathError("Dim ERROR (cross product requires 3D vectors)")
        x1, y1, z1 = v1
        x2, y2, z2 = v2
        res = [
            round(y1 * z2 - z1 * y2, 10),
            round(z1 * x2 - x1 * z2, 10),
            round(x1 * y2 - y1 * x2, 10),
        ]
        self.vectors["VCTANS"] = res
        return res

    def magnitude(self, a_name: str) -> float:
        """Vector magnitude: Abs(VctA)."""
        v = self.get_vector(a_name)
        return math.sqrt(sum(x ** 2 for x in v))

    def format_vector(self, v: list[float]) -> str:
        vals = [f"{round(x, 9):.10f}".rstrip("0").rstrip(".") or "0" for x in v]
        return "[" + ", ".join(vals) + "]"

    def evaluate_expression(self, expr_str: str) -> list[float] | float:
        """Evaluates vector expressions with +, -, cross product ×, dot product •, Abs."""
        import re
        s = expr_str.strip()

        # Abs(VctA)
        if s.startswith("Abs(") and s.endswith(")"):
            inner = s[4:-1].strip()
            return self.magnitude(inner)

        # Dot product •
        if "•" in s or " Dot " in s or " dot " in s:
            parts = re.split(r"•|\bDot\b|\bdot\b", s)
            if len(parts) == 2:
                return self.dot(parts[0].strip(), parts[1].strip())

        # Cross product or scalar mul
        if "×" in s or "*" in s:
            parts = re.split(r"×|\*", s)
            if len(parts) == 2:
                p1, p2 = parts[0].strip(), parts[1].strip()
                try:
                    k = float(p1)
                    return self.scalar_mul(k, p2)
                except ValueError:
                    pass
                try:
                    k = float(p2)
                    return self.scalar_mul(k, p1)
                except ValueError:
                    pass
                return self.cross(p1, p2)

        # Addition +
        if "+" in s:
            parts = s.split("+")
            if len(parts) == 2:
                return self.add(parts[0].strip(), parts[1].strip())

        # Subtraction -
        if "-" in s or "−" in s:
            parts = re.split(r"-|−", s)
            if len(parts) == 2:
                return self.sub(parts[0].strip(), parts[1].strip())

        # Single vector
        v = self.get_vector(s)
        self.vectors["VCTANS"] = v
        return v

