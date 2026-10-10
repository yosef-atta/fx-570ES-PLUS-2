"""Statistical calculations, regression models, and distribution functions (STAT Mode)."""
import math
from dataclasses import dataclass, field
from src.core.math.errors import MathError

STAT_MODELS = (
    "1-VAR", "A+BX", "_+CX^2", "ln X", "e^X", "A•B^X", "A•X^B", "1/X"
)

@dataclass
class StatDataRow:
    x: float
    y: float = 0.0
    freq: int = 1


class StatEngine:
    """Computes sample statistics, regression parameters, and normal distributions."""

    def __init__(self, stat_type: str = "1-VAR"):
        self.stat_type = stat_type
        self.data: list[StatDataRow] = []

    def clear(self) -> None:
        self.data.clear()

    def add_row(self, x: float, y: float = 0.0, freq: int = 1) -> None:
        self.data.append(StatDataRow(x=x, y=y, freq=max(1, freq)))

    def n(self) -> int:
        return sum(r.freq for r in self.data)

    def sum_x(self) -> float:
        return sum(r.x * r.freq for r in self.data)

    def sum_x2(self) -> float:
        return sum((r.x ** 2) * r.freq for r in self.data)

    def sum_y(self) -> float:
        return sum(r.y * r.freq for r in self.data)

    def sum_y2(self) -> float:
        return sum((r.y ** 2) * r.freq for r in self.data)

    def sum_xy(self) -> float:
        return sum(r.x * r.y * r.freq for r in self.data)

    def mean_x(self) -> float:
        total_n = self.n()
        if total_n == 0:
            raise MathError("STAT: empty dataset")
        return self.sum_x() / total_n

    def mean_y(self) -> float:
        total_n = self.n()
        if total_n == 0:
            raise MathError("STAT: empty dataset")
        return self.sum_y() / total_n

    def sigma_x(self) -> float:
        total_n = self.n()
        if total_n == 0:
            raise MathError("STAT: empty dataset")
        mx = self.mean_x()
        var = sum(((r.x - mx) ** 2) * r.freq for r in self.data) / total_n
        return math.sqrt(max(0.0, var))

    def sx(self) -> float:
        total_n = self.n()
        if total_n <= 1:
            raise MathError("STAT: sample size must be > 1")
        mx = self.mean_x()
        var = sum(((r.x - mx) ** 2) * r.freq for r in self.data) / (total_n - 1)
        return math.sqrt(max(0.0, var))

    def sigma_y(self) -> float:
        total_n = self.n()
        if total_n == 0:
            raise MathError("STAT: empty dataset")
        my = self.mean_y()
        var = sum(((r.y - my) ** 2) * r.freq for r in self.data) / total_n
        return math.sqrt(max(0.0, var))

    def sy(self) -> float:
        total_n = self.n()
        if total_n <= 1:
            raise MathError("STAT: sample size must be > 1")
        my = self.mean_y()
        var = sum(((r.y - my) ** 2) * r.freq for r in self.data) / (total_n - 1)
        return math.sqrt(max(0.0, var))

    def min_x(self) -> float:
        if not self.data:
            raise MathError("STAT: empty dataset")
        return min(r.x for r in self.data)

    def max_x(self) -> float:
        if not self.data:
            raise MathError("STAT: empty dataset")
        return max(r.x for r in self.data)

    def min_y(self) -> float:
        if not self.data:
            raise MathError("STAT: empty dataset")
        return min(r.y for r in self.data)

    def max_y(self) -> float:
        if not self.data:
            raise MathError("STAT: empty dataset")
        return max(r.y for r in self.data)

    def linear_reg(self) -> tuple[float, float, float]:
        """Returns (A, B, r) for linear model y = A + Bx."""
        total_n = self.n()
        if total_n < 2:
            raise MathError("STAT: at least 2 data points required")
        sx = self.sum_x()
        sy = self.sum_y()
        sx2 = self.sum_x2()
        sy2 = self.sum_y2()
        sxy = self.sum_xy()

        denom_b = (total_n * sx2) - (sx ** 2)
        if denom_b == 0:
            raise MathError("STAT: singular regression data")

        b = ((total_n * sxy) - (sx * sy)) / denom_b
        a = (sy - b * sx) / total_n

        denom_r = math.sqrt(abs(denom_b * ((total_n * sy2) - (sy ** 2))))
        r = ((total_n * sxy) - (sx * sy)) / denom_r if denom_r != 0 else 1.0

        return a, b, r

    def estimate_y(self, x: float) -> float:
        a, b, _ = self.linear_reg()
        return a + b * x

    def estimate_x(self, y: float) -> float:
        a, b, _ = self.linear_reg()
        if b == 0:
            raise MathError("STAT: slope is 0")
        return (y - a) / b

    @staticmethod
    def norm_p(t: float) -> float:
        """P(t) = standard normal CDF."""
        return 0.5 * (1.0 + math.erf(t / math.sqrt(2.0)))

    @staticmethod
    def norm_q(t: float) -> float:
        """Q(t) = P(t) - 0.5 for t >= 0, or 0.5 - P(t) for t < 0."""
        p = StatEngine.norm_p(t)
        return abs(p - 0.5)

    @staticmethod
    def norm_r(t: float) -> float:
        """R(t) = 1 - P(t)."""
        return 1.0 - StatEngine.norm_p(t)

    def to_t(self, x: float) -> float:
        """Standardized normal variate: t = (x - mean_x) / sigma_x."""
        sig = self.sigma_x()
        if sig == 0:
            raise MathError("STAT: standard deviation is 0")
        return (x - self.mean_x()) / sig
