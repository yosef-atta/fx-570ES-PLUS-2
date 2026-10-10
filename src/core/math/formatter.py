"""Formatting engine for exact/decimal switching, Fix/Sci/Norm, and Engineering notation."""
import math
from decimal import Context, Decimal, ROUND_HALF_UP
import sympy as sp
from .evaluator import EvaluationResult

class Formatter:
    """Formats evaluation results according to display settings and S⇔D toggle state."""

    def __init__(self, number_format: str = "Norm 1", display_format: str = "MthIO-MathO"):
        self.number_format = number_format  # "Norm 1", "Norm 2", "Fix N", "Sci N"
        self.display_format = display_format  # "MthIO-MathO", "LineIO"

    def get_representations(self, result: EvaluationResult) -> list[str]:
        """Returns the list of cyclic representations for the S⇔D button."""
        exact = result.exact
        numeric = result.numeric

        reps: list[str] = []

        # 0. Complex number representation
        if isinstance(exact, sp.Expr) and exact.has(sp.I):
            from src.core.modes.complex_engine import ComplexEngine
            ce = ComplexEngine()
            reps.append(ce.format_complex(exact, "a+bi"))
            reps.append(ce.format_complex(exact, "r∠θ"))
            return reps

        # 1. Decimal representation first if Fix or Sci is active
        if self.number_format.startswith(("Fix", "Sci")) and numeric is not None:
            reps.append(self.format_number(numeric))

        # 2. Exact representation if available
        if self.display_format.startswith("MthIO"):
            if isinstance(exact, sp.Rational) and exact.q != 1:
                # Proper or improper fraction
                frac_str = self._format_rational(exact)
                if frac_str not in reps:
                    reps.append(frac_str)
                # Mixed fraction if |numerator| > denominator
                if abs(exact.p) > exact.q:
                    reps.append(self._format_mixed_rational(exact))
            elif isinstance(exact, sp.Expr) and not isinstance(exact, (sp.Integer, sp.Float)):
                exact_str = self._format_exact_expr(exact)
                if exact_str not in reps:
                    reps.append(exact_str)

        # 3. Standard Decimal representation if not already included
        if numeric is not None:
            dec_str = self.format_number(numeric)
            if dec_str not in reps:
                reps.append(dec_str)

        # Fallback if empty
        if not reps:
            reps.append(str(exact))

        return reps

    def format_number(self, val: float, eng_shift: int | None = None) -> str:
        """Formats a floating point number according to Fix/Sci/Norm or ENG shift."""
        if math.isnan(val):
            return "Math ERROR"
        if math.isinf(val):
            return "Math ERROR"

        # Check for zero
        if val == 0:
            if eng_shift is not None:
                return f"0×10^{eng_shift * 3}"
            if self.number_format.startswith("Fix"):
                n = int(self.number_format.split()[-1])
                return f"0.{'0' * n}" if n > 0 else "0"
            if self.number_format.startswith("Sci"):
                n = int(self.number_format.split()[-1])
                return f"0.{'0' * max(0, n - 1)}×10⁰"
            return "0"

        # Engineering notation override if eng_shift is specified
        if eng_shift is not None:
            return self._format_eng(val, eng_shift)

        # Fix N
        if self.number_format.startswith("Fix"):
            n = int(self.number_format.split()[-1])
            try:
                d = Decimal(str(val))
                quant = Decimal('1e-' + str(n)) if n > 0 else Decimal('1')
                rounded = d.quantize(quant, rounding=ROUND_HALF_UP)
                return f"{rounded:.{n}f}"
            except Exception:
                return f"{val:.{n}f}"

        # Sci N
        if self.number_format.startswith("Sci"):
            n = int(self.number_format.split()[-1])
            digits = max(1, n)
            try:
                ctx = Context(prec=digits, rounding=ROUND_HALF_UP)
                d = ctx.create_decimal(str(val))
                s = f"{d:e}"
                mant, exp = s.lower().split("e")
                if "." not in mant:
                    mant += "."
                int_part, frac_part = mant.split(".")
                needed = (digits - 1) - len(frac_part)
                if needed > 0:
                    frac_part += "0" * needed
                mant = f"{int_part}.{frac_part}" if digits > 1 else int_part
                exp_int = int(exp)
                return f"{mant}×10^{exp_int}"
            except Exception:
                s = f"{val:.{digits - 1}e}"
                mant, exp = s.split("e")
                exp_int = int(exp)
                return f"{mant}×10^{exp_int}"

        # Norm 1 vs Norm 2
        # Casio specifications:
        # Norm 1: exponential for |x| < 10^-2 or |x| >= 10^10
        # Norm 2: exponential for |x| < 10^-9 or |x| >= 10^10
        abs_v = abs(val)
        low_bound = 1e-2 if self.number_format == "Norm 1" else 1e-9

        if abs_v < low_bound or abs_v >= 1e10:
            # Format as scientific with up to 10 significant digits
            s = f"{val:.9e}"
            mant, exp = s.split("e")
            mant = mant.rstrip("0").rstrip(".")
            exp_int = int(exp)
            return f"{mant}×10^{exp_int}"

        # Standard decimal up to 10 significant digits
        rounded = round(val, 9)
        # Avoid scientific notation
        dec = f"{rounded:.10f}".rstrip("0").rstrip(".")
        return dec if dec else "0"

    def _format_eng(self, val: float, eng_shift: int) -> str:
        """Formats number with power-of-10 exponent that is a multiple of 3."""
        if val == 0:
            return f"0×10^{eng_shift * 3}"

        exp = math.floor(math.log10(abs(val)))
        eng_exp = (exp // 3) * 3 + (eng_shift * 3)
        mantissa = val / (10 ** eng_exp)

        # Format mantissa cleanly
        mant_str = f"{mantissa:.9f}".rstrip("0").rstrip(".")
        if not mant_str:
            mant_str = "0"
        return f"{mant_str}×10^{eng_exp}"

    def _format_rational(self, rat: sp.Rational) -> str:
        return f"{rat.p}/{rat.q}"

    def _format_mixed_rational(self, rat: sp.Rational) -> str:
        whole = abs(rat.p) // rat.q
        rem = abs(rat.p) % rat.q
        sign = "-" if rat.p < 0 else ""
        return f"{sign}{whole} {rem}/{rat.q}"

    def _format_exact_expr(self, expr: sp.Expr) -> str:
        # Clean SymPy string representation into standard calculator format
        import re
        s = str(expr)
        s = s.replace("sqrt", "√")
        s = s.replace("*", "")
        s = s.replace("pi", "π")
        s = re.sub(r'√\((\w+)\)', r'√\1', s)
        return s
