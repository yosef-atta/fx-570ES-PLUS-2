"""Evaluation engine combining SymPy exact arithmetic and numerical computation."""
import math
import random
import sympy as sp
from .ast_nodes import (
    ASTNode, NumberNode, VariableNode, ConstantNode, AnsNode, PreAnsNode,
    UnaryOpNode, BinaryOpNode, PostfixOpNode, FractionNode, MixedFractionNode,
    FunctionCallNode, DerivativeNode, IntegralNode, SummationNode,
    EquationNode, MultiStatementNode, DMSNode
)
from .errors import MathError, ArgumentError, SyntaxError

MAX_MAGNITUDE = 10**100


class EvaluationResult:
    """Encapsulates the exact symbolic form, numerical float form, and original expression."""

    def __init__(self, exact_value: sp.Expr | int | float, numeric_value: float | None = None):
        self.exact = exact_value
        if numeric_value is not None:
            self.numeric = numeric_value
        else:
            try:
                self.numeric = float(sp.N(exact_value))
            except Exception:
                self.numeric = None

    def __repr__(self) -> str:
        return f"EvaluationResult(exact={self.exact}, numeric={self.numeric})"


class Evaluator:
    """Evaluates an AST under given angle units and memory variables."""

    def __init__(
        self,
        angle_unit: str = "DEG",
        memory: dict[str, sp.Expr | float] | None = None,
        mode: str = "COMP"
    ):
        self.angle_unit = angle_unit  # "DEG", "RAD", "GRA"
        self.memory = memory if memory is not None else {}
        self.mode = mode

    def evaluate(self, node: ASTNode) -> EvaluationResult:
        res = self._eval_node(node)
        # Check magnitude overflow
        try:
            num = float(sp.N(res))
            if abs(num) >= MAX_MAGNITUDE:
                raise MathError("Calculation overflow", position=node.position)
        except (OverflowError, ValueError):
            raise MathError("Calculation overflow", position=node.position)
        except Exception:
            pass
        return EvaluationResult(res)

    def _eval_node(self, node: ASTNode) -> sp.Expr:
        if isinstance(node, NumberNode):
            # Parse number into SymPy Integer or Rational
            val_str = node.value
            if "." in val_str:
                from fractions import Fraction
                s = val_str
                parts = s.split(".")
                dec_part = parts[1]
                # Detect repeating tail, e.g. .0121111 or 0.33333 or .16666
                if len(dec_part) >= 3 and dec_part[-1] == dec_part[-2] == dec_part[-3] and dec_part[-1].isdigit():
                    s = (parts[0] or "0") + "." + dec_part + dec_part[-1] * max(0, 16 - len(dec_part))
                try:
                    f = Fraction(s).limit_denominator(100000)
                    if abs(float(f) - float(val_str)) < 1e-4:
                        if len(str(f.numerator)) + len(str(f.denominator)) <= 10:
                            return sp.Rational(f.numerator, f.denominator)
                except Exception:
                    pass
                denom = 10 ** len(dec_part)
                numer = int(parts[0] + dec_part) if parts[0] else int(dec_part)
                return sp.Rational(numer, denom)
            return sp.Integer(int(val_str))

        if isinstance(node, VariableNode):
            name = node.name.upper()
            if name in self.memory:
                val = self.memory[name]
                return sp.sympify(val)
            return sp.Integer(0)

        if isinstance(node, ConstantNode):
            if node.name == "pi":
                return sp.pi
            if node.name == "e":
                return sp.E
            if node.name == "i":
                return sp.I
            raise ArgumentError(f"Unknown constant {node.name}", position=node.position)

        if isinstance(node, AnsNode):
            if "Ans" in self.memory:
                return sp.sympify(self.memory["Ans"])
            return sp.Integer(0)

        if isinstance(node, PreAnsNode):
            if "PreAns" in self.memory:
                return sp.sympify(self.memory["PreAns"])
            return sp.Integer(0)

        if isinstance(node, UnaryOpNode):
            operand = self._eval_node(node.operand)
            if node.op == "−" or node.op == "-":
                return -operand
            raise SyntaxError(f"Unknown unary operator {node.op}", position=node.position)

        if isinstance(node, BinaryOpNode):
            return self._eval_binary(node)

        if isinstance(node, PostfixOpNode):
            return self._eval_postfix(node)

        if isinstance(node, FractionNode):
            num = self._eval_node(node.numerator)
            den = self._eval_node(node.denominator)
            if den == 0:
                raise MathError("Division by zero", position=node.position)
            return num / den

        if isinstance(node, MixedFractionNode):
            whole = self._eval_node(node.whole)
            num = self._eval_node(node.numerator)
            den = self._eval_node(node.denominator)
            if den == 0:
                raise MathError("Division by zero", position=node.position)
            sign = -1 if whole < 0 else 1
            return whole + sign * (num / den)

        if isinstance(node, FunctionCallNode):
            return self._eval_function(node)

        if isinstance(node, DerivativeNode):
            return self._eval_derivative(node)

        if isinstance(node, IntegralNode):
            return self._eval_integral(node)

        if isinstance(node, SummationNode):
            return self._eval_summation(node)

        if isinstance(node, EquationNode):
            if isinstance(node.left, VariableNode):
                val = self._eval_node(node.right)
                self.memory[node.left.name.upper()] = val
                return val
            # For equation, returns left - right
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return left - right

        if isinstance(node, MultiStatementNode):
            # Evaluates the last statement
            res = sp.Integer(0)
            for stmt in node.statements:
                res = self._eval_node(stmt)
            return res

        raise SyntaxError(f"Cannot evaluate AST node {type(node).__name__}", position=node.position)

    def _eval_binary(self, node: BinaryOpNode) -> sp.Expr:
        # Check percentage addition/subtraction
        if isinstance(node.right, PostfixOpNode) and node.right.op == "%":
            left = self._eval_node(node.left)
            pct_val = self._eval_node(node.right.operand)
            pct_ratio = pct_val / 100
            if node.op == "+":
                return left * (1 + pct_ratio)
            elif node.op == "-":
                return left * (1 - pct_ratio)
            elif node.op == "×":
                return left * pct_ratio
            elif node.op == "÷":
                if pct_ratio == 0:
                    raise MathError("Division by zero", position=node.position)
                return left / pct_ratio

        left = self._eval_node(node.left)
        right = self._eval_node(node.right)

        if node.op == "+":
            return left + right
        if node.op == "-":
            return left - right
        if node.op == "×":
            return left * right
        if node.op == "÷":
            if right == 0:
                raise MathError("Division by zero", position=node.position)
            return left / right
        if node.op == "^":
            # Power
            try:
                # Disallow 0^0 or complex numbers in COMP mode
                if left == 0 and right <= 0:
                    raise MathError("Math ERROR (0^0 or division by zero)", position=node.position)
                res = left ** right
                # If result is complex, in COMP mode raise Math ERROR
                if self.mode != "CMPLX" and getattr(res, "is_real", None) is False:
                    raise MathError("Non-real result in COMP mode", position=node.position)
                return res
            except Exception as e:
                if isinstance(e, MathError):
                    raise
                raise MathError(str(e), position=node.position)

        if node.op == "∠":
            r_val = float(sp.N(left))
            th_val = float(sp.N(right))
            if self.angle_unit == "DEG":
                th_rad = math.radians(th_val)
            elif self.angle_unit == "GRA":
                th_rad = th_val * math.pi / 200
            else:
                th_rad = th_val
            real_part = r_val * math.cos(th_rad)
            imag_part = r_val * math.sin(th_rad)
            return sp.Float(round(real_part, 10)) + sp.I * sp.Float(round(imag_part, 10))

        if node.op == "nPr":
            # Permutations: n! / (n - r)!
            return self._npr(left, right, node.position)
        if node.op == "nCr":
            # Combinations: n! / (r! (n - r)!)
            return self._ncr(left, right, node.position)

        raise SyntaxError(f"Unknown binary operator {node.op}", position=node.position)

    def _eval_postfix(self, node: PostfixOpNode) -> sp.Expr:
        operand = self._eval_node(node.operand)

        if node.op == "!":
            # Factorial
            try:
                n = int(operand)
                if n != operand or n < 0 or n > 69:
                    raise MathError("Factorial input out of range (0 <= n <= 69)", position=node.position)
                return sp.factorial(n)
            except Exception as e:
                if isinstance(e, MathError):
                    raise
                raise MathError("Invalid factorial input", position=node.position)

        if node.op == "%":
            return operand / 100

        if node.op == "°":
            # DMS symbol on a scalar (angle)
            return operand

        raise SyntaxError(f"Unknown postfix operator {node.op}", position=node.position)

    def _eval_function(self, node: FunctionCallNode) -> sp.Expr:
        name = node.name.lower()
        args = [self._eval_node(arg) for arg in node.args]

        # 0-arg function
        if name in ("ran#", "ran"):
            # Generates random 3-decimal fraction [0.000, 0.999]
            val = random.randint(0, 999)
            return sp.Rational(val, 1000)

        if not args:
            raise SyntaxError(f"Function {name} requires arguments", position=node.position)

        x = args[0]

        # Trig functions (convert angle to radians according to current mode)
        if name in ("sin", "cos", "tan"):
            rad = self._to_radians(x)
            if name == "sin":
                return sp.sin(rad)
            if name == "cos":
                return sp.cos(rad)
            if name == "tan":
                # Check for cos(rad) == 0 (e.g. 90 deg)
                if sp.cos(rad) == 0:
                    raise MathError("Tangent domain error (Math ERROR)", position=node.position)
                return sp.tan(rad)

        # Inverse Trig functions
        if name in ("asin", "sin⁻¹", "acos", "cos⁻¹", "atan", "tan⁻¹"):
            try:
                val_num = float(sp.N(x))
            except Exception:
                val_num = 0.0

            if name in ("asin", "sin⁻¹"):
                if abs(val_num) > 1.0000000001:
                    raise MathError("Domain error for sin⁻¹ (|x| <= 1)", position=node.position)
                rad = sp.asin(x)
                return self._from_radians(rad)
            if name in ("acos", "cos⁻¹"):
                if abs(val_num) > 1.0000000001:
                    raise MathError("Domain error for cos⁻¹ (|x| <= 1)", position=node.position)
                rad = sp.acos(x)
                return self._from_radians(rad)
            if name in ("atan", "tan⁻¹"):
                rad = sp.atan(x)
                return self._from_radians(rad)

        # Hyperbolic functions
        if name == "sinh":
            return sp.sinh(x)
        if name == "cosh":
            return sp.cosh(x)
        if name == "tanh":
            return sp.tanh(x)

        # Inverse Hyperbolic functions
        if name in ("asinh", "sinh⁻¹"):
            return sp.asinh(x)
        if name in ("acosh", "cosh⁻¹"):
            try:
                if float(sp.N(x)) < 1.0:
                    raise MathError("Domain error for cosh⁻¹ (x >= 1)", position=node.position)
            except MathError:
                raise
            except Exception:
                pass
            return sp.acosh(x)
        if name in ("atanh", "tanh⁻¹"):
            try:
                if abs(float(sp.N(x))) >= 1.0:
                    raise MathError("Domain error for tanh⁻¹ (|x| < 1)", position=node.position)
            except MathError:
                raise
            except Exception:
                pass
            return sp.atanh(x)

        # Logarithms & Exponential
        if name == "ln":
            try:
                if float(sp.N(x)) <= 0:
                    raise MathError("ln domain error (x > 0)", position=node.position)
            except MathError:
                raise
            except Exception:
                pass
            return sp.log(x)

        if name == "log":
            # If two arguments log(base, value)
            if len(args) == 2:
                base, val = args[0], args[1]
                try:
                    if float(sp.N(base)) <= 0 or float(sp.N(base)) == 1 or float(sp.N(val)) <= 0:
                        raise MathError("log domain error", position=node.position)
                except MathError:
                    raise
                except Exception:
                    pass
                return sp.log(val, base)
            # Default base 10
            try:
                if float(sp.N(x)) <= 0:
                    raise MathError("log domain error (x > 0)", position=node.position)
            except MathError:
                raise
            except Exception:
                pass
            return sp.log(x, 10)

        if name == "exp" or name == "eˣ":
            return sp.exp(x)

        if name == "ten_pow" or name == "10ˣ":
            return 10 ** x

        # Square roots & Roots
        if name == "sqrt":
            try:
                if self.mode != "CMPLX" and float(sp.N(x)) < 0:
                    raise MathError("Negative square root in COMP mode", position=node.position)
            except MathError:
                raise
            except Exception:
                pass
            return sp.sqrt(x)

        if name == "cbrt":
            return sp.cbrt(x)

        if name == "nth_root":
            # xth root of y: args[0]=root_index, args[1]=radicand
            if len(args) < 2:
                raise ArgumentError("ˣ√ requires root index and radicand", position=node.position)
            root_idx, radicand = args[0], args[1]
            return radicand ** (1 / root_idx)

        # General Functions
        if name == "abs":
            return sp.Abs(x)

        if name == "rnd":
            # Round function according to display format
            return x

        if name in ("ranint#", "ranint"):
            if len(args) < 2:
                raise ArgumentError("RanInt# requires a and b", position=node.position)
            a = int(args[0])
            b = int(args[1])
            if a > b:
                raise ArgumentError("RanInt# requires a <= b", position=node.position)
            return sp.Integer(random.randint(a, b))

        # Coordinate Conversions
        if name == "pol":
            # Pol(x, y) -> r
            if len(args) < 2:
                raise ArgumentError("Pol requires x and y", position=node.position)
            x_coord, y_coord = args[0], args[1]
            r = sp.sqrt(x_coord**2 + y_coord**2)
            theta_rad = sp.atan2(y_coord, x_coord)
            theta = self._from_radians(theta_rad)
            self.memory["X"] = r
            self.memory["Y"] = theta
            return r

        if name == "rec":
            # Rec(r, θ) -> x
            if len(args) < 2:
                raise ArgumentError("Rec requires r and θ", position=node.position)
            r, theta = args[0], args[1]
            theta_rad = self._to_radians(theta)
            x_coord = r * sp.cos(theta_rad)
            y_coord = r * sp.sin(theta_rad)
            self.memory["X"] = x_coord
            self.memory["Y"] = y_coord
            return x_coord

        # Complex Functions
        if name == "arg":
            z_c = complex(sp.N(x))
            theta_rad = math.atan2(z_c.imag, z_c.real)
            if self.angle_unit == "DEG":
                theta = theta_rad * 180 / math.pi
            elif self.angle_unit == "GRA":
                theta = theta_rad * 200 / math.pi
            else:
                theta = theta_rad
            return sp.Float(round(theta, 10))

        if name in ("conjg", "conjugate"):
            return sp.conjugate(x)

        raise SyntaxError(f"Unknown function {name}", position=node.position)

    def _eval_derivative(self, node: DerivativeNode) -> sp.Expr:
        # d/dx(f(x), a, [tol])
        val = self._eval_node(node.at_point)
        x_sym = sp.Symbol(node.variable)
        # Evaluate expr symbolically by substituting X with Symbol X
        evaluator_sym = Evaluator(angle_unit=self.angle_unit, memory=dict(self.memory))
        evaluator_sym.memory[node.variable] = x_sym
        expr_sym = evaluator_sym._eval_node(node.expr)
        diff_sym = sp.diff(expr_sym, x_sym)
        res = diff_sym.subs(x_sym, val)
        return res

    def _eval_integral(self, node: IntegralNode) -> sp.Expr:
        # ∫(f(x), a, b, [tol])
        lower = self._eval_node(node.lower)
        upper = self._eval_node(node.upper)
        x_sym = sp.Symbol(node.variable)

        evaluator_sym = Evaluator(angle_unit=self.angle_unit, memory=dict(self.memory))
        evaluator_sym.memory[node.variable] = x_sym
        expr_sym = evaluator_sym._eval_node(node.expr)

        # Attempt exact integration, fallback to numerical quad
        try:
            exact_int = sp.integrate(expr_sym, (x_sym, lower, upper))
            if not isinstance(exact_int, sp.Integral):
                return exact_int
        except Exception:
            pass

        # Numerical fallback
        try:
            f = sp.lambdify(x_sym, expr_sym, "math")
            val_num = self._simpson_quad(f, float(lower), float(upper))
            return sp.Float(val_num)
        except Exception as e:
            raise MathError(f"Integration error: {e}", position=node.position)

    def _eval_summation(self, node: SummationNode) -> sp.Expr:
        # Σ(f(x), a, b)
        a = int(self._eval_node(node.lower))
        b = int(self._eval_node(node.upper))
        if a > b:
            return sp.Integer(0)

        total = sp.Integer(0)
        evaluator_sym = Evaluator(angle_unit=self.angle_unit, memory=dict(self.memory))
        for k in range(a, b + 1):
            evaluator_sym.memory[node.variable] = sp.Integer(k)
            term = evaluator_sym._eval_node(node.expr)
            total += term
        return total

    def _simpson_quad(self, f, a: float, b: float, n: int = 1000) -> float:
        """Composite Simpson's 1/3 rule for numerical integration."""
        if n % 2 != 0:
            n += 1
        h = (b - a) / n
        s = f(a) + f(b)
        for i in range(1, n, 2):
            s += 4 * f(a + i * h)
        for i in range(2, n, 2):
            s += 2 * f(a + i * h)
        return s * (h / 3)

    def _to_radians(self, x: sp.Expr) -> sp.Expr:
        if self.angle_unit == "DEG":
            return x * sp.pi / 180
        if self.angle_unit == "GRA":
            return x * sp.pi / 200
        return x  # RAD

    def _from_radians(self, rad: sp.Expr) -> sp.Expr:
        if self.angle_unit == "DEG":
            return rad * 180 / sp.pi
        if self.angle_unit == "GRA":
            return rad * 200 / sp.pi
        return rad  # RAD

    def _npr(self, n: sp.Expr, r: sp.Expr, pos: int) -> sp.Expr:
        try:
            n_int = int(n)
            r_int = int(r)
            if n_int != n or r_int != r or n_int < 0 or r_int < 0 or r_int > n_int:
                raise MathError("Math ERROR (nPr argument out of domain)", position=pos)
            return sp.factorial(n_int) / sp.factorial(n_int - r_int)
        except MathError:
            raise
        except Exception:
            raise MathError("Math ERROR (nPr invalid arguments)", position=pos)

    def _ncr(self, n: sp.Expr, r: sp.Expr, pos: int) -> sp.Expr:
        try:
            n_int = int(n)
            r_int = int(r)
            if n_int != n or r_int != r or n_int < 0 or r_int < 0 or r_int > n_int:
                raise MathError("Math ERROR (nCr argument out of domain)", position=pos)
            return sp.binomial(n_int, r_int)
        except MathError:
            raise
        except Exception:
            raise MathError("Math ERROR (nCr invalid arguments)", position=pos)
