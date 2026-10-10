"""Complex number engine (CMPLX Mode) supporting rectangular and polar arithmetic."""
import math
import sympy as sp
from src.core.math.errors import MathError

class ComplexEngine:
    """Handles complex number arithmetic, polar/rectangular conversions, and functions."""

    def __init__(self, angle_unit: str = "DEG", complex_format: str = "a+bi"):
        self.angle_unit = angle_unit
        self.complex_format = complex_format  # "a+bi" or "r∠θ"

    def arg(self, z: sp.Expr) -> sp.Expr:
        """Returns the argument (phase angle) of complex number z in current angle unit."""
        z_c = complex(sp.N(z))
        theta_rad = math.atan2(z_c.imag, z_c.real)

        if self.angle_unit == "DEG":
            theta = theta_rad * 180 / math.pi
        elif self.angle_unit == "GRA":
            theta = theta_rad * 200 / math.pi
        else:
            theta = theta_rad

        return sp.Float(round(theta, 10))

    def conjg(self, z: sp.Expr) -> sp.Expr:
        """Returns the complex conjugate of z."""
        return sp.conjugate(z)

    def abs_mod(self, z: sp.Expr) -> sp.Expr:
        """Returns the modulus / absolute value of z."""
        return sp.Abs(z)

    def polar_to_complex(self, r: float | sp.Expr, theta: float | sp.Expr) -> sp.Expr:
        """Converts polar notation r∠θ into rectangular complex form a + bi."""
        r_val = float(sp.N(r))
        th_val = float(sp.N(theta))

        if self.angle_unit == "DEG":
            th_rad = math.radians(th_val)
        elif self.angle_unit == "GRA":
            th_rad = th_val * math.pi / 200
        else:
            th_rad = th_val

        real_part = r_val * math.cos(th_rad)
        imag_part = r_val * math.sin(th_rad)

        return sp.Float(round(real_part, 10)) + sp.I * sp.Float(round(imag_part, 10))

    def format_complex(self, z: sp.Expr, target_format: str | None = None) -> str:
        """Formats a complex number into a+bi or r∠θ string."""
        fmt = target_format or self.complex_format
        try:
            z_c = complex(sp.N(z))
        except Exception:
            return str(z)

        real = z_c.real
        imag = z_c.imag

        # Format small numbers as 0
        if abs(real) < 1e-12:
            real = 0.0
        if abs(imag) < 1e-12:
            imag = 0.0

        if fmt == "r∠θ":
            r = math.hypot(real, imag)
            th_rad = math.atan2(imag, real)
            if self.angle_unit == "DEG":
                th = math.degrees(th_rad)
            elif self.angle_unit == "GRA":
                th = th_rad * 200 / math.pi
            else:
                th = th_rad

            r_str = f"{round(r, 9):.10f}".rstrip("0").rstrip(".") or "0"
            th_str = f"{round(th, 9):.10f}".rstrip("0").rstrip(".") or "0"
            return f"{r_str}∠{th_str}"

        # Default a+bi format
        if imag == 0:
            s = f"{round(real, 9):.10f}".rstrip("0").rstrip(".")
            return s or "0"
        if real == 0:
            if imag == 1:
                return "i"
            if imag == -1:
                return "-i"
            s_img = f"{round(imag, 9):.10f}".rstrip("0").rstrip(".")
            return f"{s_img}i"

        sign = "+" if imag > 0 else "-"
        abs_img = abs(imag)
        img_str = "i" if abs_img == 1 else f"{round(abs_img, 9):.10f}".rstrip("0").rstrip(".") + "i"
        real_str = f"{round(real, 9):.10f}".rstrip("0").rstrip(".")
        return f"{real_str}{sign}{img_str}"
